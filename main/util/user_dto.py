from flask_restx import Namespace, fields


class UserDto:

    user_namespace = Namespace(name="user", path="/user")


    user = user_namespace.model(
        "user",
        {
            "user_name": fields.String(required=True),
            "email": fields.String(required=True),
            "password": fields.String(required=True),
            "profile_photo": fields.String(),
            "position": fields.String(required=True),
            "phone": fields.String(required=True),
            "address": fields.String(),
            "dob": fields.Date(),
            "join_date":fields.Date(),
            "tech_skill":fields.String(),
            "period":fields.String()
        },
    )
 
        
