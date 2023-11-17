from flask_restful import Resource, reqparse
from model.like import LikeModel
from model.blog import BlogModel
from model.user import UserModel, user_exist


class LikesResource(Resource):
    def get(self):
        return [like.json() for like in LikeModel.find_all()]


class LikeResource(Resource):
    @user_exist
    def put(self, username):
        _parser = reqparse.RequestParser()
        _parser.add_argument('blog_id', type=str, required=True)
        payload = _parser.parse_args()
        blog_id = payload.get('blog_id')

        blog = BlogModel.find_one(id=blog_id)
        user = UserModel.find_one(username=username)
        if blog is None:
            return {'message': f'blog with id {blog_id} not found'}, 404

        like = LikeModel.find_one(user=user, blog=blog)
        if like:
            like.liked = not like.liked
        else:
            like = LikeModel(user=user, blog=blog, liked=True)
        like.save()
        return like.json()

    @user_exist
    def get(self, username):
        user = UserModel.find_one(username=username)
        return [like.id for like in LikeModel.find_all(user=user) if like.liked]
