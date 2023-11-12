from datetime import datetime
from db import db

class BlogModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    post_by_id = db.Column(db.String, db.ForeignKey('user_model.username'), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'post_time': str(self.post_time),
            'post_by': self.post_by.username,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_user(cls, post_by):
        return cls.query.filter_by(post_by=post_by)

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter(cls.title.ilike(title)).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def get_blogs_for_user(cls, user):
        follows = [follow.followed.username for follow in user.follows]
        follows.append(user.username)
        return cls.query.filter(cls.post_by_id.in_(follows)).all()
