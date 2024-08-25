from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(190))
    password_hash = db.Column(db.String(190))
    email = db.Column(db.String(190))
    phone = db.Column(db.String(190))
    pdfs = db.relationship('Pdf', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self):
        return create_access_token(identity=self.id_user, expires_delta=datetime.timedelta(days=1))

    @property
    def serialize(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
