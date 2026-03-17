import os

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except:
    os.system("pip install cryptography")

import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import binascii

backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


def is_b64e(s):
    try:
        b64d(s)
        return True
    except binascii.Error:
        return False



test = """`8801705814293`

`b'NMqOXuPROQXvEdaLRXHDrgABhqCAAAAAAGhNm0pVVq3o7YqYYumh4QFJY_NrS_DfDpSQTKVVYSOTgw9iAXLVLJxKzmLSnVXyEq5sdyfNOtP4o5DmcttHh-XAaOkYXXHJG7jgo4ZOwUBMgAnnIFIcYd5SrjpKgYKu4iFvc-irG-lsbsI4MtogFb8N5IGMnVWL_nkZ0fstnW8zjnvjZsnrU1imIhSItAid527xNGtNMkmFH9jIoIh5G1Jr_KlgaMNcLmZxtzbzKStfKfansIhha8Ut7kzZAPPvD1DNxVds2dDrbJZYrrPULAe2QhctvTR7vEbw2br24pCS6dC3StSzVfOAOppOsdZnlthOTY8OU3xvD3LHqV1NTYpOJCrgX7sbnvrJbmtEY96qayWanzvKNMsIW4WgFgCTkWftNz7hP7FlghKAFYM75-JKRGIv6AZo4vsj4fq4zK4zQUBXagVAHhyjWkRh3s7LVFDsBLKm96IoS0e8YNC3mwFphecV4-lTS-04_6RygyekFqzc1N-cKD5YQmXi0bt9yYSaTDaESxMyhPehpjUVE63Y_sg-NwjddI48jhcgidPwf8nDKQ=='`

💁‍♂️ Developer @k_ofcl✌️

ssn = test.split('\n\n')[1].replace("`", "").replace("b'", "").replace("'", "")

#print(f"{ssn}\n\n")

print(is_b64e(ssn))

ttt = '1BVtsOJoBuxOXjNNphZ0_lkRXfR6C0LlvsYcffR-uGklzkpdDAZMgJWEPPPYn_0AyAjTxANHIn5daNsER5n5EQnMpmR88NF18MKJiyA5bePhdUScTHdDc8-TIAZqHPAlOeJm_9W59XlG03ID_2j8qOcjvc1XP93Nv6DwCk_t3S3EQCxuWd4EMbvgu5wVbchTEoa-xlFQzzSWmOIA8m4larzJQPe-eQBgGk3DSusRflpSxJCMcMQKEXtvNlzL7KCecT_gdmwXqnplyZiFLWJZdFNORNSG0SZVmMSOq5DWuq1kCLItvCffVL2li2WI4NqPxli_hxbeSKkeWZyshWGqKbe0RpOCvFYI='
try:
    res = password_decrypt(ttt.encode(), 'KsP@542543').decode()
except:
    pass
print(f"{res}")
"""
