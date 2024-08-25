from app import db

class Pdf(db.Model):
    __tablename__ = 'pdfs'

    id_pdf = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    tag = db.Column(db.String(255), nullable=True)

    @property
    def serialize(self):
        return {
            'id_pdf': self.id_pdf,
            'id_user': self.id_user,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'description': self.description,
            'tag': self.tag
        }