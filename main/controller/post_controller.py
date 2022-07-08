import json
from xml.dom import NotFoundErr
from flask_restx import Resource
from flask import request
from ..service.post_service import (
    savePost,
    modifyPost,
    deleteById,
    getAllPost,
    getPostById
)
from ..util.post_dto import PostDto
from marshmallow import ValidationError
from ..service.token_service import token_required
post_namespace = PostDto.post_namespace


@post_namespace.route("/get/<int:id>")
class getPost(Resource):
    @token_required
    @post_namespace.doc(security="api_key")
    def get(self, id):
        return getPostById(id)

@post_namespace.route("/getAll")
class getPostList(Resource):
    @token_required
    @post_namespace.doc(security="api_key")
    def get(self):
        return getAllPost()


@post_namespace.route("/create")
@post_namespace.expect(PostDto.post)
class createPost(Resource):
    @token_required
    @post_namespace.doc(security="api_key")
    def post(self):

        try:

            savePost(json.loads(request.data))
        except ValueError as e:
            return e.args, 409
        except ValidationError as e2:
            print(e2.args)
            return e2.args, 400

        return "Successully Saved"


@post_namespace.route("/delete/<int:id>")
class deletePost(Resource):
    @token_required
    @post_namespace.doc(security="api_key")
    def delete(self, id):
        try:
            deleteById(id)
        except NotFoundErr as e:
            return e.args, 400
        return "Successully Deleted"


@post_namespace.route("/update/<int:id>")
@post_namespace.expect(PostDto.post)
class updatePost(Resource):
    @token_required
    @post_namespace.doc(security="api_key")
    def put(self, id):
        try:
            modifyPost(id, json.loads(request.data))
        except ValueError as e:
            return e.args, 409
        except ValidationError as e2:
            return e2.args, 400
        except NotFoundErr as e3:
            return e3.args, 400
        return "Successully Updated"
