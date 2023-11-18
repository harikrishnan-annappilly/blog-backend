from flask_restful import Resource, reqparse
from model.follow import FollowModel
from model.user import UserModel
from utils.wrappers import get_one_or_404


class FollowsResource(Resource):
    def get(self):
        return [follow.json() for follow in FollowModel.find_all()]


class FollowResource(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('username', type=str, required=True)

    def get(self, username):
        @get_one_or_404(UserModel, username=username)
        def decorate(*args):
            (user,) = args
            return [follow.followed.username for follow in FollowModel.find_all(follower=user)]

        return decorate()

    def post(self, username):
        payload = self._parser.parse_args()
        followed_username = payload.get('username')

        @get_one_or_404(UserModel, username=username)
        @get_one_or_404(UserModel, username=followed_username)
        def decorate(*args):
            (follower, followed) = args
            if followed.username == follower.username:
                return {'message': f'both follower and followed is same user'}, 400
            if FollowModel.find_one(follower=follower, followed=followed):
                return {'message': f'already followed'}, 400
            follow = FollowModel(follower=follower, followed=followed)
            follow.save()
            return follow.json()

        return decorate()

    def delete(self, username):
        payload = self._parser.parse_args()
        followed_username = payload.get('username')

        @get_one_or_404(UserModel, username=username)
        @get_one_or_404(UserModel, username=followed_username)
        def decorate(*args):
            (follower, followed) = args
            follow = FollowModel.find_one(follower=follower, followed=followed)
            if follow is None:
                return {'message': f'no entry for this'}, 404
            response = follow.json()
            follow.delete()
            return response

        return decorate()
