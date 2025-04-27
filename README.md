my project info to understand you my project well and I don't completely fully never need feedback and suggestions and pls don't gave me that:
# PassDroid - Advanced System Authentication Manager

## Overview

PassDroid is a robust command-line authentication manager designed to enhance system security by implementing password protection, expiration policies, and recovery mechanisms. It integrates with your shell environment to require authentication on startup and provides tools for secure password management.

## Key Features

- **Secure Password Storage**: Passwords are stored as SHA-512 hashes in a protected directory
- **Password Quality Enforcement**: Requires minimum 12-character passwords and checks against common passwords
- **Expiration Policies**: Set time-based password expiration dates
- **Recovery Codes**: Generate secure recovery codes for emergency access
- **Shell Integration**: Automatically adds authentication requirement to shell startup
- **Cross-Platform**: Works on both Linux systems and Termux (Android)
- **Password Generation**: Creates strong random passwords meeting security best practices
- **System Password Management**: Securely change Linux system passwords with synchronization (root required)

## Installation

PassDroid can be installed with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/funterminal/passdroid/refs/heads/main/install.sh | sh 
```

The installer will:
1. Check for and install required dependencies (Python 3, curl, rich Python library)
2. Download the latest version of PassDroid
3. Set up proper permissions
4. Configure shell integration

## Usage

### Setting a Password

```bash
passdroid --set-password "your_secure_password_here"
```

The password must be at least 12 characters and will be checked against common passwords.

### Setting Password Expiration

```bash
passdroid --expire "Fri Nov 24 12:00:00 +0000 2023"
```

Use standard date format for expiration time (timezone-aware).

### Checking Password Quality

```bash
passdroid --quality "password_to_check"
```

Returns one of: Very Weak, Common, Medium, Good, or Strong.

### Generating a Secure Password

```bash
passdroid --generatemy project info to understand you my project well and I don't completely fully never need feedback and suggestions and pls don't gave me that:
# PassDroid - Advanced System Authentication Manager

## Overview

PassDroid is a robust command-line authentication manager designed to enhance system security by implementing password protection, expiration policies, and recovery mechanisms. It integrates with your shell environment to require authentication on startup and provides tools for secure password management.

## Key Features

- **Secure Password Storage**: Passwords are stored as SHA-512 hashes in a protected directory
- **Password Quality Enforcement**: Requires minimum 12-character passwords and checks against common passwords
- **Expiration Policies**: Set time-based password expiration dates
- **Recovery Codes**: Generate secure recovery codes for emergency access
- **Shell Integration**: Automatically adds authentication requirement to shell startup
- **Cross-Platform**: Works on both Linux systems and Termux (Android)
- **Password Generation**: Creates strong random passwords meeting security best practices
- **System Password Management**: Securely change Linux system passwords with synchronization (root required)

## Installation

PassDroid can be installed with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/funterminal/passdroid/refs/heads/main/install.sh | sh 
```

The installer will:
1. Check for and install required dependencies (Python 3, curl, rich Python library)
2. Download the latest version of PassDroid
3. Set up proper permissions
4. Configure shell integration

## Usage

### Setting a Password

```bash
passdroid --set-password "your_secure_password_here"
```

The password must be at least 12 characters and will be checked against common passwords.

### Setting Password Expiration

```bash
passdroid --expire "Fri Nov 24 12:00:00 +0000 2023"
```

Use standard date format for expiration time (timezone-aware).

### Checking Password Quality

```bash
passdroid --quality "password_to_check"
```

Returns one of: Very Weak, Common, Medium, Good, or Strong.

### Generating a Secure Password

```bash
passdroid --generate
```

Generates a 24-character random password with mixed case, numbers, and symbols.

### Generating Recovery Codes

```bash
passdroid --generate-codes /path/to/save.txt
```

Creates 5 secure recovery codes stored in the specified file with restricted permissions.

### Removing Current Password

```bash
passdroid --remove-password
```

Allows removing or changing the current password after verification.

### Setting System Password (Linux)

```bash
sudo passdroid --system "new_secure_system_password"
```

**Warning**: This will change your actual Linux user password. Requirements:
- Must be run as root (use sudo)
- Minimum 14 characters
- Cannot be a common password
- Changes both system login and PassDroid authentication

## Security Implementation

- All passwords are hashed using SHA-512 before storage
- Configuration files stored in `~/.passdroid` with restricted permissions (700)
- System passwords stored in `/etc/droid` with root-only access
- Recovery codes generated using cryptographically secure methods
- Password quality enforcement prevents weak credentials
- Shell integration ensures authentication occurs before shell access

## Technical Details

- **Password Storage**: 
  - User passwords: SHA-512 hashes stored in `~/.passdroid/password.hash`
  - System passwords: SHA-512 hashes stored in `/etc/droid/system.hash` (root-only)
- **Expiration Tracking**: Dates stored in `~/.passdroid/expire.date`
- **Recovery Codes**: Saved to user-specified location with 600 permissions
- **Shell Integration**: Modifies shell rc file to require authentication on startup

## License

PassDroid is released under the MIT License. See the LICENSE file for full details.

## Contributing

Contributions are welcome. Please open issues or pull requests on the GitHub repository.

## Support

For support or security concerns, please open an issue on the project repository.
```

Generates a 24-character random password with mixed case, numbers, and symbols.

### Generating Recovery Codes

```bash
passdroid --generate-codes /path/to/save.txt
```

Creates 5 secure recovery codes stored in the specified file with restricted permissions.

### Removing Current Password

```bash
passdroid --remove-password
```

Allows removing or changing the current password after verification.

### Setting System Password (Linux)

```bash
sudo passdroid --system "new_secure_system_password"
```

**Warning**: This will change your actual Linux user password. Requirements:
- Must be run as root (use sudo)
- Minimum 14 characters
- Cannot be a common password
- Changes both system login and PassDroid authentication

## Security Implementation

- All passwords are hashed using SHA-512 before storage
- Configuration files stored in `~/.passdroid` with restricted permissions (700)
- System passwords stored in `/etc/droid` with root-only access
- Recovery codes generated using cryptographically secure methods
- Password quality enforcement prevents weak credentials
- Shell integration ensures authentication occurs before shell access

## Technical Details

- **Password Storage**: 
  - User passwords: SHA-512 hashes stored in `~/.passdroid/password.hash`
  - System passwords: SHA-512 hashes stored in `/etc/droid/system.hash` (root-only)
- **Expiration Tracking**: Dates stored in `~/.passdroid/expire.date`
- **Recovery Codes**: Saved to user-specified location with 600 permissions
- **Shell Integration**: Modifies shell rc file to require authentication on startup

## License

PassDroid is released under the MIT License. See the LICENSE file for full details.

## Contributing

Contributions are welcome. Please open issues or pull requests on the GitHub repository.

## Support

For support or security concerns, please open an issue on the project repository.
