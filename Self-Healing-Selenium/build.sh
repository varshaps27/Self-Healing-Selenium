#!/bin/bash
set -e

echo "========================================="
echo " Self-Healing Selenium - Build Script"
echo "========================================="

echo ""
echo ">>> Step 1: Installing system packages..."
apt-get update -qq
apt-get install -y -qq wget gnupg unzip curl ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 \
    libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
    libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
    libxrandr2 libxrender1 libxss1 libxtst6 xdg-utils

echo ""
echo ">>> Step 2: Installing Google Chrome..."
wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y -qq /tmp/chrome.deb || apt-get install -y -qq -f
rm /tmp/chrome.deb

CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
echo ">>> Chrome installed: $CHROME_VERSION"

echo ""
echo ">>> Step 3: Installing ChromeDriver..."
CHROME_MAJOR=$(echo $CHROME_VERSION | cut -d. -f1)
CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"

# Try exact version first, fall back to latest stable
if wget -q --spider "$CHROMEDRIVER_URL" 2>/dev/null; then
    wget -q -O /tmp/chromedriver.zip "$CHROMEDRIVER_URL"
else
    echo ">>> Exact version not found, fetching latest stable..."
    LATEST_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_MAJOR}")
    wget -q -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${LATEST_URL}/linux64/chromedriver-linux64.zip"
fi

unzip -q /tmp/chromedriver.zip -d /tmp/chromedriver_dir
mv /tmp/chromedriver_dir/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
rm -rf /tmp/chromedriver.zip /tmp/chromedriver_dir

echo ">>> ChromeDriver installed: $(chromedriver --version)"

echo ""
echo ">>> Step 4: Setting environment variables..."
export GOOGLE_CHROME_BIN=$(which google-chrome)
export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

echo ""
echo ">>> Step 5: Installing Python dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ""
echo ">>> Step 6: Streamlit config..."
mkdir -p .streamlit
cat > .streamlit/credentials.toml << 'EOF'
[general]
email = ""
EOF

cat > .streamlit/config.toml << 'EOF'
[theme]
base = "dark"
primaryColor = "#2563eb"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#e2e8f0"

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
EOF

echo ""
echo "========================================="
echo " Build Complete!"
echo " Chrome:      $GOOGLE_CHROME_BIN"
echo " ChromeDriver: $CHROMEDRIVER_PATH"
echo "========================================="
