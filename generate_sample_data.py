from app import app
from db import db
from model.user import UserModel
from model.blog import BlogModel
from model.like import LikeModel
from model.follow import FollowModel

_blog_content = 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer. This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer. This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.'

with app.app_context():
    db.drop_all()
    db.create_all()

    print('Creating users', end='')
    admin = UserModel(username='admin', password='123')
    jerry = UserModel(username='jerry', password='123')
    tom = UserModel(username='tom', password='123')
    db.session.add_all([admin, jerry, tom])
    db.session.commit()
    print(' --completed')

    print('Creating blogs', end='')
    blog1 = BlogModel(title='Admin made first post', content=_blog_content, post_by=admin)
    blog2 = BlogModel(title='Admin made second post', content=_blog_content, post_by=admin)
    blog3 = BlogModel(title='Jerry made first post', content=_blog_content, post_by=jerry)
    blog4 = BlogModel(title='Tom made first post', content=_blog_content, post_by=tom)
    db.session.add_all([blog1, blog2, blog3, blog4])
    db.session.commit()
    print(' --completed')

    print('Creating likes', end='')
    like1 = LikeModel(blog=blog1, user=jerry)
    like2 = LikeModel(blog=blog1, user=tom)
    like3 = LikeModel(blog=blog2, user=jerry)
    like4 = LikeModel(blog=blog3, user=admin)
    like5 = LikeModel(blog=blog4, user=admin)
    like6 = LikeModel(blog=blog4, user=jerry)
    like7 = LikeModel(blog=blog4, user=tom)
    db.session.add_all([like1, like2, like3, like4, like5, like6, like7])
    db.session.commit()
    print(' --completed')

    print('Creating follows', end='')
    follow1 = FollowModel(follower=admin, followed=jerry)
    follow2 = FollowModel(follower=admin, followed=tom)
    follow3 = FollowModel(follower=jerry, followed=tom)
    follow4 = FollowModel(follower=tom, followed=jerry)
    db.session.add_all([follow1, follow2, follow3, follow4])
    db.session.commit()
    print(' --completed')
