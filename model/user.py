from db import db

class UserModel(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    image = db.Column(db.String, default='NA')
    follows = db.relationship('FollowModel', foreign_keys='FollowModel.follower_id', backref='follower', lazy='dynamic', cascade="all, delete-orphan")
    followers = db.relationship('FollowModel', foreign_keys='FollowModel.followed_id', backref='followed', lazy='dynamic', cascade="all, delete-orphan")

    def json(self):
        return {
            'username': self.username,
            'password': self.password,
            'image': self.image,
            # 'follows': [f.followed.username for f in self.follows],
            # 'followers': [f.follower.username for f in self.followers],
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.get(userid)

    @classmethod
    def find_all(cls):
        return cls.query.all()
