from datetime import datetime
from db import db
from .base import BaseModel


class BlogModel(BaseModel):
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    post_by_id = db.Column(db.String(255), db.ForeignKey('user_model.username'), nullable=False)
    likes = db.relationship('LikeModel', backref='blog', lazy='dynamic', cascade='all, delete-orphan')

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'post_time': str(self.post_time),
            'post_by': self.post_by.username,
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter(cls.title.ilike(title)).first()
