# Secure File Sharing System

A security-focused web application for securely uploading, storing, downloading, deleting, and sharing files between authenticated users.

The system uses encryption to protect files at rest and includes authentication, authorization, CSRF protection, file validation, upload size limits, and secure file-sharing controls.

## Features

- User registration and secure login
- Password hashing and minimum password length validation
- Authentication-protected pages
- CSRF protection for forms
- Secure POST-based logout
- File upload with a 10 MB size limit
- File extension and content validation
- Fernet encryption for files stored on the server
- Secure file download and decryption
- File deletion
- File sharing between registered users
- Download permission enforcement
- Automatic cleanup of file-sharing records when files are deleted
- User-friendly error handling
- Responsive dark-themed interface

## Technologies Used

- **Python** – Application programming language
- **Flask** – Web application framework
- **Flask-SQLAlchemy** – Database integration
- **Flask-Login** – User authentication and session management
- **Flask-WTF** – CSRF protection
- **SQLite** – Database
- **HTML/CSS** – Frontend interface
- **Cryptography (Fernet)** – File encryption and decryption
- **Werkzeug** – Secure password hashing and filename handling
- **python-dotenv** – Environment variable management
- **filetype** – File-content validation
- **Git & GitHub** – Version control and project hosting

## Project Structure

```text
secure-file-sharing/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── auth.py
│   ├── encryption.py
│   │
│   └── templates/
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── files.html
│       ├── shared_with_me.html
│       └── error.html
│
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Security

This project includes several security measures:

- Passwords are stored using secure password hashing.
- Passwords must contain at least 8 characters.
- Authentication is required for protected resources.
- CSRF protection is enabled for form submissions.
- Logout uses a POST request with CSRF protection.
- Uploaded files are limited to 10 MB.
- File extensions are checked against an allowed list.
- File contents are validated using file signatures.
- DOCX files are additionally checked for valid ZIP-based structure.
- Uploaded files are encrypted using Fernet before being stored.
- Users can only access their own files unless a file has been explicitly shared with them.
- File download permissions are enforced by the server.
- Shared-file records are removed when the original file is deleted.
- Secret keys are stored in environment variables and excluded from Git.
