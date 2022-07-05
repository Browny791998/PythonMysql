from asyncio.windows_events import NULL
from xml.dom import NotFoundErr
from ..model.db_model import db, User, user_schema, user_schema_list
from sqlalchemy import exc
from flask import jsonify
from ..constant import common_constant
import datetime


def getUserById(userId):
    user = user_schema.dump(
        User.query.filter_by(user_id=userId).first()
    )
    return user


def getUserByEmail(email):
    user = user_schema.dump(User.query.filter_by(email=email).first())
    return user


def validateGetValueWithSchema(getUserData):

    user_schema.load(
        {
            "user_name": getUserData["user_name"],
            "email": getUserData["email"],
            "password": getUserData["password"],
            "profile_photo": getUserData["profile_photo"],
            "position": getUserData["position"],
            "address": getUserData["address"],
            "dob": getUserData["dob"],
            "phone": getUserData["phone"],
            "tech_skill": getUserData["tech_skill"],
            "join_date": getUserData["join_date"],
            "period": getUserData["period"],
        }
    )


def saveUser(potentialNewUser):

    validateGetValueWithSchema(potentialNewUser)

    getPeriod = potentialNewUser["period"]

    # calculate period beforing saving
    if not getPeriod:
        getPeriod = calculatePeriod(potentialNewUser["join_date"])

    saveUser= User(
        user_name=potentialNewUser["user_name"],
        email=potentialNewUser["email"],
        password=potentialNewUser["password"],
        profile_photo=potentialNewUser["profile_photo"],
        position=potentialNewUser["position"],
        address=potentialNewUser["address"],
        dob=potentialNewUser["dob"],
        phone=potentialNewUser["phone"],
        created_at=datetime.datetime.now(),
        updated_at=NULL,
        join_date=potentialNewUser["join_date"],
        period=getPeriod,
        tech_skill=potentialNewUser["tech_skill"],
    )

    try:
        db.session.add(saveUser)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        raise ValueError(common_constant.EMAIL_TAKEN_ERR)
    finally:
        db.session.close()


def modifyUser(updateId, updateUser):
    validateGetValueWithSchema(updateUser)

    # calculate period beforing saving
    getPeriod = calculatePeriod(updateUser["join_date"])
    user = User.query.get(updateId)
    if not user:
        raise NotFoundErr(common_constant.USER_NOT_FOUND_ERR)
    user.user_name = (updateUser["user_name"],)
    user.email = (updateUser["email"],)
    user.password = (updateUser["password"],)
    user.profile_photo = (updateUser["profile_photo"],)
    user.position = (updateUser["position"],)
    user.address = (updateUser["address"],)
    user.dob = (updateUser["dob"],)
    user.phone = (updateUser["phone"],)

    user.updated_at = datetime.datetime.now()
    user.join_date = updateUser["join_date"]
    user.period = getPeriod
    user.tech_skill = updateUser["tech_skill"]

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        raise ValueError(common_constant.EMAIL_TAKEN_ERR)
    finally:
        db.session.close()


def updatePasswordByEmail(email, newpassword):
    user = User.query.filter_by(email=email).first()

    if newpassword == user.password:
        raise ValueError("This is your old password, that should be new password.")
    user.password = newpassword

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception("Common error")
    finally:
        db.session.close()


def updateOTPByEmail(email, otp):
    user = User.query.filter_by(email=email).first()
    user.otp_number = otp
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception("Common error")
    finally:
        db.session.close()


def deleteById(deleteId):
    user = User.query.get(deleteId)
    if not user:
        raise NotFoundErr(common_constant.USER_NOT_FOUND_ERR)
    db.session.delete(user)
    db.session.commit()


def getAllUser():
    userList = user_schema_list.dump(User.query.all())
    for user in userList:
        del user["password"]
        del user["otp_number"]
    return jsonify(userList)



def calculatePeriod(join_date):
    print(join_date)
    today = datetime.datetime.today()
    # convert date string to date object
    joinDate = datetime.datetime.strptime(join_date, "%Y-%m-%d")
    months = today.month - joinDate.month
    years = today.year - joinDate.year
    days = today.day - joinDate.day

    return "{0} years, {1} months, {2} days".format(years, months, days)
