import json
from wsgiref import headers
from flask_restx import Resource
from flask import request,render_template,make_response
from ..util.login_dto import LoginDto
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app
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
        from ..config import app
        try:
            data = json.loads(request.data)
            email = data["email"]
            # check email is exist to reset
            checkUserExist(email)
            token = jwt.encode(
             {"email": email},
            current_app.config["SECRET_KEY"],
               )
            # save otp number
            message = Mail(
                 from_email='scm.yehtetaung@gmail.com',
                 to_emails=email,
                 
                 subject='Sending with Twilio SendGrid is Fun',
                 html_content=f'<strong>Reset password link</strong><a href="http://127.0.0.1:5000/resetpassword?email={email}&token={token}">Click here</a>')
            try:
                sg = SendGridAPIClient('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')
                response = sg.send(message)
                print(token)
            except Exception as e:
                print(e.message)
            
            # createOTP(email)
            


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



