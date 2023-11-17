from db import db
from .base import BaseModel


class UserModel(BaseModel):
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    image = db.Column(db.String, default='NA')
    follows = db.relationship(
        'FollowModel',
        foreign_keys='FollowModel.follower_id',
        backref='follower',
        lazy='dynamic',
        cascade="all, delete-orphan",
    )
    followers = db.relationship(
        'FollowModel',
        foreign_keys='FollowModel.followed_id',
        backref='followed',
        lazy='dynamic',
        cascade="all, delete-orphan",
    )
    blogs = db.relationship('BlogModel', backref='post_by', lazy='dynamic', cascade="all, delete-orphan")
    likes = db.relationship('LikeModel', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'image': self.image,
            # 'follows': [f.followed.username for f in self.follows],
            # 'followers': [f.follower.username for f in self.followers],
            # 'blogs': [blog.json() for blog in self.blogs]
        }
