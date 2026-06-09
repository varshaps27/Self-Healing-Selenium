import streamlit as st
import json
import time
import threading
import queue
import os

st.set_page_config(
    page_title="Self-Healing Selenium Framework",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Overall background */
.stApp { background-color: #0f172a; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* Main content */
.main-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 100%);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    border: 1px solid #2563eb;
    text-align: center;
}
.main-header h1 { color: #38bdf8; font-size: 2.2rem; margin: 0; }
.main-header p  { color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 1rem; }

/* OrangeHRM Login Mock */
.orangehrm-wrapper {
    background: #fff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    max-width: 900px;
    margin: 0 auto;
}
.orangehrm-left {
    background: linear-gradient(135deg, #ff6b35, #f7931e);
    padding: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
}
.orangehrm-right {
    background: #fff;
    padding: 2.5rem;
}
.login-form-field {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 12px 16px;
    width: 100%;
    font-size: 14px;
    margin-bottom: 1rem;
    background: #f9fafb;
}
.login-btn {
    background: linear-gradient(135deg, #ff6b35, #f7931e);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 0;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
}

/* Dashboard mock */
.dashboard-wrapper {
    background: #f3f4f6;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.dash-topbar {
    background: #fff;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.dash-sidebar {
    background: #fff;
    border-right: 1px solid #e5e7eb;
    padding: 1rem 0;
    min-height: 300px;
}
.dash-menu-item {
    padding: 10px 20px;
    font-size: 13px;
    color: #374151;
    cursor: pointer;
    border-left: 3px solid transparent;
}
.dash-menu-item:hover { background: #fef3ec; border-left-color: #f7931e; color: #f7931e; }
.dash-card {
    background: #fff;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

/* Scenario cards */
.scenario-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.scenario-card.pass   { border-left: 4px solid #22c55e; }
.scenario-card.healed { border-left: 4px solid #f59e0b; }
.scenario-card.fail   { border-left: 4px solid #ef4444; }
.scenario-card.report { border-left: 4px solid #38bdf8; }

/* Log console */
.log-console {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1rem;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    min-height: 200px;
    max-height: 350px;
    overflow-y: auto;
    color: #94a3b8;
}
.log-success { color: #22c55e; }
.log-warn    { color: #f59e0b; }
.log-error   { color: #ef4444; }
.log-info    { color: #38bdf8; }

/* Status badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}
.badge-pass   { background: #dcfce7; color: #16a34a; }
.badge-healed { background: #fef3c7; color: #d97706; }
.badge-fail   { background: #fee2e2; color: #dc2626; }
.badge-report { background: #dbeafe; color: #2563eb; }

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1rem; }
.metric-card {
    flex: 1;
    background: #1e293b;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #334155;
}
.metric-value { font-size: 2rem; font-weight: 700; color: #38bdf8; }
.metric-label { font-size: 12px; color: #64748b; margin-top: 4px; }

/* Button overrides */
.stButton button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛡️ Self-Healing Framework")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Overview",
        "🔐 Login Page (Mock)",
        "📊 Dashboard (Mock)",
        "▶️ Run Tests",
        "🧪 Test Scenarios",
        "📋 Locator Config",
    ])
    st.markdown("---")
    st.markdown("**Tech Stack**")
    st.markdown("🐍 Python 3.11")
    st.markdown("🌐 Selenium 4.6+")
    st.markdown("🍜 BeautifulSoup4")
    st.markdown("✅ Pytest")
    st.markdown("🎈 Streamlit")
    st.markdown("---")
    st.markdown("**Target Site**")
    st.markdown("[OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/)")

# ══════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Self-Healing Selenium Framework</h1>
        <p>AI-powered test automation that fixes broken locators & credentials automatically</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Test Scenarios", "6", "Covered")
    with col2:
        st.metric("Auto-Healed", "4", "Scenarios")
    with col3:
        st.metric("Manual Fixes", "0", "Required")
    with col4:
        st.metric("Target Site", "OrangeHRM", "Demo")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ❌ The Problem")
        st.error("""
- UI tests break when developers change element IDs
- Locators must be manually updated every time
- Wrong credentials cause silent test failures
- CSRF tokens get picked as wrong locators
        """)

    with col2:
        st.markdown("### ✅ Our Solution")
        st.success("""
- Auto-detects broken locators and heals in real time
- Scans page HTML: id → name → css → xpath priority
- Skips hidden/CSRF fields automatically
- Resets wrong credentials and retries login
        """)

    st.markdown("---")
    st.markdown("### 🔁 Self-Healing Flow")
    cols = st.columns(5)
    steps = [
        ("1️⃣", "Test Runs", "find_element() called", "#3b82f6"),
        ("2️⃣", "Not Found", "NoSuchElement error", "#ef4444"),
        ("3️⃣", "Scan HTML", "BeautifulSoup parses page", "#f59e0b"),
        ("4️⃣", "Best Locator", "id>name>css>xpath", "#a855f7"),
        ("5️⃣", "JSON Updated", "Auto-rewritten & retry", "#22c55e"),
    ]
    for col, (icon, title, desc, _) in zip(cols, steps):
        with col:
            st.markdown(f"**{icon} {title}**")
            st.caption(desc)

# ══════════════════════════════════════════════════════════════════════
# PAGE: LOGIN PAGE MOCK
# ══════════════════════════════════════════════════════════════════════
elif page == "🔐 Login Page (Mock)":
    st.markdown("## 🔐 OrangeHRM Login Page")
    st.caption("This is the actual login page your Selenium test targets")
    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b35, #f7931e);
                    border-radius: 16px; padding: 2.5rem; text-align: center;
                    min-height: 420px; display: flex; flex-direction: column;
                    align-items: center; justify-content: center;">
            <div style="font-size: 64px; margin-bottom: 1rem;">🟠</div>
            <div style="font-size: 2rem; font-weight: 800; color: white;">Orange<span style="color:#1a1a2e">HRM</span></div>
            <div style="color: rgba(255,255,255,0.8); font-size: 12px; margin-top: 4px; letter-spacing: 2px;">OPEN SOURCE HR MANAGEMENT</div>
            <div style="margin-top: 2rem; width: 80px; height: 80px; border-radius: 50%;
                        background: rgba(255,255,255,0.2); display: flex; align-items: center;
                        justify-content: center; font-size: 2rem; color: white;">👤</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 11px; margin-top: 1rem;">HR for All</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 2.5rem;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <div style="text-align:center; margin-bottom: 1.5rem;">
                <div style="color: #f7931e; font-weight: 800; font-size: 1.8rem;">Login</div>
            </div>
            <div style="background: #f3f4f6; border-radius: 8px; padding: 12px 16px; margin-bottom: 1.5rem;">
                <div style="font-size: 13px; color: #374151;">
                    <strong>Username :</strong> Admin<br/>
                    <strong>Password :</strong> admin123
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            username = st.text_input("Username", placeholder="Username", key="mock_user")
            password = st.text_input("Password", placeholder="Password", type="password", key="mock_pass")

            if st.button("Login", use_container_width=True, key="mock_login"):
                if username == "Admin" and password == "admin123":
                    st.success("✅ Login Successful! Redirecting to Dashboard...")
                    st.balloons()
                elif username and password:
                    st.error("❌ Invalid credentials")
                else:
                    st.warning("⚠️ Please enter username and password")

            st.markdown("<div style='text-align:center; margin-top: 1rem;'><a href='#' style='color:#f7931e; text-decoration:none; font-size:13px;'>Forgot your password?</a></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Locators Selenium Uses for This Page")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.code('By.NAME, "username"', language="python")
        st.caption("Username field")
    with col2:
        st.code('By.NAME, "password"', language="python")
        st.caption("Password field")
    with col3:
        st.code('By.XPATH, "//button[@type=\'submit\']"', language="python")
        st.caption("Login button")

# ══════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD MOCK
# ══════════════════════════════════════════════════════════════════════
elif page == "📊 Dashboard (Mock)":
    st.markdown("## 📊 OrangeHRM Dashboard")
    st.caption("This is what appears after successful login — Selenium verifies this page loads")
    st.markdown("---")

    # Top bar
    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 1rem 2rem;
                display: flex; justify-content: space-between; align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem; color: #374151;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="color: #f7931e; font-weight: 800; font-size: 1.2rem;">🟠 OrangeHRM</span>
            <span style="color: #9ca3af; font-size: 13px;">| Dashboard</span>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem; font-size: 13px;">
            <span>🔔</span>
            <span>👤 Admin</span>
            <span style="color: #ef4444; cursor: pointer;">Logout</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_side, col_main = st.columns([1, 4])

    with col_side:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 1rem 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        """, unsafe_allow_html=True)
        menu_items = ["Admin", "PIM", "Leave", "Time", "Recruitment", "My Info", "Performance", "Dashboard", "Directory", "Maintenance"]
        for item in menu_items:
            icon = {"Admin": "⚙️", "PIM": "👥", "Leave": "🏖️", "Time": "⏰", "Recruitment": "📋", "My Info": "👤", "Performance": "📈", "Dashboard": "🏠", "Directory": "📁", "Maintenance": "🔧"}.get(item, "•")
            st.markdown(f"<div style='padding: 8px 16px; font-size: 13px; color: #374151; cursor: pointer;'>{icon} {item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        # Stats row
        c1, c2, c3, c4 = st.columns(4)
        stats = [("👥", "124", "Total Employees"), ("🕒", "8", "Pending Leaves"), ("📋", "3", "Open Positions"), ("⚠️", "2", "HR Alerts")]
        for c, (icon, val, label) in zip([c1, c2, c3, c4], stats):
            with c:
                st.markdown(f"""
                <div style="background: white; border-radius: 10px; padding: 1.2rem;
                            text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                    <div style="font-size: 1.8rem;">{icon}</div>
                    <div style="font-size: 1.6rem; font-weight: 700; color: #f7931e;">{val}</div>
                    <div style="font-size: 11px; color: #9ca3af;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts row
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("""
            <div style="background: white; border-radius: 10px; padding: 1.5rem;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                <div style="font-weight: 600; color: #374151; margin-bottom: 1rem;">📊 Employee Distribution</div>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <div><span style="color:#555; font-size:12px;">Engineering</span>
                        <div style="background:#f3f4f6; border-radius:4px; height:8px; margin-top:4px;">
                        <div style="background:#f7931e; width:65%; height:8px; border-radius:4px;"></div></div></div>
                    <div><span style="color:#555; font-size:12px;">HR</span>
                        <div style="background:#f3f4f6; border-radius:4px; height:8px; margin-top:4px;">
                        <div style="background:#3b82f6; width:20%; height:8px; border-radius:4px;"></div></div></div>
                    <div><span style="color:#555; font-size:12px;">Finance</span>
                        <div style="background:#f3f4f6; border-radius:4px; height:8px; margin-top:4px;">
                        <div style="background:#22c55e; width:15%; height:8px; border-radius:4px;"></div></div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with cc2:
            st.markdown("""
            <div style="background: white; border-radius: 10px; padding: 1.5rem;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                <div style="font-weight: 600; color: #374151; margin-bottom: 1rem;">📅 Leave Summary</div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px; color: #374151;">
                    <div style="display:flex; justify-content:space-between;"><span>Annual Leave</span><span style="color:#22c55e;">✅ 14 days</span></div>
                    <div style="display:flex; justify-content:space-between;"><span>Sick Leave</span><span style="color:#f59e0b;">⏳ 7 days</span></div>
                    <div style="display:flex; justify-content:space-between;"><span>Casual Leave</span><span style="color:#3b82f6;">📋 5 days</span></div>
                    <div style="display:flex; justify-content:space-between;"><span>Maternity</span><span style="color:#a855f7;">🌸 90 days</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("✅ **Selenium confirms login success** when this dashboard page loads and the top navigation bar `oxd-topbar-header` is detected.")

# ══════════════════════════════════════════════════════════════════════
# PAGE: RUN TESTS
# ══════════════════════════════════════════════════════════════════════
elif page == "▶️ Run Tests":
    st.markdown("## ▶️ Run Self-Healing Tests")
    st.caption("Runs the actual Selenium test against OrangeHRM Demo site")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        scenario = st.selectbox("Choose Test Scenario", [
            "01 — Normal Login (Everything Correct)",
            "02 — Wrong Password (Credential Healing)",
            "03 — Broken Username Locator (Locator Healing)",
            "04 — Broken Button Locator (Locator Healing)",
            "05 — Page Load Failure (Bad URL)",
            "06 — Run via Pytest",
        ])

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_btn = st.button("▶️ Run Test", use_container_width=True, type="primary")

    # Instructions per scenario
    scenario_info = {
        "01 — Normal Login (Everything Correct)": {
            "badge": "PASS", "color": "success",
            "steps": [
                "Make sure login_locators.json has correct values (default)",
                "Click Run Test",
                "Watch Chrome open, type credentials, reach dashboard"
            ],
            "change": None
        },
        "02 — Wrong Password (Credential Healing)": {
            "badge": "HEALED", "color": "warning",
            "steps": [
                "In login_locators.json, change credentials.password to WRONGPASSWORD",
                "Click Run Test",
                "Framework detects 'Invalid credentials', auto-resets, retries"
            ],
            "change": '  "credentials": {\n    "username": "Admin",\n    "password": "WRONGPASSWORD"\n  }'
        },
        "03 — Broken Username Locator (Locator Healing)": {
            "badge": "HEALED", "color": "warning",
            "steps": [
                'In login_locators.json, change username value to "BROKEN_FIELD"',
                "Click Run Test",
                "Framework scans HTML, finds correct locator, updates JSON"
            ],
            "change": '  "username": { "type": "name", "value": "BROKEN_FIELD" }'
        },
        "04 — Broken Button Locator (Locator Healing)": {
            "badge": "HEALED", "color": "warning",
            "steps": [
                'In login_locators.json, change login_button value to //button[@type="BROKEN"]',
                "Click Run Test",
                "Framework finds the real button via HTML scan"
            ],
            "change": '  "login_button": { "type": "xpath", "value": "//button[@type=\'BROKEN\']" }'
        },
        "05 — Page Load Failure (Bad URL)": {
            "badge": "FAIL", "color": "error",
            "steps": [
                "In core/config.py, change BASE_URL to a fake URL",
                "Click Run Test",
                "Framework gives clear timeout error after 30s",
                "⚠️ Remember to revert config.py after!"
            ],
            "change": 'BASE_URL = "https://thissitedoesnotexist99999.com/"'
        },
        "06 — Run via Pytest": {
            "badge": "REPORT", "color": "info",
            "steps": [
                "Install pytest-html: pip install pytest-html",
                "Run: pytest tests/test_login.py -v -s --html=report.html --self-contained-html",
                "Open report.html in your browser"
            ],
            "change": None
        }
    }

    info = scenario_info[scenario]

    st.markdown("### 📋 Steps to Follow")
    for i, step in enumerate(info["steps"], 1):
        st.markdown(f"**Step {i}:** {step}")

    if info["change"]:
        st.markdown("**Change this in your file:**")
        st.code(info["change"], language="json")

    if run_btn:
        st.markdown("### 🖥️ Test Output")
        log_placeholder = st.empty()
        logs = []

        def add_log(msg, level="info"):
            prefix = {"info": "ℹ️", "success": "✅", "warn": "⚠️", "error": "❌"}.get(level, "")
            logs.append(f"{prefix} {msg}")
            log_placeholder.code("\n".join(logs), language="bash")
            time.sleep(0.3)

        try:
            add_log("Starting test run...", "info")
            add_log("Importing framework modules...", "info")

            from core.driver_factory import DriverFactory
            from tests.test_login import test_login

            add_log("✔ Modules loaded", "success")
            add_log("Launching Chrome (headless)...", "info")

            driver = DriverFactory.get_driver()
            add_log("✔ Chrome launched", "success")

            try:
                add_log("Opening OrangeHRM login page...", "info")
                test_login(driver)
                add_log("Login action completed. Dashboard loaded!", "success")
                add_log("ALL TESTS PASSED", "success")
                st.success("✅ Test PASSED — Login successful and dashboard loaded!")
                st.balloons()

            except AssertionError as e:
                add_log(f"TEST ASSERTION FAILED: {e}", "error")
                st.error(f"❌ Assertion Failed: {e}")

            except Exception as e:
                add_log(f"TEST FAILED: {e}", "error")
                st.error(f"❌ Test Failed: {e}")

            finally:
                driver.quit()
                add_log("Browser closed.", "info")

        except Exception as e:
            st.error(f"❌ Could not start test: {e}")
            st.info("💡 Make sure all dependencies are installed: pip install -r requirements.txt")

# ══════════════════════════════════════════════════════════════════════
# PAGE: TEST SCENARIOS
# ══════════════════════════════════════════════════════════════════════
elif page == "🧪 Test Scenarios":
    st.markdown("## 🧪 All 6 Test Scenarios")
    st.caption("Complete breakdown of every scenario this framework handles")
    st.markdown("---")

    scenarios = [
        {
            "num": "01", "title": "Normal Login", "badge": "PASS", "color": "#22c55e",
            "desc": "All locators correct. Framework logs in and reaches dashboard in one attempt.",
            "output": "🔄 Login attempt 1 of 2...\n✅ Username entered: Admin\n✅ Password entered.\n✅ Login button clicked.\n✅ Login action completed. Dashboard loaded!\n✅ All tests passed!"
        },
        {
            "num": "02", "title": "Wrong Password", "badge": "HEALED", "color": "#f59e0b",
            "desc": "Wrong credentials in JSON → detected via site error message → auto-reset → retry → pass.",
            "output": "🔄 Login attempt 1 of 2...\n✅ Username entered: Admin\n✅ Password entered.\n✅ Login button clicked.\n⚠️  Login error detected: 'Invalid credentials'\n🔧 Auto-healing credentials back to default...\n📝 Credentials auto-reset to default values.\n🔄 Login attempt 2 of 2...\n✅ Login action completed. Dashboard loaded!"
        },
        {
            "num": "03", "title": "Broken Username Locator", "badge": "HEALED", "color": "#f59e0b",
            "desc": "BROKEN_FIELD in JSON → SelfHealingEngine scans HTML → finds name=username → updates JSON → pass.",
            "output": "⚠️  Element 'username' not interactable. Triggering self-healing...\n📝 Locator updated for 'username': {'type': 'name', 'value': 'username'}\n✅ Healed 'username' → {'type': 'name', 'value': 'username'}\n✅ Username entered: Admin\n✅ All tests passed!"
        },
        {
            "num": "04", "title": "Broken Button Locator", "badge": "HEALED", "color": "#f59e0b",
            "desc": "Wrong button xpath → healed to working xpath via HTML scan → JSON updated → pass.",
            "output": "✅ Username entered: Admin\n✅ Password entered.\n⚠️  Element 'login_button' not interactable. Triggering self-healing...\n📝 Locator updated for 'login_button': {'type': 'xpath', 'value': '//button'}\n✅ Healed 'login_button' → {'type': 'xpath', 'value': '//button'}\n✅ Login action completed. Dashboard loaded!"
        },
        {
            "num": "05", "title": "Page Load Failure", "badge": "FAIL", "color": "#ef4444",
            "desc": "Bad URL in config.py → clear timeout error after 30s → browser stays open 5s → clean error message.",
            "output": "🚀 Starting test run...\n🌐 Opening OrangeHRM login page...\n❌ TEST FAILED UNEXPECTEDLY: Login page did not load within 30 seconds.\n🔒 Browser closed."
        },
        {
            "num": "06", "title": "HTML Report via Pytest", "badge": "REPORT", "color": "#38bdf8",
            "desc": "Run via pytest with --html flag to generate a full visual HTML test report.",
            "output": "================== test session starts ==================\ncollected 1 item\ntests/test_login.py::test_login\n✅ Username entered: Admin\n✅ Login action completed. Dashboard loaded!\nPASSED\n================== 1 passed in 14.23s =================="
        },
    ]

    for sc in scenarios:
        with st.expander(f"**Scenario {sc['num']} — {sc['title']}**  `{sc['badge']}`", expanded=False):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**Description:** {sc['desc']}")
            with col2:
                st.markdown("**Expected Terminal Output:**")
                st.code(sc["output"], language="bash")

# ══════════════════════════════════════════════════════════════════════
# PAGE: LOCATOR CONFIG
# ══════════════════════════════════════════════════════════════════════
elif page == "📋 Locator Config":
    st.markdown("## 📋 Locator Configuration")
    st.caption("Live view of login_locators.json — this file is auto-updated when self-healing occurs")
    st.markdown("---")

    try:
        with open("locators/login_locators.json", "r") as f:
            data = json.load(f)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### Current JSON File")
            st.json(data)

        with col2:
            st.markdown("### Locator Status")
            for key in ["username", "password", "login_button"]:
                loc = data.get(key, {})
                st.markdown(f"""
                **{key}**
                - Type: `{loc.get('type', 'N/A')}`
                - Value: `{loc.get('value', 'N/A')}`
                """)
                if loc.get("value") in ["BROKEN_FIELD", "WRONGPASSWORD", "_token"] or "BROKEN" in str(loc.get("value", "")):
                    st.error(f"⚠️ '{key}' looks broken — self-healing will fix this on next run")
                else:
                    st.success(f"✅ '{key}' looks correct")

            st.markdown("### Stored Credentials")
            creds = data.get("credentials", {})
            st.markdown(f"- Username: `{creds.get('username', 'N/A')}`")
            st.markdown(f"- Password: `{'*' * len(creds.get('password', ''))}`")

        st.markdown("---")
        st.markdown("### 🔧 Reset to Defaults")
        if st.button("Reset login_locators.json to defaults"):
            default = {
                "username": {"type": "name", "value": "username"},
                "password": {"type": "name", "value": "password"},
                "login_button": {"type": "xpath", "value": "//button[@type='submit']"},
                "credentials": {"username": "Admin", "password": "admin123"}
            }
            with open("locators/login_locators.json", "w") as f:
                json.dump(default, f, indent=2)
            st.success("✅ Reset to defaults! Refresh the page to see updated values.")

    except FileNotFoundError:
        st.error("❌ locators/login_locators.json not found")
        st.info("Make sure you are running from the project root directory")
