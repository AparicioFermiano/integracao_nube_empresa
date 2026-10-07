from requests.auth import AuthBase
import hashlib
import base64


class AuthAD(AuthBase):
    """Assina cada requisição à Nube com o cabeçalho security-hash."""
    def __init__(self, url: str, query: str):
        self.SECRET = '<SECRET>'
        self.TOKEN = '<TOKEN>'
        self.URL_REQUEST = url
        self.QUERY_REQUEST = query

    def __call__(self, r):
        """Adiciona o security-hash no header."""
        hash_sha = hashlib.sha256(
            (self.URL_REQUEST + self.SECRET + self.QUERY_REQUEST).encode()
        ).hexdigest()

        security_hash = base64.b64encode(
            f"{self.TOKEN}:{hash_sha}".encode()
        ).decode()

        r.headers['security-hash'] = security_hash
        return r
