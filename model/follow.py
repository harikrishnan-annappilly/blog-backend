from db import db

class FollowModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.String, db.ForeignKey('user_model.username'),  nullable=False)
    followed_id = db.Column(db.String, db.ForeignKey('user_model.username'),  nullable=False)

    def json(self):
        return {
            'follower': self.follower.username,
            'followed': self.followed.username,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_follower(cls, follower):
        return cls.query.filter_by(follower=follower).all()
    
    @classmethod
    def find_by_follower_an_followed(cls, follower, followed):
        return cls.query.filter_by(follower=follower, followed=followed).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
