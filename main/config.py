from cgitb import reset
import imp
from flask import Flask
from flask_restx import Api
from main.model.db_model import User, db
from sqlalchemy import event
# from sqlalchemy import event
from main.controller.user_controller import user_namespace
from main.controller.post_controller import post_namespace
from main.controller.authentication_controller import(
    login_namespace,
    forgot_password_namespace,
    reset_password_namespace
)
from flask import Blueprint
from flask_cors import CORS
from decouple import config
from flask_mail_sendgrid import MailSendGrid

app = Flask(__name__)  # Create a Flask WSGI application
CORS(app)

# Data Base
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{config('DB_USER_NAME')}:{config('DB_PASSWORD')}@{config('DB_HOST')}/{config('DB_DATABASE_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config("SECRET_KEY")
db.init_app(app)

app.config["MAIL_SENDGRID_API_KEY"] = config("MAIL_SENDGRID_API_KEY")
app.config["MAIL_SENDER"] = config("MAIL_SENDER")
mail = MailSendGrid(app)

# Api
authorizations = {
    "api_key": {"type": "apiKey", "in": "header", "name": "x-access-token"}
}
blueprint = Blueprint("api", __name__)
api = Api(blueprint, authorizations=authorizations)
api.add_namespace(user_namespace)
api.add_namespace(post_namespace)
api.add_namespace(login_namespace)
api.add_namespace(forgot_password_namespace)
api.add_namespace(reset_password_namespace)



# # initilize data after table is created
@event.listens_for(User.__table__, "after_create")
def receive_after_create(target, connection, **kw):

    with app.app_context():
        # Recreate database each time for demo
        db.session.add(
            User(
                user_name="default-user",
                email="scm.yehtetaung@gmail.com",
                password="1234",
                profile_photo="",
                position="admin",
                address="Yangon",
                dob="2022-01-17",
                phone="123123",
                created_at="2016-03-13 02:32:21",
                updated_at="2016-03-13 02:32:21",
                deleted_at="2016-03-13 02:32:21",
                otp_number="",
            )
        )
        db.session.commit()
