import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Khwezi Mining", page_icon="K", layout="wide", initial_sidebar_state="collapsed")

if "logged_in" not in st.session_state:
st.session_state.logged_in = False
if "role" not in st.session_state:
st.session_state.role = ""
if "page" not in st.session_state:
st.session_state.page = "Welcome"
if "workers" not in st.session_state:
st.session_state.workers = pd.DataFrame([
["WK001","Thabo","Mokoena","Production","Active",96,2,"Low","Day"],
["WK002","Lerato","Molefe","Engineering","Active",91,1,"Low","Day"],
["WK003","Kagiso","Dube","Maintenance","Active",78,4,"Medium","Night"],
["WK004","Naledi","Maseko","Safety","Active",98,0,"Low","Day"],
["WK005","Mpho","Nkosi","Production","Active",84,3,"Medium","Night"]
], columns=["ID","First Name","Surname","Department","Status","PPE %","Near Misses","Risk","Shift"])
if "incidents" not in st.session_state:
st.session_state.incidents = pd.DataFrame([
["INC001","2026-09-28","Production","Slip / Fall","Minor","Open"],
["INC002","2026-09-30","Maintenance","Equipment Contact","Moderate","Investigating"],
["INC003","2026-10-02","Engineering","Electrical","Serious","Open"],
["INC004","2026-10-04","Production","Near Miss","Minor","Closed"]
], columns=["ID","Date","Department","Type","Severity","Status"])
if "equipment" not in st.session_state:
st.session_state.equipment = pd.DataFrame([
["EQ001","Continuous Miner 01","Continuous Miner","Production","Operational",92,78,"2026-10-18"],
["EQ002","LHD 04","Load Haul Dump","Production","Warning",76,91,"2026-10-11"],
["EQ003","Roof Bolter 02","Roof Bolter","Development","Operational",95,64,"2026-10-22"],
["EQ004","Drill Rig 01","Drill Rig","Development","Critical",61,97,"2026-10-08"],
["EQ005","LHD 07","Load Haul Dump","Production","Operational",89,71,"2026-10-15"]
], columns=["ID","Equipment","Type","Department","Condition","Availability %","Engine Hours","Next Service"])
if "maintenance" not in st.session_state:
st.session_state.maintenance = pd.DataFrame([
["M001","EQ001","2026-09-25","Routine Service","Completed","Team A"],
["M002","EQ002","2026-09-29","Hydraulic Inspection","Completed","Team B"],
["M003","EQ004","2026-10-03","Brake Inspection","Overdue","Team A"],
["M004","EQ003","2026-10-05","Lubrication","Completed","Team C"]
], columns=["ID","Equipment ID","Date","Type","Status","Technician"])
if "alerts" not in st.session_state:
st.session_state.alerts = [
{"title":"Drill Rig 01 requires attention","severity":"Critical","category":"Equipment","message":"Condition score is below the safe operating threshold.","time":"08 min ago"},
{"title":"Night shift fatigue risk detected","severity":"High","category":"Worker Safety","message":"Fatigue indicators require supervisor review.","time":"21 min ago"},
{"title":"Brake inspection overdue","severity":"High","category":"Maintenance","message":"EQ004 has an overdue brake inspection.","time":"43 min ago"},
{"title":"Near miss trend increasing","severity":"Medium","category":"Safety","message":"Near-miss reports increased over the current period.","time":"1 hr ago"}
]

USERS = {
"safety":{"password":"Safety@123","role":"Safety Officer"},
"admin":{"password":"Admin@123","role":"Admin"},
"engineer":{"password":"Mining@123","role":"Engineer"},
"maint":{"password":"Maint@123","role":"Maintenance"},
"manager":{"password":"Manager@123","role":"Manager"}
}

ROLE_ACCESS = {
"Safety Officer":["Alerts","Worker Safety","Safety Incidents","Risk Assessment","Reports"],
"Admin":["Alerts","Worker Safety","Safety Incidents","Equipment","Maintenance","Risk Assessment","Data Analysis","Reports","Manage Users"],
"Engineer":["Alerts","Equipment","Maintenance","Risk Assessment","Data Analysis","Reports"],
"Maintenance":["Alerts","Equipment","Maintenance","Reports"],
"Manager":["Alerts","Worker Safety","Safety Incidents","Equipment","Maintenance","Risk Assessment","Data Analysis","Reports"],
}

CSS = """

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:#07110d;color:#edf7f1}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1400px;padding:1.2rem 3rem 3rem}
section[data-testid="stSidebar"]{display:none}
h1,h2,h3{font-family:"Space Grotesk",sans-serif}
.hero{min-height:74vh;border-radius:30px;padding:55px;background:linear-gradient(90deg,rgba(3,12,8,.95),rgba(3,12,8,.65),rgba(3,12,8,.18)),url("https://images.unsplash.com/photo-1513828583688-c52646db42da?auto=format&fit=crop&w=1800&q=85") center/cover;display:flex;flex-direction:column;justify-content:center;box-shadow:0 25px 80px rgba(0,0,0,.35)}
.brand{font-weight:800;letter-spacing:4px;font-size:14px;color:#8ff0b3}
.hero h1{font-size:clamp(42px,6vw,78px);line-height:.98;margin:15px 0;max-width:850px}
.hero p{font-size:18px;color:#c9d9d0;max-width:720px;line-height:1.7}
.topbar{background:rgba(10,27,19,.96);border:1px solid rgba(143,240,179,.15);border-radius:20px;padding:13px 18px;margin-bottom:22px;display:flex;align-items:center;justify-content:space-between}
.topbrand{font-weight:800;letter-spacing:2px}
.pill{background:#163d2a;color:#8ff0b3;border-radius:999px;padding:7px 12px;font-size:12px;font-weight:700}
.muted{color:#8fa59a}
.card{background:#0d2117;border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:24px;height:100%;box-shadow:0 12px 35px rgba(0,0,0,.14)}
.card h3{margin-top:0}
.choice button{height:190px!important;text-align:left!important;border-radius:26px!important;border:1px solid rgba(143,240,179,.18)!important;background:linear-gradient(145deg,#102b1d,#0b1d14)!important;color:#fff!important;font-size:27px!important;font-weight:800!important;box-shadow:0 18px 50px rgba(0,0,0,.2)!important}
.choice button:hover{border-color:#8ff0b3!important;transform:translateY(-2px)}
.metric{background:#0d2117;border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:20px}
.metric .value{font-family:"Space Grotesk";font-size:34px;font-weight:700}
.metric .label{font-size:13px;color:#91a99c}
.section-title{font-size:28px;font-weight:800;margin:8px 0 18px}
.notice{padding:18px 20px;border-radius:16px;background:#0e2418;border-left:4px solid #8ff0b3;margin-bottom:12px}
.notice.critical{border-left-color:#ff5c5c}.notice.high{border-left-color:#ffae52}.notice.medium{border-left-color:#ffd35c}
.backrow{display:flex;gap:10px;margin:8px 0 22px}
div[data-testid="stButton"] button{border-radius:12px}
.login-wrap{max-width:500px;margin:8vh auto}
.small{font-size:12px}
</style>

"""

st.markdown(CSS, unsafe_allow_html=True)

def logout():
st.session_state.logged_in = False
st.session_state.role = ""
st.session_state.page = "Welcome"
st.rerun()

def go(page):
st.session_state.page = page
st.rerun()

def header():
role = st.session_state.role
page = st.session_state.page
st.markdown(f'<div class="topbar"><div class="topbrand">KHWEZI <span class="muted">MINING INTELLIGENCE</span></div><div style="display:flex;align-items:center;gap:12px"><span class="pill">{role.upper()} DOMAIN</span><span class="muted">{page}</span></div></div>', unsafe_allow_html=True)
c1,c2 = st.columns([8,1])
with c2:
if st.button("SIGN OUT", key="global_logout"):
logout()

def metrics():
workers = st.session_state.workers
eq = st.session_state.equipment
inc = st.session_state.incidents
available = round(eq["Availability %"].mean())
ppe = round(workers["PPE %"].mean())
open_inc = int((inc["Status"]!="Closed").sum())
return len(workers), available, ppe, open_inc

def welcome():
role = st.session_state.role
st.markdown(f'<div class="hero"><div class="brand">KHWEZI MINING • DIGITAL CONTROL ROOM</div><h1>Welcome {role}</h1><p>One place to monitor people, equipment, safety and operational performance.</p></div>', unsafe_allow_html=True)
st.write("")
c1,c2 = st.columns(2)
with c1:
st.markdown('<div class="choice">',unsafe_allow_html=True)
if st.button("DASHBOARD\n\nView the mine at a glance",key="welcome_dashboard",use_container_width=True):
go("Dashboard")
st.markdown('</div>',unsafe_allow_html=True)
with c2:
st.markdown('<div class="choice">',unsafe_allow_html=True)
if st.button("MY DATA\n\nOpen your role-specific tools",key="welcome_data",use_container_width=True):
go("My Data")
st.markdown('</div>',unsafe_allow_html=True)

def dashboard():
header()
st.markdown('<div class="section-title">Operational Dashboard</div>',unsafe_allow_html=True)
workers,available,ppe,open_inc = metrics()
a,b,c,d = st.columns(4)
for col,label,value in [(a,"ACTIVE WORKERS",workers),(b,"EQUIPMENT AVAILABILITY",f"{available}%"),(c,"PPE COMPLIANCE",f"{ppe}%"),(d,"OPEN INCIDENTS",open_inc)]:
with col:
st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div></div>',unsafe_allow_html=True)
st.write("")
left,right = st.columns([1.4,1])
with left:
st.markdown("### Incident Trend")
inc = st.session_state.incidents.copy()
inc["Date"] = pd.to_datetime(inc["Date"])
trend = inc.groupby("Date").size().reset_index(name="Incidents")
fig = px.line(trend,x="Date",y="Incidents",markers=True,template="plotly_dark")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(l=10,r=10,t=10,b=10),font_color="#dcebe3")
st.plotly_chart(fig,use_container_width=True)
with right:
st.markdown("### Live Alerts")
for alert in st.session_state.alerts[:4]:
cls=alert["severity"].lower()
st.markdown(f'<div class="notice {cls}"><b>{alert["title"]}</b><br><span class="muted">{alert["message"]}</span><br><small>{alert["time"]} • {alert["severity"]}</small></div>',unsafe_allow_html=True)

def my_data():
header()
st.markdown('<div class="section-title">My Data</div>',unsafe_allow_html=True)
st.caption("Choose a tool to go deeper into the mining control room.")
pages = ROLE_ACCESS.get(st.session_state.role,[])
cols = st.columns(3)
for i,page in enumerate(pages):
with cols[i%3]:
if st.button(page.upper()+"\n\nOpen "+page,key="data_"+page,use_container_width=True):
go(page)

def back_home():
c1,c2,c3 = st.columns([1,1,8])
with c1:
if st.button("← BACK",key="back"):
go("My Data")
with c2:
if st.button("⌂ HOME",key="home"):
go("Welcome")

def alerts_page():
header()
back_home()
st.markdown('<div class="section-title">Alerts</div>',unsafe_allow_html=True)
sev=st.selectbox("Severity",["All","Critical","High","Medium","Low"])
cat=st.selectbox("Category",["All"]+sorted(set(a["category"] for a in st.session_state.alerts)))
items=[a for a in st.session_state.alerts if (sev=="All" or a["severity"]==sev) and (cat=="All" or a["category"]==cat)]
for a in items:
st.markdown(f'<div class="notice {a["severity"].lower()}"><b>{a["title"]}</b><br>{a["message"]}<br><small>{a["category"]} • {a["severity"]} • {a["time"]}</small></div>',unsafe_allow_html=True)

def worker_safety():
header()
back_home()
st.markdown('<div class="section-title">Worker Safety</div>',unsafe_allow_html=True)
workers=st.session_state.workers
a,b,c=st.columns(3)
with a:
st.metric("Workers",len(workers))
with b:
st.metric("Average PPE",f'{workers["PPE %"].mean():.0f}%')
with c:
st.metric("Medium/High Risk",int((workers["Risk"].isin(["Medium","High"])).sum()))
tab1,tab2=st.tabs(["WORKER REGISTER","ADD WORKER"])
with tab1:
st.dataframe(workers,use_container_width=True,hide_index=True)
with tab2:
with st.form("worker_form"):
c1,c2,c3=st.columns(3)
first=c1.text_input("First Name")
surname=c2.text_input("Surname")
dept=c3.selectbox("Department",["Production","Engineering","Maintenance","Safety","Management"])
c4,c5,c6=st.columns(3)
ppe=c4.slider("PPE Compliance %",0,100,90)
near=c5.number_input("Near Misses",0,20,0)
shift=c6.selectbox("Shift",["Day","Night"])
submitted=st.form_submit_button("ADD WORKER")
if submitted:
if first.strip() and surname.strip():
new_id=f"WK{len(workers)+1:03d}"
risk="Low" if ppe>=90 else ("Medium" if ppe>=75 else "High")
row=pd.DataFrame([[new_id,first.strip(),surname.strip(),dept,"Active",ppe,near,risk,shift]],columns=workers.columns)
st.session_state.workers=pd.concat([workers,row],ignore_index=True)
st.success("Worker added.")
st.rerun()
else:
st.error("Enter a first name and surname.")

def incidents_page():
header()
back_home()
st.markdown('<div class="section-title">Safety Incidents</div>',unsafe_allow_html=True)
inc=st.session_state.incidents
c1,c2,c3=st.columns(3)
sev=c1.selectbox("Severity",["All"]+sorted(inc["Severity"].unique()))
status=c2.selectbox("Status",["All"]+sorted(inc["Status"].unique()))
dept=c3.selectbox("Department",["All"]+sorted(inc["Department"].unique()))
filtered=inc.copy()
if sev!="All":
filtered=filtered[filtered["Severity"]==sev]
if status!="All":
filtered=filtered[filtered["Status"]==status]
if dept!="All":
filtered=filtered[filtered["Department"]==dept]
st.dataframe(filtered,use_container_width=True,hide_index=True)
st.download_button("DOWNLOAD INCIDENT CSV",filtered.to_csv(index=False).encode(),"incidents.csv","text/csv")
with st.expander("REPORT NEW INCIDENT"):
with st.form("incident_form"):
c1,c2,c3=st.columns(3)
typ=c1.selectbox("Type",["Slip / Fall","Equipment Contact","Electrical","Near Miss","Fire","Other"])
severity=c2.selectbox("Severity",["Minor","Moderate","Serious","Critical"])
department=c3.selectbox("Department",["Production","Engineering","Maintenance","Safety"])
desc=st.text_area("Description")
if st.form_submit_button("SUBMIT INCIDENT"):
new_id=f"INC{len(inc)+1:03d}"
row=pd.DataFrame([[new_id,str(date.today()),department,typ,severity,"Open"]],columns=inc.columns)
st.session_state.incidents=pd.concat([inc,row],ignore_index=True)
st.success("Incident recorded.")
st.rerun()

def equipment_page():
header()
back_home()
st.markdown('<div class="section-title">Equipment</div>',unsafe_allow_html=True)
eq=st.session_state.equipment
c1,c2,c3=st.columns(3)
c1.metric("Fleet Size",len(eq))
c2.metric("Average Availability",f'{eq["Availability %"].mean():.0f}%')
c3.metric("Needs Attention",int((eq["Condition"].isin(["Warning","Critical"])).sum()))
st.dataframe(eq,use_container_width=True,hide_index=True)
with st.expander("ADD EQUIPMENT"):
with st.form("equipment_form"):
c1,c2,c3=st.columns(3)
name=c1.text_input("Equipment Name")
typ=c2.selectbox("Type",["Continuous Miner","LHD","Roof Bolter","Drill Rig","Haul Truck"])
dept=c3.selectbox("Department",["Production","Development","Engineering","Maintenance"])
c4,c5=st.columns(2)
availability=c4.slider("Availability %",0,100,90)
hours=c5.number_input("Engine Hours",0,50000,1000)
if st.form_submit_button("ADD EQUIPMENT"):
if name.strip():
new_id=f"EQ{len(eq)+1:03d}"
condition="Operational" if availability>=85 else ("Warning" if availability>=70 else "Critical")
row=pd.DataFrame([[new_id,name.strip(),typ,dept,condition,availability,hours,str(date.today()+timedelta(days=14))]],columns=eq.columns)
st.session_state.equipment=pd.concat([eq,row],ignore_index=True)
st.success("Equipment added.")
st.rerun()

def maintenance_page():
header()
back_home()
st.markdown('<div class="section-title">Maintenance</div>',unsafe_allow_html=True)
m=st.session_state.maintenance
a,b,c=st.columns(3)
a.metric("Completed",int((m["Status"]=="Completed").sum()))
b.metric("Overdue",int((m["Status"]=="Overdue").sum()))
c.metric("Total Records",len(m))
st.dataframe(m,use_container_width=True,hide_index=True)
with st.expander("LOG SERVICE"):
with st.form("maintenance_form"):
eqid=st.selectbox("Equipment",st.session_state.equipment["ID"].tolist())
typ=st.selectbox("Service Type",["Routine Service","Inspection","Repair","Lubrication","Brake Inspection","Hydraulic Inspection"])
technician=st.text_input("Technician / Team")
if st.form_submit_button("SAVE SERVICE"):
new_id=f"M{len(m)+1:03d}"
row=pd.DataFrame([[new_id,eqid,str(date.today()),typ,"Completed",technician or "Maintenance Team"]],columns=m.columns)
st.session_state.maintenance=pd.concat([m,row],ignore_index=True)
st.success("Maintenance logged.")
st.rerun()

def risk_page():
header()
back_home()
st.markdown('<div class="section-title">Risk Assessment</div>',unsafe_allow_html=True)
c1,c2=st.columns(2)
with c1:
likelihood=st.slider("Likelihood",1,5,3)
consequence=st.slider("Consequence",1,5,3)
score=likelihood*consequence
level="Low" if score<=4 else ("Medium" if score<=9 else ("High" if score<=16 else "Critical"))
st.markdown(f'<div class="metric"><div class="label">RISK SCORE</div><div class="value">{score} • {level}</div></div>',unsafe_allow_html=True)
data=[]
for l in range(1,6):
for c in range(1,6):
s=l*c
lv="Low" if s<=4 else ("Medium" if s<=9 else ("High" if s<=16 else "Critical"))
data.append([l,c,s,lv])
st.dataframe(pd.DataFrame(data,columns=["Likelihood","Consequence","Score","Level"]).pivot(index="Likelihood",columns="Consequence",values="Score"),use_container_width=True)

def analysis_page():
header()
back_home()
st.markdown('<div class="section-title">Data Analysis</div>',unsafe_allow_html=True)
topic=st.selectbox("Topic",["Safety","Equipment","Workers","Maintenance"])
if topic=="Safety":
st.metric("Incident Count",len(st.session_state.incidents))
st.bar_chart(st.session_state.incidents["Severity"].value_counts())
elif topic=="Equipment":
st.metric("Fleet Availability",f'{st.session_state.equipment["Availability %"].mean():.1f}%')
st.bar_chart(st.session_state.equipment.set_index("Equipment")["Availability %"])
elif topic=="Workers":
st.metric("Average PPE Compliance",f'{st.session_state.workers["PPE %"].mean():.1f}%')
st.bar_chart(st.session_state.workers.set_index("ID")["PPE %"])
else:
st.metric("Maintenance Records",len(st.session_state.maintenance))
st.bar_chart(st.session_state.maintenance["Status"].value_counts())

def reports_page():
header()
back_home()
st.markdown('<div class="section-title">Reports</div>',unsafe_allow_html=True)
workers,available,ppe,open_inc=metrics()
report=f"""KHWEZI MINING OPERATIONAL REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

WORKFORCE
Active workers: {workers}
Average PPE compliance: {ppe}%

EQUIPMENT
Average availability: {available}%

SAFETY
Open incidents: {open_inc}
Total incidents: {len(st.session_state.incidents)}

MAINTENANCE
Overdue records: {int((st.session_state.maintenance["Status"]=="Overdue").sum())}

This report provides a snapshot of current mining safety and equipment conditions.
"""
st.text_area("REPORT",report,height=400)
st.download_button("DOWNLOAD REPORT",report.encode(),"khwezi_report.txt","text/plain")

def users_page():
header()
back_home()
st.markdown('<div class="section-title">Manage Users</div>',unsafe_allow_html=True)
data=pd.DataFrame([{"Username":u,"Role":v,"Status":"Active"} for u,v in USERS.items()])
st.dataframe(data,use_container_width=True,hide_index=True)
st.info("Demo access is provided for the school competition prototype.")

def login():
st.markdown('<div class="login-wrap">',unsafe_allow_html=True)
st.markdown('<div class="brand">KHWEZI MINING</div>',unsafe_allow_html=True)
st.title("Mining Intelligence")
st.write("Sign in to enter the digital control room.")
with st.form("login_form"):
username=st.text_input("USERNAME")
password=st.text_input("PASSWORD",type="password")
submit=st.form_submit_button("SIGN IN",use_container_width=True)
if submit:
account=USERS.get(username.strip().lower())
if account and password==account["password"]:
st.session_state.logged_in=True
st.session_state.role=account["role"]
st.session_state.page="Welcome"
st.rerun()
else:
st.error("Invalid username or password.")
st.caption("Demo accounts: safety / Safety@123 • admin / Admin@123 • engineer / Mining@123 • maint / Maint@123 • manager / Manager@123")
st.markdown('</div>',unsafe_allow_html=True)

def app():
if not st.session_state.logged_in:
login()
return
page=st.session_state.page
if page=="Welcome":
welcome()
elif page=="Dashboard":
dashboard()
elif page=="My Data":
my_data()
elif page=="Alerts":
alerts_page()
elif page=="Worker Safety":
worker_safety()
elif page=="Safety Incidents":
incidents_page()
elif page=="Equipment":
equipment_page()
elif page=="Maintenance":
maintenance_page()
elif page=="Risk Assessment":
risk_page()
elif page=="Data Analysis":
analysis_page()
elif page=="Reports":
reports_page()
elif page=="Manage Users":
users_page()
else:
go("Welcome")

app()
