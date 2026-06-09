# 🧠 Self-Healing Test Automation Framework

A Selenium-based test automation framework that automatically heals broken locators using BeautifulSoup HTML parsing.

---

## 📁 Folder Structure

```
self-healing-framework/
│
├── ai/
│   ├── __init__.py
│   ├── llm_client.py        # OpenAI integration for AI-powered locator suggestions
│   └── prompt_builder.py    # Prompt templates for LLM
│
├── core/
│   ├── __init__.py
│   ├── config.py            # Central config (URL, wait time, locator file path)
│   ├── driver_factory.py    # Chrome WebDriver setup
│   ├── element_actions.py   # find_element() with self-heal fallback
│   ├── locator_engine.py    # Read/write locators from JSON
│   ├── run_engine.py        # Orchestrates the full test run
│   └── self_healing_engine.py  # HTML parser to find best locator
│
├── locators/
│   └── login_locators.json  # Stored locators (auto-updated on heal)
│
├── tests/
│   ├── __init__.py
│   └── test_login.py        # Login test
│
├── conftest.py              # pytest fixture for WebDriver
├── run.py                   # Entry point (run without pytest)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API key (optional — only needed for AI-powered healing)
```bash
# Mac/Linux
export OPENAI_API_KEY=your_key_here

# Windows
set OPENAI_API_KEY=your_key_here
```

---

## ▶️ Run the Tests

### Option A — Direct run (no pytest)
```bash
python run.py
```

### Option B — Via pytest
```bash
pytest tests/test_login.py -v
```

---

## 🔁 How Self-Healing Works

```
Test runs
   │
   ▼
find_element() called
   │
   ├── ✅ Element found → continue test
   │
   └── ❌ NoSuchElementException
            │
            ▼
       SelfHealingEngine scans page HTML
            │
            ▼
       Finds best locator (id > name > css > xpath)
            │
            ▼
       Updates login_locators.json automatically
            │
            ▼
       Retries find_element with new locator
            │
            ▼
       ✅ Test continues
```

---

## 🗂️ Locator JSON Format

```json
{
  "username":     { "type": "name",  "value": "username" },
  "password":     { "type": "name",  "value": "password" },
  "login_button": { "type": "xpath", "value": "//button[@type='submit']" }
}
```

Supported types: `id`, `name`, `xpath`, `css`, `class`

---

## 🧪 Test Site
Uses the free demo site: https://opensource-demo.orangehrmlive.com/
- Username: `Admin`
- Password: `admin123`
