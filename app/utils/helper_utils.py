from random import randint
from datetime import datetime, timedelta

def generate_otp():
    otp = str(randint(100000, 999999))
    expires = datetime.now() + timedelta(minutes=3)
    return {"otp": otp, "expires": expires}