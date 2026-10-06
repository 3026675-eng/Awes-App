import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import time

st.set_page_config(page_title="Khwezi Mining", page_icon="⛏️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp {
    background:radial-gradient(circle at 80% 0%,rgba(242,169,0,.08),transparent 30%),linear-gradient(135deg,#f6f3eb 0%,#e9e5da 100%);
}
.block-container { max-width:1500px;padding:1rem 2.2rem 3rem; }
h1,h2,h3,h4 { font-family:'Barlow Condensed',sans-serif!important;color:#17191c!important;letter-spacing:.02em; }
h1 { font-size:3rem!important;font-weight:800!important; }
h2 { font-size:2.2rem!important; }
h3 { font-size:1.55rem!important; }
.stButton button { border-radius:12px;min-height:44px;font-weight:800;border:1px solid #d5d0c5;transition:.2s ease; }
.stButton button:hover { border-color:#F2A900;transform:translateY(-1px); }
[data-testid="stMetric"] { background:#fffdf8;border:1px solid #ddd8ce;border-left:5px solid #F2A900;border-radius:15px;padding:15px;box-shadow:0 8px 25px rgba(0,0,0,.05); }
[data-testid="stMetricValue"] { font-family:'Barlow Condensed',sans-serif; }
.app-header { display:flex;align-items:center;justify-content:space-between;gap:15px;background:#111417;color:white;border-radius:18px;padding:13px 16px;margin-bottom:18px;border-bottom:4px solid #F2A900;box-shadow:0 15px 35px rgba(0,0,0,.16); }
.brand { display:flex;align-items:center;gap:11px; }
.brand-mark { width:40px;height:40px;background:#F2A900;color:#111417;border-radius:11px;display:flex;align-items:center;justify-content:center;font-family:'Barlow Condensed',sans-serif;font-size:1.5rem;font-weight:900; }
.brand-name { font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:1.3rem;letter-spacing:.12em;line-height:1; }
.brand-sub { color:#9ca4ac;font-size:.58rem;letter-spacing:.18em;margin-top:4px; }
.domain { background:#F2A900;color:#111417;padding:7px 13px;border-radius:999px;font-size:.7rem;font-weight:900;letter-spacing:.08em; }
.welcome { min-height:470px;border-radius:30px;padding:55px;margin-top:10px;position:relative;overflow:hidden;color:white;background:linear-gradient(90deg,rgba(5,7,9,.94) 0%,rgba(5,7,9,.82) 42%,rgba(5,7,9,.42) 100%),url("https://images.unsplash.com/photo-1578662996442-48f60103fc96?auto=format&fit=crop&w=1800&q=85");background-size:cover;background-position:center;box-shadow:0 25px 70px rgba(0,0,0,.24); }
.welcome-content { position:relative;z-index:2;max-width:750px; }
.kicker { color:#F2A900;text-transform:uppercase;font-size:.75rem;font-weight:900;letter-spacing:.22em; }
.welcome-title { font-family:'Barlow Condensed',sans-serif;font-size:5.2rem;font-weight:900;line-height:.9;margin-top:15px; }
.welcome-title span { color:#F2A900; }
.welcome-text { color:#d4d9de;font-size:1.05rem;line-height:1.7;max-width:620px;margin-top:18px; }
.choice-button button { min-height:230px!important;font-family:'Barlow Condensed',sans-serif!important;font-size:2.1rem!important;font-weight:900!important;text-align:left!important;padding:28px!important;border-radius:24px!important;border:1px solid #d8d2c7!important;background:#fffdf8!important;color:#17191c!important;box-shadow:0 15px 40px rgba(0,0,0,.07); }
.choice-button button:hover { border:2px solid #F2A900!important;background:#fffaf0!important;transform:translateY(-4px);box-shadow:0 25px 55px rgba(0,0,0,.12); }
.choice-small { font-size:.7rem;color:#A86F00;letter-spacing:.16em;font-weight:900; }
.page-card { background:#fffdf8;border:1px solid #ddd8ce;border-radius:20px;padding:22px;min-height:170px;box-shadow:0 9px 28px rgba(0,0,0,.05);margin-bottom:15px; }
.page-card-title { font-family:'Barlow Condensed',sans-serif;font-size:1.6rem;font-weight:900;margin-top:12px; }
.page-card-text { color:#727980;font-size:.88rem;line-height:1.5; }
.alert-card { background:#fffdf8;border-radius:15px;padding:16px;margin-bottom:10px;border:1px solid #ddd8ce; }
.alert-critical { border-left:6px solid #E05252; }
.alert-warning { border-left:6px solid #F2A900; }
.breadcrumb { color:#777e85;font-size:.75rem;text-transform:uppercase;letter-spacing:.12em;margin-bottom:18px; }
.section-title { font-family:'Barlow Condensed',sans-serif;font-size:3rem;font-weight:900;line-height:1; }
.section-subtitle { color:#747b82;margin-bottom:25px; }
@media(max-width:800px) {
    .block-container { padding:.8rem; }
    .welcome { padding:35px 25px; }
    .welcome-title { font-size:3.5rem; }
    .app-header { flex-wrap:wrap; }
    .domain { width:100%;text-align:center; }
}
</style>

""", unsafe_allow_html=True)

if "logged_in" not in st.session_state: st.session_state.logged_in=False
if "role" not in st.session_state: st.session_state.role=None
if "page" not in st.session_state: st.session_state.page="Welcome"
if "history" not in st.session_state: st.session_state.history=[]
if "attempts" not in st.session_state: st.session_state.attempts=0
if "locked_until" not in st.session_state: st.session_state.locked_until=0

USERS = {
"admin":{"password":"Admin@123","role":"Admin"},
"safety":{"password":"Safety@123","role":"Safety Officer"},
"engineer":{"password":"Mining@123","role":"Engineer"},
"maint":{"password":"Maint@123","role":"Maintenance"},
"manager":{"password":"Manager@123","role":"Manager"}
}

if "workers" not in st.session_state:
st.session_state.workers=pd.DataFrame([
["W001","Mining","Driller","Day","Yes","Complete",3,8,1,0,2,2],
["W002","Processing","Plant Operator","Night","Yes","Complete",6,5,2,1,3,4],
["W003","Maintenance","Fitter","Day","No","Expired",8,3,4,2,4,5],
["W004","Mining","Operator","Night","Yes","Complete",4,7,1,0,2,3],
["W005","Engineering","Technician","Day","Yes","Complete",2,9,0,0,1,2],
["W006","Mining","Blaster","Night","No","Complete",7,4,3,1,4,5]
],columns=["worker_id","department","job_role","shift","ppe_compliant","training_status","fatigue_level","observations","near_misses","previous_incidents","likelihood","consequence"])

if "incidents" not in st.session_state:
st.session_state.incidents=pd.DataFrame([
["INC-001","2026-01-12","Mining","Equipment","High","Mechanical","Open"],
["INC-002","2026-02-08","Processing","Slip","Medium","Human error","Closed"],
["INC-003","2026-03-19","Mining","Ground control","Critical","Ground failure","Open"],
["INC-004","2026-04-07","Maintenance","Equipment","High","Mechanical","Closed"],
["INC-005","2026-05-22","Processing","Chemical","Medium","Procedure","Open"],
["INC-006","2026-06-15","Mining","Vehicle","Critical","Operator","Open"],
["INC-007","2026-07-03","Engineering","Electrical","Low","Electrical","Closed"],
["INC-008","2026-08-14","Mining","Fall","High","Human error","Open"]
],columns=["incident_id","date","department","incident_type","severity","cause","status"])

if "equipment" not in st.session_state:
st.session_state.equipment=pd.DataFrame([
["EQ-001","Drill Rig","Atlas","Mining",8210,78,5.2,91,"OK","OK","OK","Normal"],
["EQ-002","LHD","Sandvik","Mining",6450,91,8.4,83,"WARNING","OK","WARNING","Due"],
["EQ-003","Haul Truck","CAT","Mining",11200,96,11.1,76,"OK","WARNING","OK","Due"],
["EQ-004","Crusher","Metso","Processing",9340,73,4.8,94,"OK","OK","OK","Normal"],
["EQ-005","Conveyor","Fenner","Processing",7180,69,3.4,97,"OK","OK","OK","Normal"],
["EQ-006","Excavator","Komatsu","Mining",10250,101,13.2,71,"WARNING","WARNING","CRITICAL","Overdue"]
],columns=["equipment_id","equipment_type","manufacturer","department","operating_hours","temperature","vibration","availability","brake_status","tyre_status","engine_status","maintenance_status"])

if "alerts" not in st.session_state:
st.session_state.alerts=[
{"severity":"CRITICAL","category":"Equipment","message":"EQ-006 engine temperature is above critical threshold.","entity":"EQ-006"},
{"severity":"CRITICAL","category":"Safety","message":"Ground-control incident requires immediate review.","entity":"INC-003"},
{"severity":"WARNING","category":"Equipment","message":"EQ-003 tyre condition requires inspection.","entity":"EQ-003"},
{"severity":"WARNING","category":"Worker","message":"Several workers have elevated fatigue scores.","entity":"WORKFORCE"}
]

def role_name():
return st.session_state.role or "User"

def can_access(page):
permissions={
"Admin":{"Dashboard","My Data","Alerts","Worker Safety","Safety Incidents","Equipment","Maintenance","Risk Assessment","Data Analysis","Reports","Manage Users"},
"Safety Officer":{"Dashboard","My Data","Alerts","Worker Safety","Safety Incidents","Risk Assessment","Data Analysis","Reports"},
"Engineer":{"Dashboard","My Data","Alerts","Equipment","Risk Assessment","Data Analysis","Reports"},
"Maintenance":{"Dashboard","My Data","Alerts","Equipment","Maintenance","Data Analysis","Reports"},
"Manager":{"Dashboard","My Data","Alerts","Worker Safety","Safety Incidents","Equipment","Maintenance","Risk Assessment","Data Analysis","Reports"}
}
return page in permissions.get(role_name(),set())

def go_to(page):
if page!=st.session_state.page:
st.session_state.history.append(st.session_state.page)
st.session_state.page=page
st.rerun()

def go_back():
if st.session_state.history:
st.session_state.page=st.session_state.history.pop()
else:
st.session_state.page="Welcome"
st.rerun()

def home():
st.session_state.history=[]
st.session_state.page="Welcome"
st.rerun()

def sign_out():
st.session_state.clear()
st.rerun()

def header():
st.markdown(f""" <div class="app-header"> <div class="brand"> <div class="brand-mark">K</div> <div> <div class="brand-name">KHWEZI</div> <div class="brand-sub">MINING INTELLIGENCE</div> </div> </div> <div class="domain">{role_name().upper()} DOMAIN</div> </div>
""",unsafe_allow_html=True)
_,button=st.columns([8,1])
with button:
if st.button("SIGN OUT",key="global_sign_out",use_container_width=True):
sign_out()

def login():
st.markdown(""" <div class="welcome"> <div class="welcome-content"> <div class="kicker">KHWEZI MINING OPERATIONS</div> <div class="welcome-title">MINING<br><span>INTELLIGENCE.</span></div> <div class="welcome-text">One command centre for people, safety, equipment, incidents, maintenance and operational risk.</div> </div> </div>
""",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
*,centre,*=st.columns([1,1.2,1])
with centre:
st.markdown("<div class='kicker'>SECURE ACCESS</div>",unsafe_allow_html=True)
with st.form("login_form"):
username=st.text_input("Username",placeholder="Enter username")
password=st.text_input("Password",type="password",placeholder="Enter password")
submitted=st.form_submit_button("ENTER COMMAND CENTRE →",use_container_width=True)
if submitted:
if time.time()<st.session_state.locked_until:
st.error(f"Login locked. Try again in {int(st.session_state.locked_until-time.time())} seconds.")
return
account=USERS.get(username.strip().lower())
if account and password==account["password"]:
st.session_state.logged_in=True
st.session_state.role=account["role"]
st.session_state.page="Welcome"
st.session_state.history=[]
st.session_state.attempts=0
st.rerun()
else:
st.session_state.attempts+=1
if st.session_state.attempts>=3:
st.session_state.locked_until=time.time()+30
st.session_state.attempts=0
st.error("Too many failed attempts. Login locked for 30 seconds.")
else:
st.error(f"Invalid login. {3-st.session_state.attempts} attempt(s) remaining.")

def welcome_page():
st.markdown(f""" <div class="welcome"> <div class="welcome-content"> <div class="kicker">KHWEZI MINING OPERATIONS</div> <div class="welcome-title">WELCOME,<br><span>{role_name().upper()}.</span></div> <div class="welcome-text">Your operational workspace is ready. Choose where you want to go.</div> </div> </div>
""",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
left,right=st.columns(2,gap="large")
with left:
st.markdown("<div class='choice-small'>SEE THE BIG PICTURE</div>",unsafe_allow_html=True)
st.markdown('<div class="choice-button">',unsafe_allow_html=True)
if st.button("DASHBOARD\n\nMonitor the operation at a glance.",key="welcome_dashboard",use_container_width=True):
go_to("Dashboard")
st.markdown("</div>",unsafe_allow_html=True)
with right:
st.markdown("<div class='choice-small'>GO DEEPER</div>",unsafe_allow_html=True)
st.markdown('<div class="choice-button">',unsafe_allow_html=True)
if st.button("MY DATA\n\nExplore the tools and operational data.",key="welcome_data",use_container_width=True):
go_to("My Data")
st.markdown("</div>",unsafe_allow_html=True)

def controls():
left,middle,*=st.columns([1,1,6])
with left:
if st.button("← BACK",key=f"back*{st.session_state.page}",use_container_width=True):
go_back()
with middle:
if st.button("⌂ HOME",key=f"home_{st.session_state.page}",use_container_width=True):
home()
st.markdown(f"<div class='breadcrumb'>KHWEZI › {st.session_state.page.upper()}</div>",unsafe_allow_html=True)

def dashboard():
st.markdown("<div class='section-title'>Dashboard</div>",unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Live operational overview</div>",unsafe_allow_html=True)
workers=st.session_state.workers
incidents=st.session_state.incidents
equipment=st.session_state.equipment
alerts=st.session_state.alerts
ppe=round((workers["ppe_compliant"]=="Yes").mean()*100,1)
availability=round(equipment["availability"].mean(),1)
critical=sum(a["severity"]=="CRITICAL" for a in alerts)
c1,c2,c3,c4=st.columns(4)
c1.metric("WORKERS",len(workers))
c2.metric("PPE COMPLIANCE",f"{ppe}%")
c3.metric("EQUIPMENT AVAILABILITY",f"{availability}%")
c4.metric("CRITICAL ALERTS",critical)
left,right=st.columns(2)
with left:
monthly=incidents.assign(month=pd.to_datetime(incidents["date"]).dt.strftime("%b")).groupby("month").size().reset_index(name="incidents")
fig=px.line(monthly,x="month",y="incidents",markers=True,title="Safety incidents")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig,use_container_width=True)
with right:
condition=pd.DataFrame({"Condition":["Normal","Warning","Critical"],"Equipment":[sum(equipment["engine_status"]=="OK"),sum(equipment["engine_status"]=="WARNING"),sum(equipment["engine_status"]=="CRITICAL")]})
fig=px.bar(condition,x="Condition",y="Equipment",title="Equipment condition")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig,use_container_width=True)
st.subheader("Priority alerts")
for alert in alerts:
css="alert-critical" if alert["severity"]=="CRITICAL" else "alert-warning"
st.markdown(f"""<div class="alert-card {css}"><strong>{alert["severity"]}</strong><br><br>{alert["message"]}<br><span style="color:#777;font-size:.78rem;">{alert["category"]} · {alert["entity"]}</span></div>""",unsafe_allow_html=True)

def my_data():
st.markdown("<div class='section-title'>My Data</div>",unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Choose a section to go deeper into the operation.</div>",unsafe_allow_html=True)
modules=[
("Alerts","Warnings, critical conditions and operational exceptions."),
("Worker Safety","PPE, fatigue, near misses and workforce risk."),
("Safety Incidents","Record, investigate and analyse safety incidents."),
("Equipment","Equipment condition, readings and availability."),
("Maintenance","Service activity, maintenance status and readiness."),
("Risk Assessment","Likelihood, consequence and operational exposure."),
("Data Analysis","Turn operational data into useful decisions."),
("Reports","Create an operational report and export information.")
]
if role_name()=="Admin":
modules.append(("Manage Users","Control users, roles and system access."))
cols=st.columns(3)
for i,(title,description) in enumerate(modules):
with cols[i%3]:
st.markdown(f"""<div class="page-card"><div class="choice-small">KHWEZI MODULE</div><div class="page-card-title">{title}</div><div class="page-card-text">{description}</div></div>""",unsafe_allow_html=True)
if st.button(f"OPEN {title.upper()} →",key=f"module_{title}",use_container_width=True):
go_to(title)

def alerts_page():
st.markdown("<div class='section-title'>Alerts</div>",unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Operational conditions requiring attention.</div>",unsafe_allow_html=True)
severities=st.multiselect("Severity",["CRITICAL","WARNING"],default=["CRITICAL","WARNING"])
categories=sorted(set(a["category"] for a in st.session_state.alerts))
selected=st.multiselect("Category",categories,default=categories)
filtered=[a for a in st.session_state.alerts if a["severity"] in severities and a["category"] in selected]
st.write(f"{len(filtered)} active alert(s)")
for alert in filtered:
css="alert-critical" if alert["severity"]=="CRITICAL" else "alert-warning"
st.markdown(f"""<div class="alert-card {css}"><strong>{alert["severity"]}</strong><br><br>{alert["message"]}<br><span style="color:#777;">Category: {alert["category"]} · Entity: {alert["entity"]}</span></div>""",unsafe_allow_html=True)

def worker_safety():
st.markdown("<div class='section-title'>Worker Safety</div>",unsafe_allow_html=True)
workers=st.session_state.workers.copy()
workers["risk_score"]=workers["likelihood"]*workers["consequence"]
workers["risk_class"]=workers["risk_score"].apply(lambda x:"Critical" if x>=20 else "High" if x>=15 else "Medium" if x>=8 else "Low")
ppe=round((workers["ppe_compliant"]=="Yes").mean()*100,1)
high=sum(workers["risk_class"].isin(["High","Critical"]))
c1,c2,c3,c4=st.columns(4)
c1.metric("WORKERS",len(workers))
c2.metric("PPE COMPLIANCE",f"{ppe}%")
c3.metric("AVG FATIGUE",round(workers["fatigue_level"].mean(),1))
c4.metric("HIGH / CRITICAL RISK",high)
tab1,tab2,tab3=st.tabs(["WORKFORCE","RISK","ADD WORKER"])
with tab1:
departments=st.multiselect("Department",sorted(workers["department"].unique()))
filtered=workers if not departments else workers[workers["department"].isin(departments)]
st.dataframe(filtered,hide_index=True,use_container_width=True)
with tab2:
counts=workers["risk_class"].value_counts().reset_index()
counts.columns=["Risk class","Workers"]
st.plotly_chart(px.bar(counts,x="Risk class",y="Workers",title="Worker risk profile"),use_container_width=True)
st.dataframe(workers[workers["risk_class"].isin(["High","Critical"])],hide_index=True,use_container_width=True)
with tab3:
with st.form("add_worker"):
c1,c2,c3=st.columns(3)
worker_id=c1.text_input("Worker ID")
department=c2.selectbox("Department",["Mining","Processing","Maintenance","Engineering"])
job_role=c3.text_input("Job role")
c1,c2,c3=st.columns(3)
shift=c1.selectbox("Shift",["Day","Night"])
ppe_status=c2.selectbox("PPE compliant?",["Yes","No"])
training=c3.selectbox("Training status",["Complete","Expired","Pending"])
c1,c2,c3,c4=st.columns(4)
fatigue=c1.slider("Fatigue",1,10,3)
observations=c2.number_input("Observations",0,1000,0)
near_misses=c3.number_input("Near misses",0,1000,0)
previous=c4.number_input("Previous incidents",0,1000,0)
c1,c2=st.columns(2)
likelihood=c1.slider("Likelihood",1,5,2)
consequence=c2.slider("Consequence",1,5,2)
submitted=st.form_submit_button("ADD WORKER",use_container_width=True)
if submitted:
if not worker_id.strip() or not job_role.strip():
st.error("Worker ID and job role are required.")
elif worker_id.strip().upper() in workers["worker_id"].values:
st.error("That Worker ID already exists.")
else:
new=pd.DataFrame([[worker_id.strip().upper(),department,job_role.strip(),shift,ppe_status,training,fatigue,observations,near_misses,previous,likelihood,consequence]],columns=workers.columns[:-2].tolist()+["likelihood","consequence"])
st.session_state.workers=pd.concat([st.session_state.workers,new],ignore_index=True)
st.success(f"Worker {worker_id.upper()} added successfully.")

def safety_incidents():
st.markdown("<div class='section-title'>Safety Incidents</div>",unsafe_allow_html=True)
incidents=st.session_state.incidents.copy()
incidents["date"]=pd.to_datetime(incidents["date"])
c1,c2,c3=st.columns(3)
c1.metric("TOTAL INCIDENTS",len(incidents))
c2.metric("CRITICAL",sum(incidents["severity"]=="Critical"))
c3.metric("OPEN CASES",sum(incidents["status"]=="Open"))
tab1,tab2,tab3=st.tabs(["INCIDENT REGISTER","TRENDS","ADD INCIDENT"])
with tab1:
severities=st.multiselect("Severity",sorted(incidents["severity"].unique()))
filtered=incidents if not severities else incidents[incidents["severity"].isin(severities)]
st.dataframe(filtered,hide_index=True,use_container_width=True)
st.download_button("DOWNLOAD INCIDENT DATA",filtered.to_csv(index=False),"khwezi_incidents.csv","text/csv",use_container_width=True)
with tab2:
monthly=incidents.assign(month=incidents["date"].dt.strftime("%Y-%m")).groupby("month").size().reset_index(name="incidents")
st.plotly_chart(px.line(monthly,x="month",y="incidents",markers=True,title="Monthly incident trend"),use_container_width=True)
with tab3:
with st.form("incident_form"):
c1,c2,c3=st.columns(3)
incident_id=c1.text_input("Incident ID",value=f"INC-{len(incidents)+1:03d}")
incident_date=c2.date_input("Date",date.today())
department=c3.selectbox("Department",["Mining","Processing","Maintenance","Engineering"])
c1,c2,c3=st.columns(3)
incident_type=c1.selectbox("Incident type",["Equipment","Slip","Ground control","Vehicle","Chemical","Electrical","Fall"])
severity=c2.selectbox("Severity",["Low","Medium","High","Critical"])
cause=c3.selectbox("Cause",["Human error","Mechanical","Ground failure","Procedure","Operator","Electrical"])
status=st.selectbox("Status",["Open","Closed"])
submitted=st.form_submit_button("RECORD INCIDENT",use_container_width=True)
if submitted:
new=pd.DataFrame([[incident_id,str(incident_date),department,incident_type,severity,cause,status]],columns=st.session_state.incidents.columns)
st.session_state.incidents=pd.concat([st.session_state.incidents,new],ignore_index=True)
st.success(f"{incident_id} recorded successfully.")

def equipment_page():
st.markdown("<div class='section-title'>Equipment</div>",unsafe_allow_html=True)
equipment=st.session_state.equipment.copy()
c1,c2,c3=st.columns(3)
c1.metric("FLEET AVAILABILITY",f"{round(equipment['availability'].mean(),1)}%")
c2.metric("CRITICAL MACHINES",sum(equipment["engine_status"]=="CRITICAL"))
c3.metric("MAINTENANCE DUE",sum(equipment["maintenance_status"].isin(["Due","Overdue"])))
tab1,tab2,tab3=st.tabs(["FLEET","CONDITION MONITOR","ADD EQUIPMENT"])
with tab1:
types=st.multiselect("Equipment type",sorted(equipment["equipment_type"].unique()))
filtered=equipment if not types else equipment[equipment["equipment_type"].isin(types)]
st.dataframe(filtered,hide_index=True,use_container_width=True)
with tab2:
selected=st.selectbox("Select equipment",equipment["equipment_id"].tolist())
row=equipment[equipment["equipment_id"]==selected].iloc[0]
c1,c2,c3,c4=st.columns(4)
c1.metric("TEMPERATURE",f"{row['temperature']} °C")
c2.metric("VIBRATION",f"{row['vibration']} mm/s")
c3.metric("AVAILABILITY",f"{row['availability']}%")
c4.metric("OPERATING HOURS",f"{row['operating_hours']:,}")
st.dataframe(pd.DataFrame({"System":["Brakes","Tyres","Engine","Maintenance"],"Status":[row["brake_status"],row["tyre_status"],row["engine_status"],row["maintenance_status"]]}),hide_index=True,use_container_width=True)
with tab3:
with st.form("equipment_form"):
c1,c2,c3=st.columns(3)
equipment_id=c1.text_input("Equipment ID")
equipment_type=c2.selectbox("Equipment type",["Drill Rig","LHD","Haul Truck","Crusher","Conveyor","Excavator"])
manufacturer=c3.text_input("Manufacturer")
c1,c2,c3=st.columns(3)
department=c1.selectbox("Department",["Mining","Processing","Maintenance"])
operating_hours=c2.number_input("Operating hours",0,100000,0)
availability=c3.number_input("Availability %",0.0,100.0,95.0)
submitted=st.form_submit_button("ADD EQUIPMENT",use_container_width=True)
if submitted:
if not equipment_id.strip():
st.error("Equipment ID is required.")
else:
new=pd.DataFrame([[equipment_id.upper(),equipment_type,manufacturer,department,operating_hours,70,3.0,availability,"OK","OK","OK","Normal"]],columns=equipment.columns)
st.session_state.equipment=pd.concat([st.session_state.equipment,new],ignore_index=True)
st.success(f"{equipment_id.upper()} added successfully.")

def maintenance():
st.markdown("<div class='section-title'>Maintenance</div>",unsafe_allow_html=True)
equipment=st.session_state.equipment
c1,c2,c3=st.columns(3)
c1.metric("NORMAL",sum(equipment["maintenance_status"]=="Normal"))
c2.metric("DUE",sum(equipment["maintenance_status"]=="Due"))
c3.metric("OVERDUE",sum(equipment["maintenance_status"]=="Overdue"))
st.dataframe(equipment[["equipment_id","equipment_type","operating_hours","maintenance_status","availability"]],hide_index=True,use_container_width=True)
st.subheader("Log service")
with st.form("service_form"):
selected=st.selectbox("Equipment",equipment["equipment_id"])
service_type=st.selectbox("Service type",["Routine service","Inspection","Repair","Major service"])
notes=st.text_area("Service notes")
submitted=st.form_submit_button("LOG SERVICE",use_container_width=True)
if submitted:
index=st.session_state.equipment[st.session_state.equipment["equipment_id"]==selected].index
if len(index):
st.session_state.equipment.loc[index,"maintenance_status"]="Normal"
st.success(f"{selected} service logged: {service_type}.")
if notes: st.info(notes)

def risk_assessment():
st.markdown("<div class='section-title'>Risk Assessment</div>",unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Likelihood × consequence = risk score.</div>",unsafe_allow_html=True)
c1,c2=st.columns(2)
likelihood=c1.slider("Likelihood",1,5,3)
consequence=c2.slider("Consequence",1,5,3)
score=likelihood*consequence
level="CRITICAL" if score>=20 else "HIGH" if score>=15 else "MEDIUM" if score>=8 else "LOW"
st.markdown(f"""<div style="background:#111417;color:white;border-radius:22px;padding:30px;text-align:center;margin:20px 0;"><div style="color:#F2A900;font-size:.7rem;letter-spacing:.2em;font-weight:900;">RISK RESULT</div><div style="font-family:'Barlow Condensed';font-size:4rem;font-weight:900;">{score}</div><div style="font-size:1.2rem;font-weight:900;">{level}</div></div>""",unsafe_allow_html=True)
matrix=[]
for l in range(1,6):
row=[]
for c in range(1,6):
s=l*c
row.append(f"{s} {'CRITICAL' if s>=20 else 'HIGH' if s>=15 else 'MEDIUM' if s>=8 else 'LOW'}")
matrix.append(row)
st.dataframe(pd.DataFrame(matrix,index=[f"Likelihood {i}" for i in range(1,6)],columns=[f"Consequence {i}" for i in range(1,6)]),use_container_width=True)

def data_analysis():
st.markdown("<div class='section-title'>Data Analysis</div>",unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Turn operational information into decisions.</div>",unsafe_allow_html=True)
question=st.selectbox("Choose a business question",[
"Which equipment has the lowest availability?",
"Which department has the most incidents?",
"Which workers have the highest risk?",
"What is the current PPE compliance?",
"Which machines require maintenance?"
])
equipment=st.session_state.equipment
incidents=st.session_state.incidents
workers=st.session_state.workers
if question=="Which equipment has the lowest availability?":
result=equipment.sort_values("availability")[["equipment_id","equipment_type","availability"]]
st.dataframe(result,hide_index=True,use_container_width=True)
st.plotly_chart(px.bar(result,x="equipment_id",y="availability",title="Equipment availability"),use_container_width=True)
elif question=="Which department has the most incidents?":
result=incidents["department"].value_counts().reset_index()
result.columns=["Department","Incidents"]
st.dataframe(result,hide_index=True,use_container_width=True)
st.plotly_chart(px.bar(result,x="Department",y="Incidents",title="Incidents by department"),use_container_width=True)
elif question=="Which workers have the highest risk?":
result=workers.copy()
result["Risk score"]=result["likelihood"]*result["consequence"]
result=result.sort_values("Risk score",ascending=False)
st.dataframe(result[["worker_id","department","job_role","Risk score"]],hide_index=True,use_container_width=True)
elif question=="What is the current PPE compliance?":
st.metric("CURRENT PPE COMPLIANCE",f"{round((workers['ppe_compliant']=='Yes').mean()*100,1)}%")
else:
st.dataframe(equipment[equipment["maintenance_status"].isin(["Due","Overdue"])],hide_index=True,use_container_width=True)

def reports():
st.markdown("<div class='section-title'>Reports</div>",unsafe_allow_html=True)
workers=st.session_state.workers
incidents=st.session_state.incidents
equipment=st.session_state.equipment
report=f"""KHWEZI MINING
HEALTH, SAFETY AND EQUIPMENT REPORT

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

DOMAIN
{role_name()}

WORKFORCE
Total workers: {len(workers)}
PPE compliance: {round((workers['ppe_compliant']=='Yes').mean()*100,1)}%

SAFETY
Total incidents: {len(incidents)}
Critical incidents: {sum(incidents['severity']=='Critical')}
Open incidents: {sum(incidents['status']=='Open')}

EQUIPMENT
Fleet availability: {round(equipment['availability'].mean(),1)}%
Critical equipment: {sum(equipment['engine_status']=='CRITICAL')}
Maintenance due/overdue: {sum(equipment['maintenance_status'].isin(['Due','Overdue']))}

KHWEZI MINING
Safer people. Smarter equipment. Better decisions.
"""
st.text_area("Operational report",report,height=430)
st.download_button("DOWNLOAD REPORT",report,"khwezi_mining_report.txt","text/plain",use_container_width=True)

def manage_users():
st.markdown("<div class='section-title'>Manage Users</div>",unsafe_allow_html=True)
if role_name()!="Admin":
st.error("Only Admin can manage users.")
return
data=pd.DataFrame([{"Username":u,"Role":d,"Status":"Active"} for u,d in USERS.items()])
st.dataframe(data,hide_index=True,use_container_width=True)
with st.form("user_form"):
username=st.text_input("Username")
password=st.text_input("Password",type="password")
role=st.selectbox("Role",["Admin","Safety Officer","Engineer","Maintenance","Manager"])
submitted=st.form_submit_button("ADD USER",use_container_width=True)
if submitted:
username=username.strip().lower()
if not username or not password:
st.error("Username and password are required.")
elif username in USERS:
st.error("That username already exists.")
else:
USERS[username]={"password":password,"role":role}
st.success(f"{username} added as {role}.")

PAGES={
"Dashboard":dashboard,
"My Data":my_data,
"Alerts":alerts_page,
"Worker Safety":worker_safety,
"Safety Incidents":safety_incidents,
"Equipment":equipment_page,
"Maintenance":maintenance,
"Risk Assessment":risk_assessment,
"Data Analysis":data_analysis,
"Reports":reports,
"Manage Users":manage_users
}

def main():
if not st.session_state.logged_in:
login()
return
header()
current=st.session_state.page
if current!="Welcome":
controls()
if current=="Welcome":
welcome_page()
elif current in PAGES:
if can_access(current):
PAGES[current]()
else:
st.error("This section is not available for your domain.")
home()
else:
home()

if **name**=="**main**":
main()
