import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

def create_jwt_token(data: dict, expires_delta: timedelta):
    expiration = datetime.utcnow() + expires_delta
    data_to_encode = data.copy()
    data_to_encode.update({"exp": expiration})
    encoded_data = jwt.encode(data_to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_data

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None