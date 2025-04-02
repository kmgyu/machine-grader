from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    userid = db.Column(db.Integer, primary_key=True)  # Student Number
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))

    # 관계 설정 (optional)
    scores = db.relationship('Score', back_populates='user', cascade="all, delete-orphan")


class Score(db.Model):
    __tablename__ = 'score'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 기본 키 추가
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    username = db.Column(db.String(128))
    score = db.Column(db.Float)

    # 관계 설정 (optional)
    user = db.relationship('User', back_populates='scores')
