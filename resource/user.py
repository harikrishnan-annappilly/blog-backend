from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from model.user import UserModel
from utils.wrappers import get_one_or_404

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

    def get(self):
        return [user.json() for user in UserModel.find_all()]


class UserResource(Resource):
    def get(self, username):
        @get_one_or_404(UserModel, username=username)
        def decorate(*args):
            (user,) = args
            return user.json()

        return decorate()

    @jwt_required()
    def delete(self, username):
        logged_username = get_jwt_identity()
        if logged_username != username and logged_username not in SUPER_USER:
            return {'message': 'you dont have permission to do this'}, 403

        @get_one_or_404(UserModel, username=username)
        def decorate(*args):
            (user,) = args
            response = {'message': f'user {username} deleted', 'user': user.json()}
            user.delete()
            return response

        return decorate()

    @jwt_required()
    def put(self, username):
        logged_username = get_jwt_identity()
        if logged_username != username and logged_username not in SUPER_USER:
            return {'message': 'you dont have permission to do this'}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        parser.add_argument('image', type=str)
        payload = parser.parse_args()
        password = payload.get('password')
        image = payload.get('image')

        @get_one_or_404(UserModel, username=username)
        def decorate(*args):
            (user,) = args
            user.password = password if password is not None else user.password
            user.image = image if image is not None else user.image
            user.save()
            return user.json()

        return decorate()


class AuthResource(Resource):
    def post(self):
        payload = _user_parser.parse_args()
        username = payload.get('username')
        password = payload.get('password')

        @get_one_or_404(UserModel, username=username)
        def decorate(*args):
            (user,) = args
            if user.password != password:
                return {'message': f'invalid password'}, 401
            access_token = create_access_token(identity=user.username, additional_claims=user.json())
            return {'message': 'login success', 'access_token': access_token}

        return decorate()
