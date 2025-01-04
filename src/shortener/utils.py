import string, random


class Utils:
    @staticmethod
    def generate_redirect_string(length: int = 5) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))