from flask_restful import Resource, reqparse
from datetime import datetime
from model.blog import BlogModel
from model.user import UserModel

class BlogsResource(Resource):
    def get(self):
        return [blog.json() for blog in BlogModel.find_all()]

class BlogUserResource(Resource):
    def post(self, username):
        _parser = reqparse.RequestParser()
        _parser.add_argument('title', type=str, required=True)
        _parser.add_argument('content', type=str, required=True)
        payload = _parser.parse_args()
        title = payload.get('title')
        content = payload.get('content')
        user = UserModel.find_by_userid(username)
        post_time = datetime.now()
        if BlogModel.find_by_title(title):
            return {'message': f'similar title exist', 'title': title}, 400
        blog = BlogModel(
            title=title,
            content=content,
            post_time=post_time,
            post_by=user
        )
        blog.save()
        return blog.json()
    
    def get(self, username):
        user = UserModel.find_by_username(username=username)
        if user is None:
            return {'message': f'user not found {username}'}, 400
        return [blog.json() for blog in BlogModel.find_by_user(user)]

class BlogResource(Resource):
    def get(self, blog_id):
        blog = BlogModel.find_by_id(blog_id)
        if blog is None:
            return {'message': f'no blog with id {blog_id}'}, 404
        return blog.json()

    def put(self, blog_id):
        blog = BlogModel.find_by_id(blog_id)
        if blog is None:
            return {'message': f'no blog with id {blog_id}'}, 404
        _parse = reqparse.RequestParser()
        _parse.add_argument('title', type=str, required=True)
        _parse.add_argument('content', type=str, required=True)
        payload = _parse.parse_args()
        blog.title = payload.get('title')
        blog.content = payload.get('content')
        blog.save()
        return blog.json()

    def delete(self, blog_id):
        blog = BlogModel.find_by_id(blog_id)
        if blog is None:
            return {'message': f'no blog with id {blog_id}'}, 404
        response = blog.json()
        blog.delete()
        return {'message': f'blog deleted', 'object': response}
