from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from model.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', required=True, type=str)
_user_parser.add_argument('password', required=True, type=str)

class UsersResource(Resource):
    def post(self):
        _user_parser.add_argument('image', type=str)
        payload = _user_parser.parse_args()
        username = payload.get('username')
        password = payload.get('password')
        image = payload.get('image')
        if UserModel.find_by_username(username):
            return {
                'message': f'username {username} is taken'
            }, 400
        user = UserModel(username=username, password=password, image=image)
        user.save()
        return user.json()

    def get(self):
        return [user.json() for user in UserModel.find_all()]

class UserResource(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user is None:
            return {
                'message': f'user {username} not found'
            }, 404
        return user.json()

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user is None:
            return {
                'message': f'user {username} not found'
            }, 404
        response = {
            'message': f'user {username} deleted',
            'user': user.json()
            }
        user.delete()
        return response

    def put(self, username):
        user = UserModel.find_by_username(username)
        if user is None:
            return {
                'message': f'user {username} not found'
            }, 404
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        parser.add_argument('image', type=str)
        payload = parser.parse_args()
        password = payload.get('password')
        image = payload.get('image')
        user.password = password if password is not None else user.password
        user.image = image if image is not None else user.image
        user.save()
        return user.json()

class AuthResource(Resource):
    def post(self):
        payload = _user_parser.parse_args()
        username = payload.get('username')
        password = payload.get('password')
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': f'user {username} not found'}, 404
        if user.password != password:
            return {'message': f'invalid password'}, 401
        access_token = create_access_token(identity=user.username, additional_claims=user.json())
        return {'message': 'login success', 'access_token': access_token}
