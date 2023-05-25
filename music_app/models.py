from .extentions import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_access_token = db.Column(db.String(38), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)


class Track(db.Model):
    __tablename__ = 'tracks'

    track_id = db.Column(db.Integer, primary_key=True)
    track_uuid = db.Column(db.String(38), nullable=False)
    track_file_bin = db.Column(db.LargeBinary, nullable=False)
    track_file_name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.user_id', ondelete='CASCADE'), 
        nullable=False,
    )