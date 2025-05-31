# Lazy-Password-Manager
A cli python password manager.


Lazy Pass

Lazy Pass is a command-line password manager written in Python, designed to create, store, and recall password information securely. **This is an ongoing project actively being developed**, with Version 1 providing core functionality and plans for future enhancements like improved input validation, advanced CLI options, and bug fixes.

Status

Lazy Pass is in active development. Version 1 is functional but includes known limitations 

Contributions, feedback, and bug reports are welcome via GitHub issues to shape future releases.

## Features

**Password Storage**: Store website credentials (website, username, password) in a text file, organized as a nested    dictionary.
**Encryption**: Encrypt password files using the `cryptography` library’s Fernet (symmetric encryption) with generated   keys.
**Decryption**: Decrypt and view encrypted files using the corresponding key.
 **File Management**:
    Create new password files or overwrite existing ones.
    Load and read password files.
    Append new entries to files.
    Delete specific website/username entries.
    Password Validation**: Require passwords to be at least 8 characters and include special characters (`!`, `@`, `#`, `$`, `%`, `&`).
**Command-Line Interface**:
  Interactive menu for file creation, loading, and editing.
  CLI lookup for passwords (e.g., `python newpass.py passwords google.com`).  
  Error Handling**: Checks for file existence, permissions, and invalid inputs.

## Installation

### Prerequisites
  Python 3.6 or higher
  `cryptography` library

Future Improvements
Fix read_encrypt_file to support encrypted file reading.

Add reusable input validation (e.g., get_valid_input).

Support non-.ao domains in urls.

Implement addparse for advanced CLI options.

Add unit tests with unittest or pytest.






  
