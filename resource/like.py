from flask_restful import Resource, reqparse
from model.like import LikeModel
from model.blog import BlogModel
from model.user import UserModel

class LikesResource(Resource):
    def get(self):
        return [like.json() for like in LikeModel.find_by()]

class LikeResource(Resource):
    def put(self, username):
        _parser = reqparse.RequestParser()
        _parser.add_argument('blog_id', type=str, required=True)
        payload = _parser.parse_args()
        blog_id = payload.get('blog_id')
        blog = BlogModel.find_by_id(blog_id)
        user = UserModel.find_by_username(username)
        like = LikeModel.find_by(user=user, blog=blog)
        if blog is None:
            return {'message': f'blog with id {blog_id} not found'}, 404
        if user is None:
            return {'message': f'user with username {username} not found'}, 404
        if like:
            like.liked = not like.liked
        else:
            like = LikeModel(user=user, blog=blog, liked=True)
        like.save()
        return like.json()
    
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user is None:
            return {'message': f'user with username {username} not found'}, 404
        return [like.id for like in LikeModel.find_by(user) if like.liked]
