#!/bin/bash
set -e

echo "Installing system dependencies (Chrome)..."
apt-get update -qq
apt-get install -y -qq wget gnupg unzip curl

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update -qq
apt-get install -y -qq google-chrome-stable

echo "Chrome version: $(google-chrome --version)"

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating Streamlit config..."
mkdir -p .streamlit
cat > .streamlit/credentials.toml << 'EOF'
[general]
email = ""
EOF

echo "Build complete!"
