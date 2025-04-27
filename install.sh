#!/bin/sh

# Detect Termux or Linux
if [ -n "$PREFIX" ] && [ "$(uname)" = "Linux" ]; then
    IS_TERMUX=true
else
    IS_TERMUX=false
fi

# Function to install packages
install_package() {
    if [ "$IS_TERMUX" = true ]; then
        pkg install -y "$1"
    else
        if command -v apt >/dev/null 2>&1; then
            sudo apt update && sudo apt install -y "$1"
        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y "$1"
        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -Sy --noconfirm "$1"
        else
            echo "Unsupported package manager. Install $1 manually."
            exit 1
        fi
    fi
}

# Check for python3
if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found. Installing..."
    install_package python3
else
    echo "python3 found."
fi

# Check for curl
if ! command -v curl >/dev/null 2>&1; then
    echo "curl not found. Installing..."
    install_package curl
else
    echo "curl found."
fi

# Check for rich Python library
if ! python3 -c "import rich" >/dev/null 2>&1; then
    echo "rich library not found. Installing..."
    python3 -m pip install --upgrade pip
    python3 -m pip install rich
else
    echo "rich library found."
fi

# Download passdroid.py
echo "Downloading passdroid.py..."
curl -L -o passdroid.py "https://raw.githubusercontent.com/funterminal/passdroid/refs/heads/main/passdroid.py"

# Detect if running as root
if [ "$(id -u)" -eq 0 ]; then
    IS_ROOT=true
else
    IS_ROOT=false
fi

# Handle installation
if [ "$IS_TERMUX" = false ] && [ "$IS_ROOT" = true ]; then
    echo "Installing passdroid.py to /usr/local/bin..."
    mv passdroid.py /usr/local/bin/passdroid
    chmod +x /usr/local/bin/passdroid
    echo "Installed! Run 'passdroid' to start."
else
    echo "Setting up alias in Termux or non-root Linux."

    # Detect shell
    SHELL_NAME="$(basename "$SHELL")"
    case "$SHELL_NAME" in
        bash)
            CONFIG_FILE="$HOME/.bashrc"
            ;;
        zsh)
            CONFIG_FILE="$HOME/.zshrc"
            ;;
        fish)
            CONFIG_FILE="$HOME/.config/fish/config.fish"
            ;;
        tcsh|csh)
            CONFIG_FILE="$HOME/.cshrc"
            ;;
        ksh)
            CONFIG_FILE="$HOME/.kshrc"
            ;;
        *)
            CONFIG_FILE="$HOME/.profile"
            ;;
    esac

    # Add alias
    if ! grep -q "alias passdroid=" "$CONFIG_FILE"; then
        echo "alias passdroid='python3 \$HOME/passdroid.py'" >> "$CONFIG_FILE"
        echo "Alias added to $CONFIG_FILE"
    else
        echo "Alias already exists in $CONFIG_FILE"
    fi

    chmod +x passdroid.py
    mv passdroid.py "$HOME/"
    echo "Setup done. Restart your shell or run 'source $CONFIG_FILE' to use 'passdroid'."
fi
