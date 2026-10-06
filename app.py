
import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px


# ============================================================
# KHWЕZI MINING
# HEALTH, SAFETY & EQUIPMENT MONITORING APP
# SINGLE-FILE DEMO — PASTE AND RUN DIRECTLY
# ============================================================

st.set_page_config(
    page_title="Khwezi Mining",
    page_icon="⛏",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# THEME
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --black: #0d0f11;
    --black2: #15181c;
    --panel: #1d2228;
    --panel2: #252b31;
    --amber: #f2a900;
    --gold: #ffc857;
    --cream: #f4f1e9;
    --muted: #89929b;
    --white: #ffffff;
    --green: #4fbd7a;
    --red: #e05252;
    --orange: #ed8d22;
}

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background: var(--cream);
}

.block-container {
    padding: 0 2.2rem 3rem;
    max-width: 1500px;
}

h1, h2, h3, h4 {
    font-family: "Barlow Condensed", sans-serif !important;
}

h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
}

h3 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}


/* ============================================================
   HIDE STREAMLIT DEFAULT UI
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ============================================================
   TOP APP BAR
   ============================================================ */

.appbar {
    background: rgba(13,15,17,.98);
    color: white;
    min-height: 70px;
    margin: 0 -2.2rem 0;
    padding: 12px 25px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid var(--amber);
    position: relative;
    z-index: 20;
}

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-mark {
    width: 40px;
    height: 40px;
    background: var(--amber);
    color: var(--black);
    border-radius: 11px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: "Barlow Condensed";
    font-weight: 900;
    font-size: 25px;
}

.brand-name {
    font-family: "Barlow Condensed";
    font-size: 25px;
    line-height: 20px;
    font-weight: 900;
    letter-spacing: .08em;
}

.brand-sub {
    color: #858d95;
    font-size: 8px;
    letter-spacing: .2em;
    margin-top: 5px;
}

.domain {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    letter-spacing: .1em;
    font-weight: 700;
}

.domain-pill {
    color: var(--black);
    background: var(--amber);
    padding: 7px 13px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 900;
}

.signed {
    color: #9199a1;
    font-size: 10px;
}


/* ============================================================
   WELCOME HERO
   ============================================================ */

.welcome {
    min-height: 410px;
    margin: 0 -2.2rem 35px;
    padding: 65px 45px;
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            90deg,
            rgba(5,7,9,.96) 0%,
            rgba(5,7,9,.86) 45%,
            rgba(5,7,9,.48) 100%
        ),
        url("https://images.unsplash.com/photo-1578662996442-48f60103fc96?auto=format&fit=crop&w=2400&q=90")
        center/cover no-repeat;

    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 25px 70px rgba(0,0,0,.2);
}

.welcome::after {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(
            125deg,
            transparent 40%,
            rgba(242,169,0,.12)
        );
    pointer-events: none;
}

.welcome-content {
    position: relative;
    z-index: 2;
    max-width: 850px;
}

.kicker {
    color: var(--amber);
    font-size: 11px;
    letter-spacing: .28em;
    font-weight: 900;
}

.welcome-title {
    color: white;
    font-family: "Barlow Condensed";
    font-size: 76px;
    line-height: .82;
    font-weight: 900;
    margin-top: 15px;
}

.welcome-title span {
    color: var(--amber);
}

.welcome-domain {
    margin-top: 22px;
    color: #e5e7e9;
    letter-spacing: .17em;
    font-size: 12px;
    font-weight: 800;
}

.welcome-description {
    color: #adb5bd;
    margin-top: 13px;
    font-size: 15px;
    line-height: 1.7;
    max-width: 610px;
}


/* ============================================================
   CHOICE CARDS
   ============================================================ */

.choice {
    background: #fffdf8;
    border: 1px solid #ded8cc;
    border-radius: 24px;
    min-height: 245px;
    padding: 30px;
    box-shadow: 0 15px 40px rgba(20,20,20,.07);
}

.choice:hover {
    border-color: var(--amber);
}

.choice-small {
    color: #a16d00;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: .2em;
}

.choice-title {
    color: #17191c;
    font-family: "Barlow Condensed";
    font-weight: 900;
    font-size: 46px;
    line-height: .95;
    margin-top: 10px;
}

.choice-text {
    color: #6d747b;
    line-height: 1.6;
    margin-top: 12px;
    max-width: 450px;
}

.choice-arrow {
    color: #a16d00;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: .17em;
    margin-top: 22px;
}


/* ============================================================
   SIGN OUT
   ============================================================ */

.signout-row {
    margin-top: 12px;
    margin-bottom: 15px;
}


/* ============================================================
   PAGE CONTROLS
   ============================================================ */

.crumb {
    color: #777f86;
    font-size: 11px;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin: 8px 0 25px;
}

.crumb strong {
    color: #a16d00;
}


/* ============================================================
   MODULE CARDS
   ============================================================ */

.module {
    background: #fffdf8;
    border: 1px solid #ddd7ca;
    border-radius: 20px;
    min-height: 180px;
    padding: 23px;
    box-shadow: 0 9px 30px rgba(20,20,20,.05);
    transition: .2s;
}

.module:hover {
    transform: translateY(-3px);
    border-color: var(--amber);
    box-shadow: 0 18px 40px rgba(20,20,20,.1);
}

.module-arrow {
    float: right;
    background: #eee9df;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #646b72;
    font-size: 19px;
}

.module-title {
    clear: both;
    padding-top: 25px;
    font-family: "Barlow Condensed";
    font-size: 26px;
    font-weight: 800;
}

.module-text {
    color: #747b82;
    font-size: 13px;
    line-height: 1.55;
    margin-top: 5px;
}


/* ============================================================
   DASHBOARD
   ============================================================ */

.dashboard-hero {
    background:
        linear-gradient(120deg,#111417,#252b31);
    color: white;
    padding: 30px;
    border-radius: 22px;
    margin-bottom: 20px;
}

.dashboard-hero h1 {
    color: white !important;
    margin: 0;
}

.dashboard-hero p {
    color: #aeb6bf;
    margin: 4px 0 0;
}


/* ============================================================
   METRICS
   ============================================================ */

[data-testid="stMetric"] {
    background: #fffdf8;
    border: 1px solid #ddd7ca;
    border-left: 5px solid var(--amber);
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 8px 25px rgba(20,20,20,.05);
}


/* ============================================================
   LOGIN
   ============================================================ */

.login-shell {
    max-width: 1100px;
    margin: 80px auto;
}

.login-title {
    font-family: "Barlow Condensed";
    color: white;
    font-size: 80px;
    font-weight: 900;
}

.login-panel {
    background: #171a1e;
    padding: 35px;
    border-radius: 22px;
    border: 1px solid #343a40;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media(max-width:800px) {

    .block-container {
        padding: 0 1rem 2rem;
    }

    .appbar {
        margin-left: -1rem;
        margin-right: -1rem;
        padding: 12px 16px;
    }

    .domain {
        display: none;
    }

    .welcome {
        margin-left: -1rem;
        margin-right: -1rem;
        padding: 50px 25px;
        min-height: 380px;
    }

    .welcome-title {
        font-size: 55px;
    }

    .choice {
        margin-bottom: 15px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEMO DATA
# ============================================================

INCIDENTS = pd.DataFrame({
    "Date": pd.date_range("2026-09-25", periods=12, freq="D"),
    "Incidents": [3, 2, 4, 1, 2, 5, 3, 2, 1, 2, 3, 1]
})

EQUIPMENT = pd.DataFrame({
    "Equipment": [
        "DR-001",
        "DR-002",
        "LHD-014",
        "LHD-021",
        "HD-110",
        "HD-114",
        "JMB-004",
        "JMB-006"
    ],
    "Availability": [
        "Available",
        "Available",
        "Maintenance",
        "Available",
        "Available",
        "Breakdown",
        "Available",
        "Available"
    ],
    "Condition": [
        "Normal",
        "Normal",
        "Warning",
        "Normal",
        "Normal",
        "Critical",
        "Normal",
        "Warning"
    ]
})

ALERTS = pd.DataFrame({
    "Category": [
        "Equipment",
        "Safety",
        "Maintenance",
        "Equipment",
        "Worker Safety"
    ],
    "Severity": [
        "CRITICAL",
        "WARNING",
        "WARNING",
        "CRITICAL",
        "WARNING"
    ],
    "Message": [
        "HD-114 hydraulic temperature above limit.",
        "PPE compliance below target in Section B.",
        "LHD-014 service interval exceeded.",
        "Ventilation sensor reading outside normal range.",
        "Fatigue flag detected during shift monitoring."
    ]
})

WORKERS = pd.DataFrame({
    "Worker ID": [
        "W001",
        "W002",
        "W003",
        "W004",
        "W005",
        "W006"
    ],
    "Department": [
        "Production",
        "Engineering",
        "Production",
        "Maintenance",
        "Safety",
        "Production"
    ],
    "PPE": [
        "Compliant",
        "Compliant",
        "Review",
        "Compliant",
        "Compliant",
        "Review"
    ],
    "Fatigue": [
        "Normal",
        "Normal",
        "Flag",
        "Normal",
        "Normal",
        "Flag"
    ]
})

MAINTENANCE = pd.DataFrame({
    "Equipment": [
        "DR-001",
        "DR-002",
        "LHD-014",
        "LHD-021",
        "HD-110",
        "HD-114"
    ],
    "Service": [
        "Complete",
        "Complete",
        "OVERDUE",
        "Due Soon",
        "Complete",
        "OVERDUE"
    ],
    "Last Service": [
        "2026-09-18",
        "2026-09-21",
        "2026-08-12",
        "2026-09-05",
        "2026-09-20",
        "2026-08-30"
    ]
})


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "Welcome"


# ============================================================
# ROLE HELPERS
# ============================================================

def role_name():

    roles = {
        "Safety Officer": "SAFETY OFFICER",
        "Admin": "ADMIN",
        "Engineer": "ENGINEER",
        "Maintenance": "MAINTENANCE",
        "Manager": "MANAGER"
    }

    return roles.get(
        st.session_state.role,
        "USER"
    )


# ============================================================
# NAVIGATION
# ============================================================

def go(page):
    st.session_state.page = page
    st.rerun()


def sign_out():

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "Welcome"

    st.rerun()


# ============================================================
# APP HEADER
# ============================================================

def app_header():

    role = role_name()

    st.markdown(f"""
    <div class="appbar">

        <div class="brand">

            <div class="brand-mark">
                K
            </div>

            <div>
                <div class="brand-name">
                    KHWEZI
                </div>

                <div class="brand-sub">
                    MINING INTELLIGENCE
                </div>
            </div>

        </div>

        <div class="domain">

            <span class="domain-pill">
                {role} DOMAIN
            </span>

            <span>
                KHWEZI OPERATIONS
            </span>

        </div>

        <div class="signed">
            SIGNED IN
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SIGN OUT BUTTON — EVERYWHERE
# ============================================================

def sign_out_bar():

    st.markdown(
        '<div class="signout-row"></div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([8, 1])

    with right:

        if st.button(
            "SIGN OUT",
            use_container_width=True
        ):
            sign_out()


# ============================================================
# LOGIN
# ============================================================

def login():

    st.markdown("""
    <div class="login-shell">

        <div class="hero">

            <div class="kicker">
                KHWEZI MINING / OPERATIONS INTELLIGENCE
            </div>

            <div class="login-title">
                KHWEZI
            </div>

            <div style="
                color:#d8dde1;
                font-size:20px;
                margin-top:10px;
            ">
                Health, Safety & Equipment Monitoring
            </div>

            <div style="
                color:#939ca5;
                max-width:620px;
                margin-top:12px;
                line-height:1.6;
            ">
                One operational command centre for people,
                equipment, incidents, risk and maintenance.
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    _, middle, _ = st.columns([1, 1, 1])

    with middle:

        st.markdown(
            '<div class="kicker">SECURE ACCESS</div>',
            unsafe_allow_html=True
        )

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button(
            "ENTER KHWEZI →",
            use_container_width=True
        ):

            accounts = {
                "safety": (
                    "Safety@123",
                    "Safety Officer"
                ),
                "admin": (
                    "Admin@123",
                    "Admin"
                ),
                "engineer": (
                    "Mining@123",
                    "Engineer"
                ),
                "maint": (
                    "Maint@123",
                    "Maintenance"
                ),
                "manager": (
                    "Manager@123",
                    "Manager"
                )
            }

            if (
                username in accounts
                and password == accounts[username][0]
            ):

                st.session_state.logged_in = True
                st.session_state.role = accounts[
                    username
                ][1]

                st.session_state.page = "Welcome"

                st.rerun()

            else:
                st.error(
                    "Invalid username or password."
                )

        with st.expander(
            "DEMO LOGIN DETAILS"
        ):

            st.write(
                "Safety Officer: safety / Safety@123"
            )

            st.write(
                "Admin: admin / Admin@123"
            )

            st.write(
                "Engineer: engineer / Mining@123"
            )

            st.write(
                "Maintenance: maint / Maint@123"
            )

            st.write(
                "Manager: manager / Manager@123"
            )


# ============================================================
# WELCOME
# ============================================================

def welcome():

    role = role_name()

    st.markdown(f"""
    <div class="welcome">

        <div class="welcome-content">

            <div class="kicker">
                KHWEZI MINING OPERATIONS
            </div>

            <div class="welcome-title">
                WELCOME,
                <span>{role}.</span>
            </div>

            <div class="welcome-domain">
                {role} DOMAIN · OPERATIONS CONTROL
            </div>

            <div class="welcome-description">
                Your mining operations space.
                Choose where you want to go.
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(
        2,
        gap="large"
    )

    with left:

        st.markdown("""
        <div class="choice">

            <div class="choice-small">
                SEE THE BIG PICTURE
            </div>

            <div class="choice-title">
                DASHBOARD
            </div>

            <div class="choice-text">
                Your operational command centre for
                performance, alerts, incidents and
                equipment health.
            </div>

            <div class="choice-arrow">
                OPEN DASHBOARD →
            </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "DASHBOARD",
            key="welcome_dashboard",
            use_container_width=True
        ):
            go("Dashboard")

    with right:

        st.markdown("""
        <div class="choice">

            <div class="choice-small">
                GO INTO THE DETAILS
            </div>

            <div class="choice-title">
                MY DATA
            </div>

            <div class="choice-text">
                Explore safety, people, equipment,
                maintenance, risk, analysis and
                reporting tools.
            </div>

            <div class="choice-arrow">
                OPEN MY DATA →
            </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "MY DATA",
            key="welcome_data",
            use_container_width=True
        ):
            go("My Data")

    st.markdown("""
    <div style="
        text-align:center;
        margin-top:35px;
        color:#7f878e;
        font-size:10px;
        font-weight:800;
        letter-spacing:.2em;
    ">
        PEOPLE • EQUIPMENT • SAFETY • INTELLIGENCE
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.markdown("""
    <div class="dashboard-hero">

        <h1>
            COMMAND CENTRE
        </h1>

        <p>
            Live operational picture across Khwezi Mining.
        </p>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "ACTIVE ALERTS",
        "05",
        "+2"
    )

    c2.metric(
        "EQUIPMENT AVAILABLE",
        "75%",
        "+4%"
    )

    c3.metric(
        "OPEN INCIDENTS",
        "08",
        "-3"
    )

    c4.metric(
        "PPE COMPLIANCE",
        "94%",
        "+2%"
    )

    st.markdown("### Operational trend")

    left, right = st.columns(2)

    with left:

        fig = px.line(
            INCIDENTS,
            x="Date",
            y="Incidents",
            markers=True,
            title="Safety incidents",
        )

        fig.update_traces(
            line=dict(
                color="#F2A900",
                width=3
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        availability = (
            EQUIPMENT["Availability"]
            .value_counts()
            .reset_index()
        )

        availability.columns = [
            "Status",
            "Equipment"
        ]

        fig = px.bar(
            availability,
            x="Status",
            y="Equipment",
            title="Equipment availability",
        )

        fig.update_traces(
            marker_color="#F2A900"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### Priority alerts")

    for _, row in ALERTS.head(4).iterrows():

        severity = row["Severity"]

        if severity == "CRITICAL":
            border = "#E05252"
        else:
            border = "#F2A900"

        st.markdown(f"""
        <div style="
            background:#fffdf8;
            border-left:5px solid {border};
            padding:15px 18px;
            margin-bottom:9px;
            border-radius:10px;
            border-top:1px solid #ded8cc;
            border-right:1px solid #ded8cc;
            border-bottom:1px solid #ded8cc;
        ">

            <div style="
                font-size:10px;
                font-weight:900;
                letter-spacing:.15em;
                color:{border};
            ">
                {severity}
            </div>

            <div style="
                margin-top:5px;
                font-weight:600;
                color:#25282c;
            ">
                {row["Message"]}
            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# MY DATA
# ============================================================

def my_data():

    st.markdown(
        '<div class="kicker">YOUR KHWEZI TOOLKIT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="screen-title">MY DATA</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="
        color:#727a81;
        margin-bottom:25px;
    ">
        Choose a section to go deeper into the operation.
    </div>
    """, unsafe_allow_html=True)

    modules = [
        (
            "Alerts",
            "Exceptions, warnings and critical conditions."
        ),
        (
            "Worker Safety",
            "People, PPE, fatigue and worker risk."
        ),
        (
            "Safety Incidents",
            "Record and investigate safety incidents."
        ),
        (
            "Equipment",
            "Fleet condition and equipment health."
        ),
        (
            "Maintenance",
            "Service activity and machine readiness."
        ),
        (
            "Risk Assessment",
            "Identify hazards and understand exposure."
        ),
        (
            "Data Analysis",
            "Turn operational data into insight."
        ),
        (
            "Reports",
            "Create and export operational reports."
        )
    ]

    if role_name() == "ADMIN":
        modules.append(
            (
                "Manage Users",
                "Manage users, roles and access."
            )
        )

    cols = st.columns(3)

    for index, (
        title,
        description
    ) in enumerate(modules):

        with cols[index % 3]:

            st.markdown(f"""
            <div class="module">

                <div class="module-arrow">
                    →
                </div>

                <div class="module-title">
                    {title}
                </div>

                <div class="module-text">
                    {description}
                </div>

            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"OPEN {title.upper()}",
                key=f"module_{title}",
                use_container_width=True
            ):
                go(title)


# ============================================================
# ALERTS
# ============================================================

def alerts_page():

    st.markdown(
        '<div class="kicker">OPERATIONS</div>',
        unsafe_allow_html=True
    )

    st.title("Alerts")

    severity = st.multiselect(
        "Filter severity",
        ["CRITICAL", "WARNING"],
        default=["CRITICAL", "WARNING"]
    )

    data = ALERTS[
        ALERTS["Severity"].isin(severity)
    ]

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# WORKER SAFETY
# ============================================================

def worker_safety():

    st.markdown(
        '<div class="kicker">PEOPLE</div>',
        unsafe_allow_html=True
    )

    st.title("Worker Safety")

    a, b, c = st.columns(3)

    a.metric(
        "WORKERS",
        "126"
    )

    b.metric(
        "PPE COMPLIANCE",
        "94%"
    )

    c.metric(
        "FATIGUE FLAGS",
        "07"
    )

    st.markdown("### Worker register")

    st.dataframe(
        WORKERS,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# INCIDENTS
# ============================================================

def incidents_page():

    st.markdown(
        '<div class="kicker">SAFETY</div>',
        unsafe_allow_html=True
    )

    st.title("Safety Incidents")

    a, b, c = st.columns(3)

    a.metric(
        "TOTAL INCIDENTS",
        "29"
    )

    b.metric(
        "OPEN",
        "08"
    )

    c.metric(
        "NEAR MISSES",
        "14"
    )

    st.dataframe(
        pd.DataFrame({
            "Date": [
                "2026-10-05",
                "2026-10-04",
                "2026-10-03",
                "2026-10-02"
            ],
            "Category": [
                "Equipment",
                "PPE",
                "Ground Control",
                "Vehicle"
            ],
            "Severity": [
                "High",
                "Medium",
                "High",
                "Low"
            ],
            "Status": [
                "Open",
                "Closed",
                "Open",
                "Closed"
            ]
        }),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EQUIPMENT
# ============================================================

def equipment_page():

    st.markdown(
        '<div class="kicker">FLEET</div>',
        unsafe_allow_html=True
    )

    st.title("Equipment")

    a, b, c, d = st.columns(4)

    a.metric(
        "TOTAL EQUIPMENT",
        "48"
    )

    b.metric(
        "AVAILABLE",
        "36"
    )

    c.metric(
        "MAINTENANCE",
        "08"
    )

    d.metric(
        "CRITICAL",
        "04"
    )

    st.markdown("### Equipment condition")

    st.dataframe(
        EQUIPMENT,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MAINTENANCE
# ============================================================

def maintenance_page():

    st.markdown(
        '<div class="kicker">RELIABILITY</div>',
        unsafe_allow_html=True
    )

    st.title("Maintenance")

    a, b, c = st.columns(3)

    a.metric(
        "WORK ORDERS",
        "32"
    )

    b.metric(
        "DUE SOON",
        "06"
    )

    c.metric(
        "OVERDUE",
        "03"
    )

    st.dataframe(
        MAINTENANCE,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RISK
# ============================================================

def risk_page():

    st.markdown(
        '<div class="kicker">CONTROL</div>',
        unsafe_allow_html=True
    )

    st.title("Risk Assessment")

    left, right = st.columns(2)

    with left:

        likelihood = st.slider(
            "Likelihood",
            1,
            5,
            3
        )

    with right:

        consequence = st.slider(
            "Consequence",
            1,
            5,
            3
        )

    score = likelihood * consequence

    if score <= 4:
        level = "LOW"
        border = "#4FBD7A"
    elif score <= 9:
        level = "MEDIUM"
        border = "#F2A900"
    elif score <= 16:
        level = "HIGH"
        border = "#ED8D22"
    else:
        level = "CRITICAL"
        border = "#E05252"

    st.markdown(f"""
    <div style="
        background:#fffdf8;
        border-left:7px solid {border};
        padding:25px;
        border-radius:15px;
        border-top:1px solid #ddd7ca;
        border-right:1px solid #ddd7ca;
        border-bottom:1px solid #ddd7ca;
        margin-top:20px;
    ">

        <div style="
            color:#7c8288;
            font-size:11px;
            letter-spacing:.16em;
            font-weight:800;
        ">
            CURRENT RISK
        </div>

        <div style="
            font-family:'Barlow Condensed';
            font-size:55px;
            font-weight:900;
            color:#17191c;
        ">
            {score}
        </div>

        <div style="
            color:{border};
            font-weight:900;
            letter-spacing:.15em;
        ">
            {level}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DATA ANALYSIS
# ============================================================

def analysis_page():

    st.markdown(
        '<div class="kicker">INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.title("Data Analysis")

    question = st.selectbox(
        "Business question",
        [
            "How are incidents changing?",
            "What is the equipment availability?",
            "Where are the main safety concerns?",
            "Which equipment needs attention?"
        ]
    )

    if question == "How are incidents changing?":

        fig = px.line(
            INCIDENTS,
            x="Date",
            y="Incidents",
            markers=True,
            title="Incident trend"
        )

        fig.update_traces(
            line=dict(
                color="#F2A900",
                width=3
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif question == "What is the equipment availability?":

        data = (
            EQUIPMENT["Availability"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            data,
            names="Status",
            values="Count",
            title="Equipment availability"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif question == "Where are the main safety concerns?":

        st.info(
            "The current demo shows PPE, fatigue, "
            "equipment and incident trends as the "
            "main operational safety areas."
        )

    else:

        st.dataframe(
            EQUIPMENT[
                EQUIPMENT["Condition"] != "Normal"
            ],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# REPORTS
# ============================================================

def reports_page():

    st.markdown(
        '<div class="kicker">DOCUMENTS</div>',
        unsafe_allow_html=True
    )

    st.title("Reports")

    report = f"""
KHWЕZI MINING
OPERATIONAL SAFETY REPORT

Date: {date.today()}

Equipment
---------
Total equipment: 48
Available: 36
Maintenance: 8
Critical: 4

Safety
------
PPE compliance: 94%
Open incidents: 8
Near misses: 14

Alerts
------
Critical alerts: 2
Warning alerts: 3

Overall operational status:
ATTENTION REQUIRED
"""

    st.text_area(
        "Operational report",
        report,
        height=350
    )

    st.download_button(
        "DOWNLOAD REPORT",
        report,
        "khwezi_operational_report.txt",
        "text/plain"
    )


# ============================================================
# USER MANAGEMENT
# ============================================================

def users_page():

    st.markdown(
        '<div class="kicker">ADMINISTRATION</div>',
        unsafe_allow_html=True
    )

    st.title("Manage Users")

    users = pd.DataFrame({
        "Role": [
            "Admin",
            "Safety Officer",
            "Engineer",
            "Maintenance",
            "Manager"
        ],
        "Status": [
            "Active",
            "Active",
            "Active",
            "Active",
            "Active"
        ],
        "Access": [
            "Full",
            "Safety",
            "Engineering",
            "Maintenance",
            "Management"
        ]
    })

    st.dataframe(
        users,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE ROUTER
# ============================================================

def render_page():

    page = st.session_state.page

    if page == "Welcome":
        welcome()

    elif page == "Dashboard":
        dashboard()

    elif page == "My Data":
        my_data()

    elif page == "Alerts":
        alerts_page()

    elif page == "Worker Safety":
        worker_safety()

    elif page == "Safety Incidents":
        incidents_page()

    elif page == "Equipment":
        equipment_page()

    elif page == "Maintenance":
        maintenance_page()

    elif page == "Risk Assessment":
        risk_page()

    elif page == "Data Analysis":
        analysis_page()

    elif page == "Reports":
        reports_page()

    elif page == "Manage Users":
        users_page()


# ============================================================
# MAIN
# ============================================================

if not st.session_state.logged_in:

    login()

else:

    app_header()

    sign_out_bar()

    if st.session_state.page != "Welcome":

        left, middle, right = st.columns([
            1,
            1,
            6
        ])

        with left:

            if st.button(
                "← BACK",
                use_container_width=True
            ):

                if st.session_state.page in [
                    "Dashboard",
                    "My Data"
                ]:

                    go("Welcome")

                else:

                    go("My Data")

        with middle:

            if st.button(
                "⌂ HOME",
                use_container_width=True
            ):
                go("Welcome")

        st.markdown(
            f"""
            <div class="crumb">
                <strong>KHWEZI</strong>
                &nbsp;›&nbsp;
                {st.session_state.page.upper()}
            </div>
            """,
            unsafe_allow_html=True
        )

    render_page()
```
