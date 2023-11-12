from db import db

class LikeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by(cls, user=None, blog=None):
        if user and blog:
            return cls.query.filter_by(user=user, blog=blog).first()
        if user:
            return cls.query.filter_by(user=user).all()
        if blog:
            return cls.query.filter_by(blog=blog).all()
        return cls.query.all()
