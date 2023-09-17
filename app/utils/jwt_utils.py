from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
import os
from app.schema.schemas import super_user_serializer
from app.db.db import db
from dotenv import load_dotenv
load_dotenv()

superuser_col = db['superusers']
staffuser_col = db['staffusers']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    
async def check_user_exists(userId: str):
    """
    Check if a user exists.
    """
    find_superuser = superuser_col.find_one({"$or": [{"username": userId}, {"email": userId}]})
    if find_superuser:
        return {
            "roles": ["superuser"],
            **super_user_serializer(find_superuser)
        }
    else:
        find_staffuser = staffuser_col.find_one({"$or": [{"username": userId}, {"email": userId}]})
        if find_staffuser:
            return find_staffuser
        else:
            return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from a JWT token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        payload: dict = payload.get("sub")
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = await check_user_exists(username)
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

