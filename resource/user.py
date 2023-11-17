from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from model.user import UserModel, user_exist

SUPER_USER = ['admin']

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
        if UserModel.find_one(username=username):
            return {'message': f'username {username} is taken'}, 400
        user = UserModel(username=username, password=password, image=image)
        user.save()
        return user.json()

    @jwt_required()
    def get(self):
        return [user.json() for user in UserModel.find_all()]


class UserResource(Resource):
    @user_exist
    def get(self, username):
        user = UserModel.find_one(username=username)
        return user.json()

    @jwt_required()
    @user_exist
    def delete(self, username):
        if get_jwt_identity() not in SUPER_USER:
            return {'message': f'you are not authorized perform this operation'}, 403
        user = UserModel.find_one(username=username)
        response = {'message': f'user {username} deleted', 'user': user.json()}
        user.delete()
        return response

    @user_exist
    def put(self, username):
        user = UserModel.find_one(username=username)
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
    @user_exist
    def post(self):
        payload = _user_parser.parse_args()
        username = payload.get('username')
        password = payload.get('password')
        user = UserModel.find_one(username=username)
        if user.password != password:
            return {'message': f'invalid password'}, 401
        access_token = create_access_token(identity=user.username, additional_claims=user.json())
        return {'message': 'login success', 'access_token': access_token}
