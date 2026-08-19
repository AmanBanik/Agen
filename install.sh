#!/bin/bash
set -e

echo -e "\033[1;32m      ▄▄████▄▄      \033[0m"
echo -e "\033[1;32m    ▄██████████▄    \033[0m"
echo -e "\033[1;33m   ████▀▀  ▀▀████   \033[0m"
echo -e "\033[1;33m  ████        ████  \033[0m"
echo -e "\033[0;33m ██████████████████ \033[0m"
echo -e "\033[0;33m█████▀▀▀▀▀▀▀▀▀▀█████\033[0m"
echo -e "\033[0;31m████            ████\033[0m"
echo -e "\033[0;31m███              ███\033[0m\n"

echo -e "\033[1;36mInitializing Agen V2 Autonomous Swarm Setup (macOS/Linux)...\033[0m\n"

if ! command -v git &> /dev/null; then
    echo -e "\033[1;31m[ERROR] git could not be found. Please install git.\033[0m"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;31m[ERROR] python3 could not be found. Please install Python 3.10+.\033[0m"
    exit 1
fi

TARGET_DIR="$HOME/.agen-src"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/AmanBanik/Agen.git"

if [ -d "$TARGET_DIR" ]; then
    echo -e "\033[1;33m>>> Removing existing source...\033[0m"
    rm -rf "$TARGET_DIR"
fi

echo -e "\033[1;33m>>> Cloning repository...\033[0m"
git clone --branch v2-stable --depth 1 "$REPO_URL" "$TARGET_DIR" > /dev/null 2>&1

echo -e "\033[1;33m>>> Building isolated Python environment...\033[0m"
python3 -m venv "$TARGET_DIR/venv"

echo -e "\033[1;33m>>> Installing dependencies (this may take a moment)...\033[0m"
"$TARGET_DIR/venv/bin/pip" install --quiet -e "$TARGET_DIR"

echo -e "\033[1;33m>>> Linking executable...\033[0m"
mkdir -p "$BIN_DIR"
ln -sf "$TARGET_DIR/venv/bin/agen" "$BIN_DIR/agen"

echo -e "\033[1;32m>>> Binary linked to $BIN_DIR/agen\033[0m"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "\n\033[1;31m⚠️  WARNING: $BIN_DIR is not in your PATH.\033[0m"
    echo -e "To use the 'agen' command, you must add it to your PATH by running:"
    echo -e "\033[1mexport PATH=\"\$HOME/.local/bin:\$PATH\"\033[0m"
    echo -e "(Add that line to your ~/.bashrc or ~/.zshrc file to make it permanent)\n"
fi

echo -e "\033[1;36m=========================================================\033[0m"
echo -e "\033[1;32mInstallation Complete!\033[0m"
echo -e "\033[1;37mYou can now type 'agen' in your terminal to start the swarm.\033[0m"
echo -e "\033[1;36m=========================================================\033[0m\n"
