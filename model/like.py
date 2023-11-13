from db import db
from .base import BaseModel


class LikeModel(BaseModel):
    username = db.Column(db.String, db.ForeignKey('user_model.username'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_model.id'), nullable=False)
    liked = db.Column(db.Boolean, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'blog_id': self.blog_id,
            'liked': self.liked,
        }
