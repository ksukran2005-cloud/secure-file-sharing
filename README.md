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

> **Note:** The `.env` file, virtual environment, database files, and uploaded files are excluded from GitHub using `.gitignore`.

## Security

This project includes several security measures to protect user accounts and uploaded files:

- Passwords are securely hashed using Werkzeug.
- A minimum password length of 8 characters is enforced.
- Login is required to access protected pages and files.
- CSRF protection is enabled for forms.
- Logout uses a secure POST request with CSRF protection.
- Uploaded files are limited to 10 MB.
- File extensions and file contents are validated.
- DOCX files are checked for valid ZIP structure.
- Uploaded files are encrypted using Fernet encryption.
- Only file owners can delete or share their files.
- Shared files can only be downloaded by authorized users.
- Deleted files are also removed from the sharing records.
- Secret keys are stored in environment variables instead of GitHub.

## How It Works

The Secure File Sharing System follows a simple workflow:

1. The user creates an account and logs in securely.
2. The user uploads a file through the web interface.
3. The uploaded file is validated for size, extension, and file content.
4. The file is encrypted using Fernet encryption before being stored.
5. File information is stored in the SQLite database.
6. The file owner can download, delete, or share the file with another registered user.
7. A shared user can access the file only if the required permission is available.
8. During download, the encrypted file is decrypted and sent to the authorized user.

## File Encryption

Uploaded files are encrypted before they are stored on the server.

The system uses **Fernet symmetric encryption** from the Python `cryptography` library. The encryption key is stored securely in the `.env` file and is not uploaded to GitHub.

When a user downloads an authorized file, the system decrypts the file and returns the original file to the user.

This ensures that the files stored in the `uploads` directory are not kept in their original readable form.

## Supported File Types

The system currently supports the following file types:

- `.txt` — Text files
- `.pdf` — PDF documents
- `.png` — PNG images
- `.jpg` / `.jpeg` — JPEG images
- `.docx` — Microsoft Word documents

Files are checked using both their file extension and actual file content before they are accepted for upload.

## File Sharing

The system allows users to securely share uploaded files with other registered users.

The file owner can enter another user's username and share the file with them. The shared user can access the file from the **Shared With Me** page.

Each file share has a permission level. Currently, the system supports **download permission**, which allows the authorized user to download the shared file.

Only the file owner can share or delete their files.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ksukran2005-cloud/secure-file-sharing.git
cd secure-file-sharing
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory and add the required secret keys:

```text
SECRET_KEY=your-secret-key
ENCRYPTION_KEY=your-fernet-encryption-key
```

### 6. Run the Application

```bash
python run.py
```

Open the application in your browser at:

```text
http://127.0.0.1:5000
```

## Testing Performed

The following features were tested during development:

- User registration and password validation
- User login and logout
- Protected page access
- File upload and encryption
- File type and content validation
- File size limit validation
- File download and decryption
- File deletion
- File sharing between users
- Shared file download permissions
- CSRF protection on forms
- Unauthorized file access prevention
- Cleanup of file sharing records after deletion

## Future Improvements

The project can be further improved by adding:

- Stronger password requirements and account security.
- Email verification and password reset functionality.
- File preview for supported document and image formats.
- More flexible file permissions such as view and edit.
- Downloading large files using streaming instead of loading them fully into memory.
- Rate limiting to reduce brute-force login attempts.
- Improved user interface and responsive design.
- Deployment on a secure cloud server.
- Security logging and activity monitoring.

## Project Status

The Secure File Sharing System is a working portfolio project.

The core features, including user authentication, secure file upload, encryption, file management, and file sharing, have been implemented and tested successfully.

## Author

**Sukran K**

Computer Science and Engineering Student

GitHub: https://github.com/ksukran2005-cloud