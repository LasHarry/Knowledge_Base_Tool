from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class KnowledgeBase(db.Model):
    __tablename__ = 'kbase'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(99))
    trust_score = db.Column(db.Float)

    def __init__(self, full_name, trust_score):
        self.full_name = full_name
        self.trust_score = trust_score
