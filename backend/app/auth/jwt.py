import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
        )

        return payload
    
    except JWTError:
        return None
