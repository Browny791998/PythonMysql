from ..model.db_model import User
from xml.dom import NotFoundErr,InvalidAccessErr
import jwt
from datetime import datetime,timedelta
from .user_service import(
    getUserByEmail,
    updatePasswordByEmail,
    updateOTPByEmail
)

from .mail_service import sendEmail
from flask import current_app


import math,random

def generateToken(auth):

    # check auth data is complete
    if not auth or not auth.get("email") or not auth.get("password"):
        raise IndentationError("Imcomplete data")

    user = getUserByEmail(auth["email"])

    authPassword = auth["password"]
    # check auth email is exist
    if not user:
        raise NotFoundErr("email do not exist")
    # check auth password match
    if authPassword != user["password"]:
        raise InvalidAccessErr("wrong password")

    # generateToken
    token = jwt.encode(
        {"email": user["email"], "exp": datetime.utcnow() + timedelta(minutes=800)},
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    #get user name
    userName=user["user_name"]

    #construct employee object
    responseData={
        'name':userName,
        'token':token
    }

    return responseData


def checkUserExist(email):
    employee = getUserByEmail(email)
    if not employee:
        raise NotFoundErr("Email do not exist")


def resetPassword(email, newPassword, confirmpassword):
    print(email)
    if newPassword != confirmpassword:
        raise InvalidAccessErr("mismatch password")
    try:
        updatePasswordByEmail(email, newPassword)
    except ValueError:
        raise ValueError("Please enter new password")


def createOTP(email):
    otpNumber = generateOTP()
    
    updateOTPByEmail(email, otpNumber)
    sendEmail(email, otpNumber)


# function to generate OTP
def generateOTP():

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def checkOTP(email, otp):
    user= getUserByEmail(email)
    if user["otp_number"] != otp:
        raise ValueError("Otp is Invalid")


   


