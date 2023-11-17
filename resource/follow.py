from flask_restful import Resource, reqparse
from model.follow import FollowModel
from model.user import UserModel
from utils.wrappers import user_exist


class FollowsResource(Resource):
    def get(self):
        return [follow.json() for follow in FollowModel.find_all()]


class FollowResource(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('username', type=str, required=True)

    @user_exist
    def get(self, username):
        user = UserModel.find_one(username=username)
        return [follow.followed.username for follow in FollowModel.find_all(follower=user)]

    @user_exist
    def post(self, username):
        payload = self._parser.parse_args()
        followed_username = payload.get('username')
        follower = UserModel.find_one(username=username)
        followed = UserModel.find_one(username=followed_username)
        if followed.username == follower.username:
            return {'message': f'both follower and followed is same user'}, 400
        if FollowModel.find_one(follower=follower, followed=followed):
            return {'message': f'already followed'}, 400
        follow = FollowModel(follower=follower, followed=followed)
        follow.save()
        return follow.json()

    @user_exist
    def delete(self, username):
        payload = self._parser.parse_args()
        followed_username = payload.get('username')
        follower = UserModel.find_one(username=username)
        followed = UserModel.find_one(username=followed_username)
        if followed.username == follower.username:
            return {'message': f'both follower and followed is same user'}, 400
        follow = FollowModel.find_one(follower=follower, followed=followed)
        if follow is None:
            return {'message': f'no entry for this'}, 400
        response = follow.json()
        follow.delete()
        return response
