import functools
from flask import request
from model.user import UserModel
from model.blog import BlogModel


def user_exist(func):
    @functools.wraps(func)
    def validation(*args, **kwargs):
        usernames = []
        key = 'username'

        if kwargs.get(key):
            usernames.append(kwargs.get(key))
        if request.is_json and key in request.json:
            usernames.append(str(request.json.get(key)))

        for username in usernames:
            user = UserModel.find_one(username=username)
            if user is None:
                return {'message': f'user not found', 'username': username}, 404
        return func(*args, **kwargs)

    return validation


def blog_exist(func):
    @functools.wraps(func)
    def validation(*args, **kwargs):
        blog_ids = []
        key = 'blog_id'

        if kwargs.get(key):
            blog_ids.append(kwargs.get(key))
        if request.is_json and key in request.json:
            blog_id = request.json[key]
            if not str(blog_id).isdigit():
                return {"message": {"blog_id": f"invalid literal for int() with base 10: '{blog_id}'"}}, 400
            blog_ids.append(int(blog_id))

        for blog_id in blog_ids:
            blog = BlogModel.find_one(id=blog_id)
            if blog is None:
                return {'message': 'blog not found', 'blog_id': int(blog_id)}, 404
        return func(*args, **kwargs)

    return validation
