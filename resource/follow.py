from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.follow import FollowModel
from model.user import UserModel
from utils.wrappers import get_one_or_404


class FollowsResource(Resource):
    def get(self):
        return [follow.json() for follow in FollowModel.find_all()]


class FollowResource(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('username', type=str, required=True)

    @jwt_required()
    def get(self):
        logged_username = get_jwt_identity()

        @get_one_or_404(UserModel, username=logged_username)
        def decorate(*args):
            (user,) = args
            return [follow.followed.username for follow in FollowModel.find_all(follower=user)]

        return decorate()

    @jwt_required()
    def post(self):
        logged_username = get_jwt_identity()
        payload = self._parser.parse_args()
        followed_username = payload.get('username')

        @get_one_or_404(UserModel, username=logged_username)
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

    @jwt_required()
    def delete(self):
        logged_username = get_jwt_identity()
        payload = self._parser.parse_args()
        followed_username = payload.get('username')

        @get_one_or_404(UserModel, username=logged_username)
        @get_one_or_404(UserModel, username=followed_username)
        def decorate(*args):
            (follower, followed) = args
            follow = FollowModel.find_one(follower=follower, followed=followed)
            if follow is None:
                return {
                    'message': f'no entry for this',
                    'follower': logged_username,
                    'followed': followed_username,
                }, 404
            response = follow.json()
            follow.delete()
            return response

        return decorate()
