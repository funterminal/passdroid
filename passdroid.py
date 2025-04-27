import argparse
import hashlib
import os
import secrets
import sys
import getpass
import shutil
import datetime
import subprocess
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

base_dir = os.path.expanduser("~/.passdroid")
password_file = os.path.join(base_dir, "password.hash")
expire_file = os.path.join(base_dir, "expire.date")
codes_file = os.path.join(base_dir, "codes.txt")

system_dir = "/etc/droid"
system_password_file = os.path.join(system_dir, "system.hash")
system_expire_file = os.path.join(system_dir, "system_expire.date")

def ensure_base_dir():
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, mode=0o700)

def ensure_system_dir():
    if not os.path.exists(system_dir):
        os.makedirs(system_dir, mode=0o700)

def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()

def password_exists():
    return os.path.exists(password_file)

def load_password_hash():
    if not password_exists():
        return None
    with open(password_file, "r") as f:
        return f.read().strip()

def check_password(input_password):
    stored_hash = load_password_hash()
    if not stored_hash:
        return False
    return hash_password(input_password) == stored_hash

def is_common_password(password):
    common = [
        '1234567890', 'password', 'qwerty', 'abc123', '111111', '123123', 'abc', '123456'
    ]
    return password in common

def check_quality(password):
    if len(password) < 12:
        return "Very Weak"
    if is_common_password(password):
        return "Common"
    strength = 0
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|" for c in password):
        strength += 1
    if strength == 4:
        return "Strong"
    elif strength == 3:
        return "Good"
    else:
        return "Medium"

def set_password(new_password):
    ensure_base_dir()
    if len(new_password) < 12:
        console.print("[bold red]Error:[/bold red] Password must be at least 12 characters.")
        sys.exit(1)
    if is_common_password(new_password):
        console.print("[bold red]Error:[/bold red] Password too common.")
        sys.exit(1)
    hashed = hash_password(new_password)
    with open(password_file, "w") as f:
        f.write(hashed)
    console.print("[bold green]Password successfully set.[/bold green]")

def set_expire(date_str):
    ensure_base_dir()
    with open(expire_file, "w") as f:
        f.write(date_str)
    console.print(f"[bold cyan]Password will expire on:[/bold cyan] {date_str}")

def check_expiry():
    if not os.path.exists(expire_file):
        return False
    with open(expire_file, "r") as f:
        expiry_date = f.read().strip()
    try:
        expiry = datetime.datetime.strptime(expiry_date, "%a %b %d %H:%M:%S %z %Y")
        now = datetime.datetime.now(datetime.timezone.utc)
        return now > expiry
    except Exception:
        return False

def generate_password():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[{]};:'\",<.>/?\\|"
    password = ''.join(secrets.choice(alphabet) for _ in range(24))
    console.print(f"[bold green]Generated Password:[/bold green] {password}")

def generate_codes(file_path):
    ensure_base_dir()
    codes = [secrets.token_hex(16) for _ in range(5)]
    with open(file_path, "w") as f:
        for code in codes:
            f.write(code + "\n")
    os.chmod(file_path, 0o600)
    console.print(f"[bold yellow]Recovery codes saved to {file_path}[/bold yellow]")

def remove_password():
    if not password_exists():
        console.print("[bold red]No password set.[/bold red]")
        return
    current = getpass.getpass("Enter current password: ")
    if not check_password(current):
        console.print("[bold red]Incorrect password.[/bold red]")
        sys.exit(1)
    if Confirm.ask("Do you want to set a new password?"):
        new = getpass.getpass("Enter new password: ")
        set_password(new)
    else:
        os.remove(password_file)
        if os.path.exists(expire_file):
            os.remove(expire_file)
        console.print("[bold green]Password removed.[/bold green]")

def update_shell_config():
    shell = os.path.basename(os.environ.get("SHELL", "bash"))
    shells = {
        "bash": ".bashrc",
        "zsh": ".zshrc",
        "ksh": ".kshrc",
        "csh": ".cshrc",
        "tcsh": ".tcshrc"
    }
    config = shells.get(shell)
    if not config:
        return
    config_path = os.path.expanduser(f"~/{config}")
    line = 'python3 ~/.passdroid/authenticate.py'
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write(f"{line}\n")
    else:
        with open(config_path, "r") as f:
            content = f.read()
        if line not in content:
            with open(config_path, "a") as f:
                f.write(f"\n{line}\n")
    console.print(f"[bold blue]Shell config updated ({config}) to require authentication on startup.[/bold blue]")

def create_auth_script():
    script_path = os.path.join(base_dir, "authenticate.py")
    script = f'''import hashlib
import getpass
import sys
import os
import datetime

password_file = os.path.expanduser("{password_file}")
expire_file = os.path.expanduser("{expire_file}")

def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()

def load_password_hash():
    if not os.path.exists(password_file):
        sys.exit(0)
    with open(password_file, "r") as f:
        return f.read().strip()

def check_expiry():
    if not os.path.exists(expire_file):
        return False
    with open(expire_file, "r") as f:
        expiry_date = f.read().strip()
    try:
        expiry = datetime.datetime.strptime(expiry_date, "%a %b %d %H:%M:%S %z %Y")
        now = datetime.datetime.now(datetime.timezone.utc)
        return now > expiry
    except Exception:
        return False

while True:
    password = getpass.getpass("Enter your system password: ")
    if hash_password(password) == load_password_hash():
        if check_expiry():
            print("Password expired. Please set a new password.")
            sys.exit(1)
        break
    else:
        print("Incorrect password. Try again.")
'''
    with open(script_path, "w") as f:
        f.write(script)
    os.chmod(script_path, 0o700)

def set_system_password(new_password):
    if os.geteuid() != 0:
        console.print("[bold red]Error: System password setup requires root privileges.[/bold red]")
        sys.exit(1)
    console.print("[bold red blink]WARNING: You are about to change the real Linux user password![/bold red blink]")
    confirm = Confirm.ask("[bold yellow]Are you absolutely sure you want to continue?[/bold yellow]")
    if not confirm:
        console.print("[bold red]Operation cancelled.[/bold red]")
        sys.exit(1)
    username = os.getenv("SUDO_USER") or os.getenv("USER")
    if not username:
        console.print("[bold red]Could not determine username.[/bold red]")
        sys.exit(1)
    if len(new_password) < 14:
        console.print("[bold red]Error:[/bold red] System password must be at least 14 characters.")
        sys.exit(1)
    if is_common_password(new_password):
        console.print("[bold red]Error:[/bold red] Password too common.")
        sys.exit(1)
    try:
        subprocess.run(["chpasswd"], input=f"{username}:{new_password}".encode(), check=True)
    except Exception as e:
        console.print(f"[bold red]Failed to set system password: {e}[/bold red]")
        sys.exit(1)
    ensure_system_dir()
    hashed = hash_password(new_password)
    with open(system_password_file, "w") as f:
        f.write(hashed)
    os.chmod(system_password_file, 0o600)
    console.print("[bold green]System password successfully updated.[/bold green]")

def main():
    parser = argparse.ArgumentParser(description="Passdroid - Advanced Password Manager")
    parser.add_argument("--set-password", type=str, help="Set a new password")
    parser.add_argument("--expire", type=str, help="Set password expiration date")
    parser.add_argument("--quality", type=str, help="Check password quality")
    parser.add_argument("--generate", nargs="?", const=True, help="Generate a strong password or recovery codes")
    parser.add_argument("--remove-password", action="store_true", help="Remove the current password")
    parser.add_argument("--generate-codes", type=str, help="Generate recovery codes to a file")
    parser.add_argument("--system", type=str, help="Set a system level password and change OS login")

    args = parser.parse_args()

    if args.set_password:
        set_password(args.set_password)
        create_auth_script()
        update_shell_config()
    elif args.expire:
        set_expire(args.expire)
    elif args.quality:
        quality = check_quality(args.quality)
        console.print(f"[bold magenta]Password Quality:[/bold magenta] {quality}")
    elif args.generate:
        if isinstance(args.generate, str):
            generate_codes(args.generate)
        else:
            generate_password()
    elif args.remove_password:
        remove_password()
    elif args.system:
        set_system_password(args.system)
    else:
        console.print("[bold red]No option selected. Use --help for available commands.[/bold red]")

if __name__ == "__main__":
    main()
