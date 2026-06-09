# 🧠 Self-Healing Test Automation Framework

A Selenium-based test automation framework that automatically heals broken locators and credentials using BeautifulSoup HTML parsing — no manual fixing needed.

---

## 📁 Folder Structure

```
self-healing-framework/
│
├── ai/
│   ├── __init__.py
│   ├── llm_client.py            # OpenAI integration for AI-powered locator suggestions
│   └── prompt_builder.py        # Prompt templates for LLM
│
├── core/
│   ├── __init__.py
│   ├── config.py                # Central config (URL, wait time, locator file path)
│   ├── driver_factory.py        # Chrome WebDriver setup (no webdriver-manager needed)
│   ├── element_actions.py       # find_element() with self-heal fallback + explicit waits
│   ├── locator_engine.py        # Read/write locators + credentials from JSON
│   ├── run_engine.py            # Orchestrates the full test run
│   └── self_healing_engine.py   # HTML parser to find best locator (skips hidden fields)
│
├── locators/
│   └── login_locators.json      # Stored locators + credentials (auto-updated on heal)
│
├── tests/
│   ├── __init__.py
│   └── test_login.py            # Login test with retry loop + credential healing
│
├── conftest.py                  # pytest fixture for WebDriver
├── requirements.txt
├── run.py                       # Entry point (run without pytest)
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ No need to install ChromeDriver separately.
> Selenium 4.6+ manages it automatically using Selenium Manager.
> Just make sure **Google Chrome** is installed on your system.

### 2. Set OpenAI API key (optional — only needed for AI-powered healing)
```bash
# Mac/Linux
export OPENAI_API_KEY=your_key_here

# Windows
set OPENAI_API_KEY=your_key_here
```

---

## ▶️ How to Run

### Option A — Direct run
```bash
python run.py
```

### Option B — Via pytest
```bash
pytest tests/test_login.py -v
```

### Option C — Pytest with logs visible
```bash
pytest tests/test_login.py -v -s
```

### Option D — Pytest with HTML report
```bash
pip install pytest-html
pytest tests/test_login.py -v -s --html=report.html --self-contained-html
```
Then open `report.html` in your browser for a full visual report.

---

## ✅ Expected Output (All Passing)

```
🚀 Starting test run...
🌐 Opening OrangeHRM login page...
✅ Page loaded successfully.

🔄 Login attempt 1 of 2...
✅ Username entered: Admin
✅ Password entered.
✅ Login button clicked.
✅ Login action completed. Dashboard loaded!
✅ All tests passed!
🔒 Browser closed.
```

---

## 🗂️ Locator JSON Format

All locators and credentials are stored in `locators/login_locators.json`:

```json
{
  "username":     { "type": "name",  "value": "username" },
  "password":     { "type": "name",  "value": "password" },
  "login_button": { "type": "xpath", "value": "//button[@type='submit']" },
  "credentials": {
    "username": "Admin",
    "password": "admin123"
  }
}
```

Supported locator types: `id`, `name`, `xpath`, `css`, `class`

> This file is **automatically updated** when self-healing kicks in.

---

## 🔁 How Self-Healing Works

### Locator Healing
```
find_element() called
       │
       ├── ✅ Element found → continue
       │
       └── ❌ Element not found / not interactable
                   │
                   ▼
          SelfHealingEngine scans page HTML
                   │
                   ▼
          Skips hidden fields, CSRF tokens
                   │
                   ▼
          Finds best locator:
          id > name > placeholder xpath > css
                   │
                   ▼
          Updates login_locators.json
                   │
                   ▼
          Retries with new locator
                   │
                   ▼
          ✅ Test continues
```

### Credential Healing
```
Login attempt 1
       │
       ├── ✅ Dashboard loaded → DONE
       │
       └── ❌ "Invalid credentials" error detected
                   │
                   ▼
          reset_credentials() called
                   │
                   ▼
          JSON reset to default: Admin / admin123
                   │
                   ▼
          Page reloaded → Login attempt 2
                   │
                   ├── ✅ Dashboard loaded → DONE
                   │
                   └── ❌ Still failing → Report error
```

---

## 🧪 How to Test All Scenarios

### ✅ Scenario 1 — Normal Login
No changes needed:
```bash
python run.py
```

---

### ❌ Scenario 2 — Wrong Password (Credential Self-Healing)
Break the password in `locators/login_locators.json`:
```json
"credentials": {
  "username": "Admin",
  "password": "WRONGPASSWORD"
}
```
Run `python run.py` — framework detects error, auto-resets to `admin123`, retries and passes. ✅

---

### ❌ Scenario 3 — Broken Username Locator
Break the username locator in `locators/login_locators.json`:
```json
"username": { "type": "name", "value": "BROKEN_FIELD" }
```
Run `python run.py` — framework scans HTML, finds correct locator, updates JSON, retries and passes. ✅

---

### ❌ Scenario 4 — Broken Login Button Locator
Break the button locator in `locators/login_locators.json`:
```json
"login_button": { "type": "xpath", "value": "//button[@type='BROKEN']" }
```
Run `python run.py` — framework finds the real button, updates JSON, passes. ✅

---

### ❌ Scenario 5 — Page Load Failure
Break the URL in `core/config.py`:
```python
BASE_URL = "https://thissitedoesnotexist99999.com/"
```
Run `python run.py` — shows clear error, browser stays open 5 seconds so you can see the state.
Revert `BASE_URL` after testing.

---

### ✅ Scenario 6 — Pytest HTML Report
```bash
pytest tests/test_login.py -v -s --html=report.html --self-contained-html
```
Open `report.html` in browser for visual test report.

---

---

## 🚀 Deploy to Render

### Quick Start
1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New +" → "Web Service"**
   - Connect your GitHub repo
   - Fill in these settings:

   | Setting | Value |
   |---------|-------|
   | **Name** | `self-healing-selenium` |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0` |
   | **Instance Type** | Standard (or higher) |

3. **Click "Create Web Service"** — Render will build and deploy automatically

4. **Access Your App**
   - Your app will be live at: `https://{your-service-name}.onrender.com`
   - Example: `https://self-healing-selenium.onrender.com`

### ✅ What's Pre-Configured
- ✅ **Headless Chrome**: Automatically enabled in `driver_factory.py`
- ✅ **Streamlit Web UI**: `app.py` runs the interactive dashboard
- ✅ **Dynamic Port Binding**: Render's `$PORT` environment variable
- ✅ **Network Sandbox**: `--no-sandbox` flag for containerized environment
- ✅ `.gitignore` & `.renderignore`: Keeps build small and fast

### 📌 Alternative: Use render.yaml
If you prefer, Render can read deployment config from `render.yaml`:
1. Commit the `render.yaml` file to your repo
2. In Render dashboard, select **"Use existing render.yaml"**
3. Deploy — Render uses the exact config from `render.yaml`

### ⚠️ Important Notes
- **Free tier**: 15-minute request timeout (adjust test timeouts if needed)
- **No display server**: Tests run headless (already configured)
- **Browser persistence**: Each request gets a fresh browser instance
- **Data storage**: Use external services for persistent data (not Render's ephemeral disk)

---

## 📋 All Failure Scenarios and Outputs

| Scenario | What Happens | Output |
|---|---|---|
| Page doesn't load | Timeout after 30s | `❌ Login page did not load within 30 seconds.` |
| Username field missing | Self-healing triggers | `⚠️ Element 'username' not interactable. Triggering self-healing...` |
| Password field missing | Self-healing triggers | `⚠️ Element 'password' not interactable. Triggering self-healing...` |
| Login button missing | Self-healing triggers | `⚠️ Element 'login_button' not interactable. Triggering self-healing...` |
| Wrong credentials | Auto-reset + retry | `🔧 Auto-healing credentials back to default...` |
| Dashboard doesn't load | Clear error with URL | `❌ Dashboard did not load. Current URL: ...` |
| Network issue | Exception caught | `❌ TEST FAILED UNEXPECTEDLY: connection error` |

---

## 🗂️ Quick Reference — What to Change Per Test

| Scenario | File | What to Change |
|---|---|---|
| Normal run | Nothing | Just run |
| Wrong password | `locators/login_locators.json` | Change `credentials.password` |
| Broken username locator | `locators/login_locators.json` | Change `username.value` to `"BROKEN_FIELD"` |
| Broken button locator | `locators/login_locators.json` | Change `login_button.value` to `"BROKEN"` |
| Page load failure | `core/config.py` | Change `BASE_URL` to fake URL |
| HTML report | Nothing | Run with `--html=report.html` |

---

## 📦 Requirements

```
selenium
openai
beautifulsoup4
lxml
pytest
pytest-html        # optional, for HTML reports
```

Install:
```bash
pip install -r requirements.txt
```

---

## 🧪 Test Site

- URL: https://opensource-demo.orangehrmlive.com/
- Username: `Admin`
- Password: `admin123`

---

## 🔑 Key Design Decisions

| Decision | Reason |
|---|---|
| No `webdriver-manager` | Avoids network errors on restricted systems; Selenium 4.6+ handles it natively |
| Explicit waits (`WebDriverWait`) | More reliable than `implicitly_wait` for JS-rendered pages |
| Credentials stored in JSON | Allows auto-reset without touching code |
| Skip hidden/CSRF inputs in healer | Prevents healing to wrong fields like `_token` |
| Retry loop (2 attempts) | Gives framework one chance to heal before reporting failure |
