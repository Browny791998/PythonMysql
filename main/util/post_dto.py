from flask_restx import Namespace, fields


class PostDto:

    post_namespace = Namespace(name="post", path="/post")


    post = post_namespace.model(
        "post",
        {
            "post_title": fields.String(required=True),
            "description": fields.String(required=True),
            "user_id": fields.Integer(required=True),
            "date": fields.Date(),
        },
    )
 
        
