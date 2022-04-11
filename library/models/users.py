from sqlalchemy.dialects.postgresql import UUID

from library.app import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True))
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
