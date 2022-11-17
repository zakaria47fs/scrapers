from base64 import b64decode
from functools import wraps

from Crypto.PublicKey import RSA
from fastapi import HTTPException

from utils.constant import ROOT_DIR


def authorize_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            key = kwargs["request"].headers.get('private_key')
            pem_key = bytes(key.encode('utf-8'))
            key = b64decode(pem_key)
            keyPriv = RSA.importKey(key)
            modulusN = keyPriv.n
            pubExpE = keyPriv.e
            priExpD = keyPriv.d
            primeP = keyPriv.p
            primeQ = keyPriv.q
            private_key = RSA.construct((modulusN, pubExpE, priExpD, primeP, primeQ))
            public_key = private_key.publickey().exportKey()
            public_key_start_comment = '-----BEGIN PUBLIC KEY-----'
            public_key_end_comment = '-----END PUBLIC KEY-----'
            public_key = str(public_key.decode('utf-8')).replace('\n', '').replace(public_key_start_comment, '').replace(
                public_key_end_comment, '').replace(' ', '')
            with open(ROOT_DIR / "public.pem", "rb") as file:
                pub_key = file.read()
            if public_key == pub_key.decode("utf-8"):
                return f(*args, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Not authorized")
        except:
            raise HTTPException(status_code=405, detail="Not authorized")
    return decorator
