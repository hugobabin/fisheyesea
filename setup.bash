#!/bin/sh
set -e

# setup file for fisheyesea
# bash setup.bash

echo "🔧 Setting up project with uv..."

# install uv if not found
if ! command -v uv >/dev/null 2>&1; then
    echo 🌀 Installing uv...
    if command -v curl >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command -v wget >/dev/null 2>&1; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        echo "Error: need curl or wget to install uv." >&2
        exit 1
    fi
    # make sure the new uv is available
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "📦 Syncing project environment..."
uv sync

echo "📦 Creating config/.env..."
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")
cat > config/.env <<EOF
API_TOKEN=yoursecretkey
JWT_SECRET=${JWT_SECRET}
EOF

echo "📦 Creating data/ dir..."
chmod 777 data/

echo "✅ Setup complete!"
