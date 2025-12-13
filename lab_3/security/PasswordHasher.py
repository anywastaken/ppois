
import hashlib

class PasswordHasher:
    def hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, plain: str, hashed: str) -> bool:
        return self.hash(plain) == hashed