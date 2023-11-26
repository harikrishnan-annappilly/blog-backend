from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_restful import Api
from db import db
from resource.user import UsersResource, UserResource, AuthResource
from resource.follow import FollowsResource, FollowResource
from resource.blog import BlogsResource, BlogResource
from resource.like import LikeResource, LikesResource

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
    return render_template('home.html')


api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/user/<string:username>')
api.add_resource(AuthResource, '/login')
api.add_resource(FollowsResource, '/follows')
api.add_resource(FollowResource, '/follow')
api.add_resource(BlogsResource, '/blogs')
api.add_resource(BlogResource, '/blog/<int:blog_id>')
api.add_resource(LikesResource, '/likes')
api.add_resource(LikeResource, '/like')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
