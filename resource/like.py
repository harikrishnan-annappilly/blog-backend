from flask_restful import Resource, reqparse
from model.like import LikeModel
from model.blog import BlogModel
from model.user import UserModel
from utils.wrappers import get_one_or_404


class LikesResource(Resource):
    def get(self):
        return [like.json() for like in LikeModel.find_all()]


class LikeResource(Resource):
    def put(self, username):
        _parser = reqparse.RequestParser()
        _parser.add_argument('blog_id', type=int, required=True)
        payload = _parser.parse_args()
        blog_id = payload.get('blog_id')

        @get_one_or_404(UserModel, username=username)
        @get_one_or_404(BlogModel, id=blog_id)
        def decorate(*args):
            (user, blog) = args

            like = LikeModel.find_one(user=user, blog=blog)
            if like:
                like.liked = not like.liked
            else:
                like = LikeModel(user=user, blog=blog, liked=True)
            like.save()
            return like.json()

        return decorate()

    def get(self, username):
        @get_one_or_404(UserModel, username=username)
        def decorate(*args):
            (user,) = args
            return [like.id for like in LikeModel.find_all(user=user) if like.liked]

        return decorate()
