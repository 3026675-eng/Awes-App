"""Generate the SYNTHETIC sample dataset (no real mine data). Run:  python data/generate_data.py"""
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import auth, config as C  # noqa: E402

SEED = 2026


def gen_users():
    demo = [("admin", "System Administrator", "Administrator", "Admin@123"),
            ("safety", "Sipho Safety (Safety Officer)", "Safety Officer", "Safety@123"),
            ("engineer", "Thandi Engineer (Mining Engineer)", "Mining Engineer", "Mining@123"),
            ("maint", "Pieter Maint (Maintenance Engineer)", "Maintenance Engineer", "Maint@123"),
            ("manager", "Lerato Manager (Manager)", "Manager", "Manager@123")]
    rows = []
    for u, n, r, p in demo:
        salt, h = auth.hash_password(p)
        rows.append([u, n, r, salt, h, "Yes"])
    pd.DataFrame(rows, columns=["username", "full_name", "role", "salt", "password_hash", "active"]).to_csv(C.FILES["users"], index=False)


def gen_workers(rng):
    roles = {"Underground Production": ["Miner", "Team Leader", "Loco Operator"],
             "Surface Mining": ["Truck Operator", "Excavator Operator", "Dozer Operator"],
             "Drilling & Blasting": ["Driller", "Blaster", "Assistant"],
             "Processing Plant": ["Plant Operator", "Crusher Operator", "Lab Technician"],
             "Engineering & Maintenance": ["Fitter", "Electrician", "Boilermaker"],
             "Hauling & Logistics": ["Truck Driver", "Dispatcher", "Loader Operator"]}
    weights = [24, 26, 16, 22, 20, 12]
    rows = []
    for i in range(1, 121):
        dept = rng.choices(C.DEPARTMENTS, weights)[0]
        shift = rng.choices(C.SHIFTS, [58, 42])[0]
        fatigue = min(10, max(1, round(rng.gauss(4.2 if shift == "Day" else 5.6, 1.9))))
        high_cons = dept in ("Underground Production", "Drilling & Blasting")
        like = rng.choices([1, 2, 3, 4, 5], [18, 30, 26, 16, 10])[0]
        cons = rng.choices([1, 2, 3, 4, 5], [10, 20, 28, 24, 18] if high_cons else [20, 28, 26, 16, 10])[0]
        rows.append(dict(worker_id=f"W{i:03d}", department=dept, job_role=rng.choice(roles[dept]), shift=shift,
                         ppe_compliant=rng.choices(["Yes", "No"], [88, 12])[0],
                         training_status=rng.choices(C.TRAINING_STATUS, [80, 12, 8])[0],
                         fatigue_level=fatigue, safety_observations=rng.randint(0, 6),
                         near_misses=rng.choices([0, 1, 2, 3, 4], [40, 30, 18, 8, 4])[0],
                         previous_incidents=rng.choices([0, 1, 2, 3], [60, 25, 11, 4])[0],
                         likelihood=like, consequence=cons))
    pd.DataFrame(rows).to_csv(C.FILES["workers"], index=False)


def gen_incidents(rng, today):
    sev_w = [58, 28, 10, 4]
    rows = []
    for _ in range(220):
        d = today - timedelta(days=rng.randint(0, 364))
        shift = rng.choices(C.SHIFTS, [45, 55])[0]
        hour = rng.randint(6, 17) if shift == "Day" else rng.choice(list(range(18, 24)) + list(range(0, 6)))
        sev = rng.choices(C.SEVERITIES, sev_w)[0]
        inj = {"Minor": rng.choices(C.INJURY_STATUS[:3], [50, 40, 10])[0],
               "Moderate": rng.choices(C.INJURY_STATUS[1:], [20, 65, 15])[0],
               "Major": rng.choices(C.INJURY_STATUS[2:], [55, 45])[0],
               "Critical": "Serious Injury"}[sev]
        lti = "Yes" if inj in ("Medical Treatment", "Serious Injury") and rng.random() < 0.7 else "No"
        age = (today - d).days
        status = "Closed" if age > 60 else rng.choices(C.INCIDENT_STATUS, [25, 35, 40])[0]
        rows.append(dict(date=d.isoformat(), time=f"{hour:02d}:{rng.choice([0, 15, 30, 45]):02d}", shift=shift,
                         location=rng.choice(C.LOCATIONS), department=rng.choices(C.DEPARTMENTS, [24, 26, 16, 20, 20, 14])[0],
                         incident_type=rng.choice(C.INCIDENT_TYPES), severity=sev, injury_status=inj,
                         lost_time_injury=lti, cause=rng.choice(C.CAUSES),
                         corrective_action=rng.choice(["Retraining", "Equipment repair", "Barricading / signage",
                                                        "Procedure revision", "Supervision increased", "Pending"]),
                         incident_status=status))
    df = pd.DataFrame(rows).sort_values(["date", "time"]).reset_index(drop=True)
    df = df.rename(columns={"incident_status": "status"})
    df.insert(0, "incident_id", [f"INC-{r.date[:4]}-{i + 1:04d}" for i, r in df.iterrows()])
    # sequence numbers should be per-year
    counts = {}
    ids = []
    for d in df["date"]:
        y = d[:4]
        counts[y] = counts.get(y, 0) + 1
        ids.append(f"INC-{y}-{counts[y]:04d}")
    df["incident_id"] = ids
    df.to_csv(C.FILES["incidents"], index=False)


def gen_equipment(rng, today):
    mfr = {"Haul Truck": ["Caterpillar", "Komatsu", "Liebherr"], "Loader": ["Caterpillar", "Sandvik", "Epiroc"],
           "Excavator": ["Hitachi", "Komatsu", "Liebherr"], "Drilling Machine": ["Epiroc", "Sandvik"],
           "Bulldozer": ["Caterpillar", "Komatsu"], "Scraper Winch": ["Joy Global", "Epiroc"],
           "Crusher": ["Metso", "FLSmidth"], "Conveyor": ["FLSmidth", "Continental"]}
    counts = {"Haul Truck": 12, "Loader": 5, "Excavator": 4, "Drilling Machine": 5, "Bulldozer": 3,
              "Scraper Winch": 3, "Crusher": 3, "Conveyor": 5}
    dept_of = {"Haul Truck": "Hauling & Logistics", "Loader": "Surface Mining", "Excavator": "Surface Mining",
               "Drilling Machine": "Drilling & Blasting", "Bulldozer": "Surface Mining",
               "Scraper Winch": "Underground Production", "Crusher": "Processing Plant", "Conveyor": "Processing Plant"}
    rows = []
    for et, n in counts.items():
        for k in range(1, n + 1):
            r = rng.random()
            temp = rng.uniform(55, 78) if r < 0.66 else (rng.uniform(80, 99) if r < 0.90 else rng.uniform(101, 118))
            r = rng.random()
            vib = rng.uniform(1.5, 4.8) if r < 0.66 else (rng.uniform(5, 7.9) if r < 0.90 else rng.uniform(8.2, 11))
            wheeled = et in ("Haul Truck", "Loader")
            braked = et in ("Haul Truck", "Loader", "Bulldozer", "Excavator")
            down = rng.choice([rng.uniform(8, 90)] * 4 + [rng.uniform(100, 260)])
            ms = rng.choices(C.MAINTENANCE_STATUS, [85, 12, 3])[0]
            nxt = today + timedelta(days=rng.randint(-15, 75))
            rows.append(dict(
                equipment_id=f"{C.EQUIPMENT_PREFIX[et]}-{k:03d}", equipment_type=et,
                manufacturer=rng.choice(mfr[et]), department=dept_of[et],
                operating_hours=rng.randint(2500, 38000), temperature=round(temp, 1), vibration=round(vib, 1),
                fuel_consumption=round(rng.uniform(40, 130), 1) if et not in ("Conveyor", "Crusher", "Scraper Winch") else 0.0,
                brake_status=rng.choices(["OK", "Worn", "Fault"], [91, 7, 2])[0] if braked else "N/A",
                tyre_status=rng.choices(["OK", "Worn", "Fault"], [88, 10, 2])[0] if wheeled else "N/A",
                engine_status=rng.choices(["OK", "Worn", "Fault"], [91, 7, 2])[0],
                maintenance_status=ms, uptime_hours=round(max(0, C.PERIOD_HOURS - down - rng.uniform(0, 60)), 1),
                downtime_hours=round(down + (rng.uniform(30, 120) if ms != "Operational" else 0), 1),
                last_service_date=(nxt - timedelta(days=rng.choice([90, 120]))).isoformat(),
                next_service_due=nxt.isoformat(), alerts_30d=rng.choices([0, 1, 2, 3, 4, 5], [34, 26, 18, 12, 6, 4])[0]))
    df = pd.DataFrame(rows)
    i = df.index[df["equipment_id"] == "TRK-012"][0]       # matches Figure 1 of the brief
    df.loc[i, ["temperature", "vibration", "engine_status", "maintenance_status"]] = [92.0, 9.2, "OK", "Operational"]
    df.to_csv(C.FILES["equipment"], index=False)


if __name__ == "__main__":
    rng = random.Random(SEED)
    today = date.today()
    C.DATA_DIR.mkdir(exist_ok=True)
    gen_users()
    gen_workers(rng)
    gen_incidents(rng, today)
    gen_equipment(rng, today)
    print("Sample data written to", C.DATA_DIR)
