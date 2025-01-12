import hashlib
import os

from django.db import models

from .utils import Utils


class ShortLink(models.Model):
    original_url = models.CharField(max_length=512)
    passcode = models.CharField(max_length=64, blank=True, default='')
    salt = models.CharField(max_length=64, blank=True, default='')
    redirect_string = models.CharField(max_length=8)

    def encode_fields(self):
        if self.passcode:
            salt = os.urandom(16)
            self.original_url = Utils.encrypt_url(
                url=self.original_url, passcode=self.passcode, salt=salt
            )

            self.salt = salt.hex()
            self.passcode = hashlib.sha256(self.passcode.encode("utf-8")).hexdigest()

    def decode_url(self, passcode: str) -> str:
        if not self.passcode:
            return self.original_url

        encrypted_passcode = hashlib.sha256(passcode.encode("utf-8")).hexdigest()
        if encrypted_passcode != self.passcode:
            return "not same passcode"

        burl = bytes.fromhex(self.original_url)
        bsalt = bytes.fromhex(self.salt)
        decrypted_url = Utils.decrypt_url(url=burl, passcode=passcode, salt=bsalt)
        return decrypted_url
