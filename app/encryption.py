import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv()


encryption_key = os.getenv("ENCRYPTION_KEY")

if not encryption_key:
    raise ValueError("ENCRYPTION_KEY is not set in the .env file")


cipher = Fernet(encryption_key.encode())


def encrypt_file(file_data):
    return cipher.encrypt(file_data)


def decrypt_file(encrypted_data):
    return cipher.decrypt(encrypted_data)