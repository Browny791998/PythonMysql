import json
from xml.dom import NotFoundErr
from flask_restx import Resource
from flask import request
from ..service.user_service import (
    saveUser,
    modifyUser,
    deleteById,
    getAllUser,
    getUserById
)
from ..util.user_dto import UserDto
from marshmallow import ValidationError

user_namespace = UserDto.user_namespace


@user_namespace.route("/get/<int:id>")
class getUser(Resource):
    @user_namespace.doc(security="api_key")
    def get(self, id):
        return getUserById(id)

@user_namespace.route("/getAll")
class getUserList(Resource):
    @user_namespace.doc(security="api_key")
    def get(self):
        return getAllUser()


@user_namespace.route("/create")
@user_namespace.expect(UserDto.user)
class createUser(Resource):
    @user_namespace.doc(security="api_key")
    def post(self):

        try:

            saveUser(json.loads(request.data))
        except ValueError as e:
            return e.args, 409
        except ValidationError as e2:
            print(e2.args)
            return e2.args, 400

        return "Successully Saved"


@user_namespace.route("/delete/<int:id>")
class deleteUser(Resource):
    @user_namespace.doc(security="api_key")
    def delete(self, id):
        try:
            deleteById(id)
        except NotFoundErr as e:
            return e.args, 400
        return "Successully Deleted"


@user_namespace.route("/update/<int:id>")
@user_namespace.expect(UserDto.user)
class updateUser(Resource):
    @user_namespace.doc(security="api_key")
    def put(self, id):
        try:
            modifyUser(id, json.loads(request.data))
        except ValueError as e:
            return e.args, 409
        except ValidationError as e2:
            return e2.args, 400
        except NotFoundErr as e3:
            return e3.args, 400
        return "Successully Updated"
