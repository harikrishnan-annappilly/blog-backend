from db import db
from .base import BaseModel


class FollowModel(BaseModel):
    follower_id = db.Column(db.String, db.ForeignKey('user_model.username'), nullable=False)
    followed_id = db.Column(db.String, db.ForeignKey('user_model.username'), nullable=False)

    def json(self):
        return {
            'follower': self.follower.username,
            'followed': self.followed.username,
        }
