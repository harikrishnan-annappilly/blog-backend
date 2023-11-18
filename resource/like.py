from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.like import LikeModel
from model.blog import BlogModel
from model.user import UserModel
from utils.wrappers import get_one_or_404


class LikesResource(Resource):
    def get(self):
        return [like.json() for like in LikeModel.find_all()]


class LikeResource(Resource):
    @jwt_required()
    def put(self):
        _parser = reqparse.RequestParser()
        _parser.add_argument('blog_id', type=int, required=True)
        payload = _parser.parse_args()
        blog_id = payload.get('blog_id')

        @get_one_or_404(UserModel, username=get_jwt_identity())
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

    @jwt_required()
    def get(self):
        @get_one_or_404(UserModel, username=get_jwt_identity())
        def decorate(*args):
            (user,) = args
            return [like.blog_id for like in LikeModel.find_all(user=user) if like.liked]

        return decorate()
