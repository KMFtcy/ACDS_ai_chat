from app.dao import daoPool
from sqlalchemy.sql import func

db = daoPool.sqlDAO

class Behaviour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    data = db.Column(db.String(500))
    parms = db.Column(db.String(500))
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, user_id, type, data, parms=""):
        self.user_id = user_id
        self.type = type
        self.data = data
        self.parms = parms

    def __repr__(self):
        return "<User %r>" % self.user_id

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
