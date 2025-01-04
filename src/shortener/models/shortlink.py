import hashlib
import os

from pydantic import BaseModel, HttpUrl

from src.shortener.utils import Utils


class LinkRequest(BaseModel):
    url: HttpUrl
    passcode: str | None = None

    def generate_shortlink(self):
        redirect_string = Utils.generate_redirect_string()
        shortlink = ShortLink(original_url=str(self.url), passcode=self.passcode, redirect_string=redirect_string)
        shortlink.encode_fields()

        return shortlink

class ShortLink(BaseModel):
    original_url: str
    passcode: str | None = None
    salt: str | None = None
    redirect_string: str

    def encode_fields(self):
        if self.passcode:
            salt = os.urandom(16)
            self.original_url = Utils.encrypt_url(url=self.original_url, passcode=self.passcode, salt=salt)

            self.salt = salt.hex()
            self.passcode = hashlib.sha256(self.passcode.encode('utf-8')).hexdigest()

    def decode_url(self, passcode: str) -> str:
        if not self.passcode:
            return self.original_url

        encrypted_passcode = hashlib.sha256(passcode.encode('utf-8')).hexdigest()
        if encrypted_passcode != self.passcode:
            return "not same passcode"

        burl = bytes.fromhex(self.original_url)
        bsalt = bytes.fromhex(self.salt)
        decrypted_url = Utils.decrypt_url(url=burl, passcode=passcode, salt=bsalt)
        return decrypted_url


