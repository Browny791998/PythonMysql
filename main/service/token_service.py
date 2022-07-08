
from textwrap import wrap
from flask import request
from ..model.db_model import User
from functools import wraps
from flask import current_app

import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return {"message":"Token is missing !"},401

        try:
            print(token)
            
            data = jwt.decode(
                token,current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = User.query.filter_by(email =data["email"]).first()
        except:
            return {"message":"Token is invalid !!"},401

        return f(*args, **kwargs)

    return decorated