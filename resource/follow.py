from flask_restful import Resource, reqparse
from model.follow import FollowModel
from model.user import UserModel

class FollowsResource(Resource):
    def get(self):
        response = {}
        for follow in FollowModel.find_all():
            if response.get(follow.follower.username):
                response[follow.follower.username].append(follow.followed.username)
            else:
                response[follow.follower.username] = [follow.followed.username]
        return [follow.json() for follow in FollowModel.find_all()]
    
class FollowResource(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('username', type=str, required=True)
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user is None:
            return {'message': f'username {username} not found'}, 404
        return [follow.followed.username for follow in FollowModel.find_by_follower(user)]

    def post(self, username):
        payload = self._parser.parse_args()
        followed_username = payload.get('username')
        follower = UserModel.find_by_username(username)
        followed = UserModel.find_by_username(followed_username)
        if follower is None:
            return {'message': f'follower {username} not found'}, 404
        if followed is None:
            return {'message': f'follower {followed_username} not found'}, 404
        if followed.username == follower.username:
            return {'message': f'both follower and followed is same user'}, 400
        if FollowModel.find_by_follower_an_followed(follower=follower, followed=followed):
            return {'message': f'already followed'}, 400
        follow = FollowModel(follower=follower, followed=followed)
        follow.save()
        return follow.json()

    def delete(self, username):
        payload = self._parser.parse_args()
        followed_username = payload.get('username')
        follower = UserModel.find_by_username(username)
        followed = UserModel.find_by_username(followed_username)
        if follower is None:
            return {'message': f'follower {username} not found'}, 404
        if followed is None:
            return {'message': f'follower {followed_username} not found'}, 404
        if followed.username == follower.username:
            return {'message': f'both follower and followed is same user'}, 400
        follow = FollowModel.find_by_follower_an_followed(follower=follower, followed=followed)
        if follow is None:
            return {'message': f'no entry for this'}, 400
        response = follow.json()
        follow.delete()
        return response
