from time import time
from uuid import uuid4

import jwt


def create_jwt(private_key_path: str,
               client_id: str,
               claims: dict = {},
               headers: dict = {},
               algorithm: str = "RS512"):
    with open(private_key_path, "r") as f:
        private_key = f.read()

        _claims = {
            "sub": client_id,
            "iss": client_id,
            "jti": str(uuid4()),
            "exp": int(time()) + 5,
        }
        claims = {**_claims, **claims}

        return jwt.encode(claims, private_key, algorithm=algorithm, headers=headers)
