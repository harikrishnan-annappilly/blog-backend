from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from db import db
from resource.user import UsersResource, UserResource, AuthResource
from resource.follow import FollowsResource, FollowResource

app = Flask(__name__)

app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


db.init_app(app)

api = Api(app)
jwt = JWTManager(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return '<h1>This is running...</h1>'

api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/user/<string:username>')
api.add_resource(AuthResource, '/login')
api.add_resource(FollowsResource, '/follows')
api.add_resource(FollowResource, '/follow/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)
