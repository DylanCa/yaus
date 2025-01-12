import base64
import string, random

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Utils:
    @staticmethod
    def generate_redirect_string(length: int = 5) -> str:
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=length))

    @staticmethod
    def encrypt_url(url: str, passcode: str, salt: bytes) -> str:
        key = Utils._generate_key(passcode, salt)
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(url.encode())

        return encrypted_message.hex()

    @staticmethod
    def decrypt_url(url: bytes, passcode: str, salt: bytes) -> str:
        key = Utils._generate_key(passcode, salt)
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(url).decode()

        return decrypted_message

    @staticmethod
    def _generate_key(passcode: str, salt: bytes) -> bytes:
        key = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend(),
        )

        return base64.urlsafe_b64encode(key.derive(passcode.encode()))
