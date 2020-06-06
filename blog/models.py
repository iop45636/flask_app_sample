from blog import db, login_manager
from flask_login import UserMixin
from datetime import datetime
#for make format url
from sqlalchemy import event
from slugify import slugify

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150))
    profile = db.Column(db.String(150), default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(180), nullable=False)
    body = db.Column(db.Text, nullable=False)
    comments = db.Column(db.Integer, default=0)
    view = db.Column(db.Integer, default=0)
    image = db.Column(db.String(120), default='image.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    author = db.relationship('User',backref=db.backref('authors', lazy=True))
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return '<Post %r>' % self.title

    #for make format url
    @staticmethod
    def generat_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

db.event.listen(Post.title, 'set', Post.generat_slug, retval=False)