from app import db
from werkzeug.security import generate_password_hash, check_password_hash

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)


class BcInfo(db.Model):
    __tablename__ = "bc_detect_info"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    upload_path = db.Column(db.String(128))
    upload_date = db.Column(db.DateTime())
    model_result = db.Column(db.String(32))
    doctor_result = db.Column(db.String(32))
    report_path = db.Column(db.String(128))

    def __repr__(self):
        return '<Path {}>'.format(self.img_path)

    def obj2dict(self):
        return {'id': self.id,
               'username': self.username,
               'img_path': self.img_path,
               'model_result': self.model_result,
               'doctor_result': self.doctor_result,
               'upload_date': self.upload_date.strftime("%Y-%m-%d %H:%M:%S")
               }
