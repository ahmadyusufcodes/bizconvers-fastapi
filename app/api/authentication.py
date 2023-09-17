from datetime import datetime, timedelta
from random import randint

from pydantic import BaseModel
from app.schemas import UserCredentials
from app.utils.helper_utils import generate_otp
from app.utils.perms_utils import verify_super_admin
from app.db.db import db
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_jwt_token, verify_jwt_token
from app.company.models import SuperUser, SuperUserOut, SuperUserRegister
from app.staff.models import Staff
from fastapi import APIRouter, Depends, HTTPException, Request, status
from bson import ObjectId
from app.utils.request_utils import response
from app.utils.mail import send_email
from app.schema.schemas import permission_serial, role_serial, super_user_insert_serializer, super_user_serializer

router = APIRouter()

superuser_col = db["superuser"]
staff_col = db["staff"]
company_col = db["company"]
branch_col = db["branch"]

def authenticate_user(email: str, password: str):
    try:
        super_user = superuser_col.find_one({"email": email})
        staff_user = staff_col.find_one({"email": email})
        if super_user and verify_password(password, super_user["password"]):
            return {"roles": ["superuser"], "sub": super_user_serializer(super_user)}
        elif staff_user and verify_password(password, staff_user["password"]):
            return staff_user
        else:
            return "Invalid credentials"
    except Exception as e:
        return str(e)

@router.post("/login")
async def login(userCreds: UserCredentials):
    userCreds = userCreds.dict()
    user = authenticate_user(userCreds["email"], userCreds["password"])
    if user != "Invalid credentials":
        token_data = user
        access_token_expires = timedelta(days=30)
        access_token = create_jwt_token(token_data, access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@router.post("/register")
async def register(super_user: SuperUserRegister):
    superuser_col.find_one_and_delete({})
    super_user = super_user.dict()
    super_user = super_user_insert_serializer(super_user)
    user = superuser_col.find_one({"email": super_user["email"]})
    try:
        if user:
            return response(status_code=400, message="A user exists with the same Email", data=None)
        else:
            hashed_password = hash_password(super_user["password"])
            super_user["password"] = hashed_password
            user_id = superuser_col.insert_one(super_user).inserted_id
            otp = generate_otp()
            find_user = superuser_col.find_one_and_update({"_id": user_id}, {"$set": {"otp": otp}}, return_document=True)
            try:
                send_email("OTP for Rumbu", f"<p>Your OTP is {otp['otp']}</p>", [find_user["email"]])
            except Exception as e:
                print(e)
            return response(status_code=200, message=f"An OTP has been sent to {super_user['email']}", data=super_user_serializer(find_user))
    except Exception as e:
        return response(status_code=500, message="Internal server error", data=str(e))
class OTP(BaseModel):
    otp: str
    email: str
@router.post("/verify-superuser")
async def verify_superuser(otp: OTP):
    otp = otp.dict()
    email, otp = otp["email"], otp["otp"]
    user = superuser_col.find_one({"email": email})
    if user:
        if user["otp"]["expires"] < datetime.now():
            return response(status_code=400, message="OTP has expired", data=None)
        if user["otp"]["otp"] == otp:
            superuser_col.find_one_and_update({"email": email}, {"$set": {"verified": True, "otp": {"otp": "", "expires": ""}}}, return_document=False)
            send_email("Welcome to Rumbu", f"<p>Your account has been verified successfully</p>", [user["email"]])
            find_superuser = superuser_col.find_one({"email": email})
            return response(status_code=200, message="OTP verified successfully", data=super_user_serializer(find_superuser))
        else:
            return response(status_code=400, message="OTP is incorrect", data=None)
    else:
        return response(status_code=400, message="User not found", data=None)

@router.post("/verify-otp")
async def verify_otp(email: str, otp: str):
    user = superuser_col.find_one({"email": email})
    if user:
        if user["otp"]["otp"] == otp:
            return response(status_code=200, message="OTP verified successfully", data=user)
        else:
            return response(status_code=400, message="OTP is incorrect", data=None)
    else:
        return response(status_code=400, message="User not found", data=None)

class OTPReq(BaseModel):
    email: str

@router.post("/send-otp")
async def send_otp(otp_req: OTPReq):
    email = otp_req.dict()["email"]
    user = superuser_col.find_one({"email": email})
    if user:
        otp = generate_otp()
        find_user = superuser_col.find_one_and_update({"email": email}, {"$set": {"otp": otp}}, return_document=True)
        try:
            send_email("OTP for Rumbu", f"<p>Your OTP is {otp['otp']}</p>", [find_user["email"]])
        except Exception as e:
            print(e)
        return response(status_code=200, message="OTP sent successfully", data=super_user_serializer(user))
    else:
        return response(status_code=400, message="User not found", data=None)
    
@router.post("/forgot-password")
async def forgot_password(email: str):
    user = superuser_col.find_one({"email": email})
    if user:
        otp = generate_otp()
        find_user = superuser_col.find_one_and_update({"email": email}, {"$set": {"otp": otp}}, return_document=True)
        try:
            send_email("OTP for Rumbu", f"<p>Your OTP is {otp['otp']}</p>", [find_user["email"]])
        except Exception as e:
            print(e)
        return response(status_code=200, message="OTP sent successfully", data=user)
    else:
        return response(status_code=400, message="User not found", data=None)
    
@router.post("/reset-password")
async def reset_password(email: str, otp: str, password: str):
    user = superuser_col.find_one({"email": email})
    if user:
        if user["otp"]["otp"] == otp:
            hashed_password = hash_password(password)
            superuser_col.find_one_and_update({"email": email}, {"$set": {"password": hashed_password, "otp": {"otp": "", "expires": ""}}}, return_document=False)
            send_email("Password reset", f"<p>Your password has been reset successfully</p>", [user["email"]])
            return response(status_code=200, message="Password reset successfully", data=None)
        else:
            return response(status_code=400, message="OTP is incorrect", data=None)
    else:
        return response(status_code=400, message="User not found", data=None)
    

@router.get("/protected")
async def protected_route(request: Request = Depends(verify_super_admin)):
    return response(status_code=200, message="This is a protected route!", data=True)