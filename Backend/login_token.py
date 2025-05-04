from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

import objects


SECRET_KEY = 'f02a5a3d33a5e1aca7234ca644f84efe3049fb890ecf78a152e78a4d43a2aaf3'
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
       expire = datetime.now(timezone.utc) + timedelta(expires_delta)
    else:
       expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


async def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('email')
        if email is None:
            raise credentials_exception
        token_data = objects.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception

    return token_data
