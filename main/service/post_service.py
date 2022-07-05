from asyncio.windows_events import NULL
from xml.dom import NotFoundErr
from ..model.db_model import db, Post, post_schema, post_schema_list
from sqlalchemy import exc
from flask import jsonify
from ..constant import common_constant
import datetime


def getPostById(postId):
    post = post_schema.dump(
        Post.query.filter_by(post_id=postId).first()
    )
    return post





def validateGetValueWithSchema(getPostData):

    post_schema.load(
        {
            "post_title": getPostData["post_title"],
            "description": getPostData["description"],
            "user_id": getPostData["user_id"],
            "date": getPostData["date"],
        }
    )


def savePost(potentialNewPost):

    validateGetValueWithSchema(potentialNewPost)

    savePost= Post(
        post_title=potentialNewPost["post_title"],
        description=potentialNewPost["description"],
        user_id=potentialNewPost["user_id"],
        date=potentialNewPost["date"]
    )

    try:
        db.session.add(savePost)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        raise ValueError(common_constant.EMAIL_TAKEN_ERR)
    finally:
        db.session.close()


def modifyPost(updateId, updatePost):
    validateGetValueWithSchema(updatePost)

   
    post = Post.query.get(updateId)
    if not post:
        raise NotFoundErr(common_constant.POST_NOT_FOUND_ERR)
    post.post_title = (updatePost["post_title"],)
    post.description = (updatePost["description"],)
    post.user_id = (updatePost["user_id"],)
    post.date = (updatePost["date"],)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        raise ValueError(common_constant.EMAIL_TAKEN_ERR)
    finally:
        db.session.close()







def deleteById(deleteId):
    post = Post.query.get(deleteId)
    if not post:
        raise NotFoundErr(common_constant.POST_NOT_FOUND_ERR)
    db.session.delete(post)
    db.session.commit()


def getAllPost():
    postList = post_schema_list.dump(Post.query.all())
    return jsonify(postList)




