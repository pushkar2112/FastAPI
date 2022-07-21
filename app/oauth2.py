from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET KEY
# ALGORITH
# EXPIRATION  TIME

SECRET_KEY = "f00d4251f3a3bc9c30c92e1e8cd8a5ae73c7edefb9e3463addb0ec8d717c2dbe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt