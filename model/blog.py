from datetime import datetime
import functools
from db import db
from .base import BaseModel


class BlogModel(BaseModel):
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    post_by_id = db.Column(db.String, db.ForeignKey('user_model.username'), nullable=False)
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


def blog_exist(func):
    @functools.wraps(func)
    def validation(*args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog = BlogModel.find_one(id=blog_id)
        if blog is None:
            return {'message': 'blog not found', 'blog_id': blog_id}, 404
        return func(*args, **kwargs)

    return validation
