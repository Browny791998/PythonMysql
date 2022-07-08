from flask_mail import Message


def sendEmail(email, otp):
    from ..config import app

    msg = Message("Here is your otp", sender=app.config["MAIL_SENDER"], recipients=[email])
    msg.body = otp
    msg.html = f"<b>{otp}</b>"

    from ..config import mail

    mail.send(msg)
    print("Successfully Sent!!!!")
