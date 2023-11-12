from db import db

class UserModel(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    image = db.Column(db.String, default='NA')

    def json(self):
        return {
            'username': self.username,
            'password': self.password,
            'image': self.image,
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
