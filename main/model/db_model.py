from attr import field
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from ..constant import common_constant

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(
        db.Integer, primary_key=True, unique=True, autoincrement=True
    )
    user_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(100))
    profile_photo = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    dob = db.Column(db.Date())
    phone = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)
    deleted_at = db.Column(db.DateTime())
    otp_number = db.Column(db.String(100))
    token = db.Column(db.String())
    join_date = db.Column(db.Date())
    period = db.Column(db.String(100))
    tech_skill = db.Column(db.String(100))


class UserSchema(Schema):

    user_id = fields.Integer()

    user_name = fields.String(
        required=True,
        validate=validate.Length(min=1, error=common_constant.USER_NAME_ERR),
    )
    email = fields.String(
        required=True,
        validate=validate.Length(min=1, error=common_constant.USER_EMAIL_ERR),
    )
    password = fields.String(required=True)
    profile_photo = fields.String(
        required=True,
        validate=validate.Length(
            min=1, error=common_constant.USER_PROFILE_PHOTO_ERR
        ),
    )
    position = fields.String(
        required=True,
        validate=validate.Length(min=1, error=common_constant.USER_POSITION_ERR),
    )
    address = fields.String(required=True)
    dob = fields.Date()
    phone = fields.String(required=True)
    created_at = fields.DateTime(common_constant.DATE_TIME_FORMAT)
    updated_at = fields.DateTime(common_constant.DATE_TIME_FORMAT)
    deleted_at = fields.DateTime(common_constant.DATE_TIME_FORMAT)
    otp_number = fields.String()
    token = fields.String()
    join_date = fields.Date()
    period = fields.String()
    tech_skill = fields.String()

    class Meta:
        fields = (
            "user_id",
            "user_name",
            "email",
            "password",
            "profile_photo",
            "position",
            "address",
            "dob",
            "phone",
            "created_at",
            "updated_at",
            "deleted_at",
            "otp_number",
            "token",
            "join_date",
            "period",
            "tech_skill",
        )


user_schema = UserSchema()
user_schema_list = UserSchema(many=True)



class Post(db.Model):
    post_id = db.Column(
        db.Integer, primary_key=True, unique=True, autoincrement=True
    )
    post_title = db.Column(db.String(100), nullable=False)
    description= db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer(),nullable=False)
    date = db.Column(db.Date())


class PostSchema(Schema):

    post_id = fields.Integer()

    post_title= fields.String(
        required=True,
        validate=validate.Length(min=1, error=common_constant.POST_TITLE_ERR),
    )
    description = fields.String(
        required=True,
        validate=validate.Length(min=1, error=common_constant.POST_DESCRIPTION_ERR),
    )
    user_id = fields.Integer(required=True)
    date = fields.Date()

    class Meta:
        fields = (
            "post_id",
            "post_title",
            "description",
            "user_id",
            "date",
            
        )


post_schema = PostSchema()
post_schema_list = PostSchema(many=True)
