import json
from flask_restx import Resource
from flask import request
from ..util.login_dto import LoginDto
from ..service.authentication_service import (
    generateToken,
    checkUserExist,
    resetPassword,
    createOTP,
    checkOTP,
)
from xml.dom import NotFoundErr, InvalidAccessErr

# imports for PyJWT authentication
import jwt

login_namespace = LoginDto.login_namespace
reset_password_namespace = LoginDto.reset_password_namespace
forgot_password_namespace = LoginDto.forgot_password_namespace


@login_namespace.route("/login")
class Login(Resource):
    @login_namespace.expect(LoginDto.login_request)
    def post(self):
        try:
            auth = json.loads(request.data)
            responseData = generateToken(auth)

        except IndentationError as e:
            return e.args, 400
        except NotFoundErr as e:
            return e.args, 401
        except InvalidAccessErr as e:
            return e.args, 403
        return responseData


@forgot_password_namespace.route("/retrieve")
class RetrieveEmail(Resource):
    @forgot_password_namespace.expect(LoginDto.retrieve_request)
    def post(self):
        try:
            data = json.loads(request.data)
            email = data["email"]
            # check email is exist to reset
            checkUserExist(email)
            # save otp number
            createOTP(email)

        except NotFoundErr as e:
            return e.args, 401

        return {"message": "email exist", "email": email}


@reset_password_namespace.route("/reset")
class ResetEmail(Resource):
    @reset_password_namespace.expect(LoginDto.reset_request)
    def post(self):
        try:
            resetData = json.loads(request.data)
            email = resetData["email"]
            otpNumber = resetData["otpnumber"]
            newPassword = resetData["newpassword"]
            confirmpassword = resetData["confirmpassword"]

            checkOTP(email, otpNumber)

            resetPassword(email, newPassword, confirmpassword)

        except InvalidAccessErr as e:
            return e.args, 401

        except ValueError as e:
            return e.args, 401

        return {"message": "password change"}
