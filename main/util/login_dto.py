from flask_restx import Namespace, fields


class LoginDto:

    login_namespace = Namespace(name="login", path="/")
    forgot_password_namespace = Namespace(name="retrieve", path="/")
    reset_password_namespace = Namespace(name="reset", path="/")

    login_request = login_namespace.model(
        "Login", {"email": fields.String(), "password": fields.String()}
    )

    retrieve_request = forgot_password_namespace.model(
        "Retrieve",
        {
            "email": fields.String(),
        },
    )
    reset_request = reset_password_namespace.model(
        "Reset",
        {
            "email": fields.String(),
            "newpassword": fields.String(),
            "confirmpassword": fields.String(),
            "otpnumber": fields.String(),
        },
    )
