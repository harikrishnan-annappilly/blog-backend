from flask_restful import Resource, reqparse
from datetime import datetime
from model.blog import BlogModel
from model.user import UserModel
from utils.wrappers import get_one_or_404


class BlogsResource(Resource):
    def get(self):
        return [blog.json() for blog in BlogModel.find_all()]

    def post(self):
        _parser = reqparse.RequestParser()
        _parser.add_argument('title', type=str, required=True)
        _parser.add_argument('content', type=str, required=True)
        _parser.add_argument('username', type=str, required=True)
        payload = _parser.parse_args()
        title = payload.get('title')
        content = payload.get('content')
        username = payload.get('username')
        post_time = datetime.now()
        if BlogModel.find_by_title(title):
            return {'message': f'similar title exist', 'title': title}, 400

        @get_one_or_404(UserModel, username=username)
        def decorate(*args):
            (user,) = args
            blog = BlogModel(title=title, content=content, post_time=post_time, post_by=user)
            blog.save()
            return blog.json()

        return decorate()


class BlogResource(Resource):
    def get(self, blog_id):
        @get_one_or_404(BlogModel, id=blog_id)
        def decorate(*args):
            (blog,) = args
            return blog.json()

        return decorate()

    def put(self, blog_id):
        _parse = reqparse.RequestParser()
        _parse.add_argument('title', type=str, required=True)
        _parse.add_argument('content', type=str, required=True)
        payload = _parse.parse_args()
        title = payload.get('title')
        content = payload.get('content')

        @get_one_or_404(BlogModel, id=blog_id)
        def decorate(*args):
            (blog,) = args
            blog.title = title
            blog.content = content
            blog.save()
            return blog.json()

        return decorate()

    def delete(self, blog_id):
        @get_one_or_404(BlogModel, id=blog_id)
        def decorate(*args):
            (blog,) = args
            response = blog.json()
            blog.delete()
            return {'message': f'blog deleted', 'object': response}

        return decorate()
