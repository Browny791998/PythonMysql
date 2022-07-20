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

from ..service.user_service import(
    saveTokenByEmail
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
            algorithm="HS256",)
            saveTokenByEmail(email,token)
            # save otp number
            # message = Mail(
            #      from_email='scm.yehtetaung@gmail.com',
            #      to_emails=email,
                 
            #      subject='Sending with Twilio SendGrid is Fun',
            #      html_content=f'<strong>Reset password link</strong><a href="http://127.0.0.1:5000/resetpassword?email={email}&token={token}">Click here</a>')
            # try:
            #     sg = SendGridAPIClient('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')
            #     response = sg.send(message)
            #     print(token)
            # except Exception as e:
            #     print(e.message)
            
            # createOTP(email)
            


        except NotFoundErr as e:
            return e.args, 401

        return {"message": "email exist", "email": email,"token":token}
        


@reset_password_namespace.route("/reset")
class ResetEmail(Resource):
    @reset_password_namespace.expect(LoginDto.reset_request)
    def post(self):
        try:
            resetData = json.loads(request.data)
            token = resetData["token"]
            newPassword = resetData["newpassword"]
            confirmpassword = resetData["confirmpassword"]
            data = jwt.decode(
                token,current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            checkUserExist(data['email'])
            email = data['email']
            resetPassword(email,newPassword,confirmpassword)
            # checkToken(email, token)

            # resetPassword(email, newPassword, confirmpassword)

        except InvalidAccessErr as e:
            return e.args, 401

        except ValueError as e:
            return e.args, 401

        return {"message": "password change"}



