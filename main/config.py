from flask import Flask
from flask_restx import Api
from main.model.db_model import User, db
# from sqlalchemy import event
from main.controller.user_controller import user_namespace
from main.controller.post_controller import post_namespace
from flask import Blueprint
from flask_cors import CORS
from decouple import config

app = Flask(__name__)  # Create a Flask WSGI application
CORS(app)

# Data Base
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{config('DB_USER_NAME')}:{config('DB_PASSWORD')}@{config('DB_HOST')}/{config('DB_DATABASE_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config("SECRET_KEY")
db.init_app(app)



# Api
authorizations = {
    "api_key": {"type": "apiKey", "in": "header", "name": "x-access-token"}
}
blueprint = Blueprint("api", __name__)
api = Api(blueprint, authorizations=authorizations)
api.add_namespace(user_namespace)
api.add_namespace(post_namespace)

# # initilize data after table is created
# @event.listens_for(Employee.__table__, "after_create")
# def receive_after_create(target, connection, **kw):

#     with app.app_context():
#         # Recreate database each time for demo
#         db.session.add(
#             Employee(
#                 employee_name="default-employee",
#                 email="scm.nandahein@gmail.com",
#                 password="1234",
#                 profile_photo="",
#                 position="admin",
#                 address="Yangon",
#                 dob="2022-01-17",
#                 phone="123123",
#                 created_at="2016-03-13 02:32:21",
#                 updated_at="2016-03-13 02:32:21",
#                 deleted_at="2016-03-13 02:32:21",
#                 otp_number="",
#             )
#         )
#         db.session.commit()
