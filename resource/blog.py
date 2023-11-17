from flask_restful import Resource, reqparse
from datetime import datetime
from model.blog import BlogModel
from model.user import UserModel
from utils.wrappers import user_exist, blog_exist


class BlogsResource(Resource):
    def get(self):
        return [blog.json() for blog in BlogModel.find_all()]

    @user_exist
    def post(self):
        _parser = reqparse.RequestParser()
        _parser.add_argument('title', type=str, required=True)
        _parser.add_argument('content', type=str, required=True)
        _parser.add_argument('username', type=str, required=True)
        payload = _parser.parse_args()
        title = payload.get('title')
        content = payload.get('content')
        username = payload.get('username')
        user = UserModel.find_one(username=username)
        post_time = datetime.now()
        if BlogModel.find_by_title(title):
            return {'message': f'similar title exist', 'title': title}, 400
        blog = BlogModel(title=title, content=content, post_time=post_time, post_by=user)
        blog.save()
        return blog.json()


class BlogResource(Resource):
    @blog_exist
    def get(self, blog_id):
        blog = BlogModel.find_one(id=blog_id)
        return blog.json()

    @blog_exist
    def put(self, blog_id):
        blog = BlogModel.find_one(id=blog_id)
        _parse = reqparse.RequestParser()
        _parse.add_argument('title', type=str, required=True)
        _parse.add_argument('content', type=str, required=True)
        payload = _parse.parse_args()
        title = payload.get('title')
        content = payload.get('content')
        blog.title = title
        blog.content = content
        blog.save()
        return blog.json()

    @blog_exist
    def delete(self, blog_id):
        blog = BlogModel.find_one(id=blog_id)
        response = blog.json()
        blog.delete()
        return {'message': f'blog deleted', 'object': response}
