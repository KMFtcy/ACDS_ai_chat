from app.dao import daoPool

db = daoPool.sqlDAO

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)

    def __init__(self, user_id):
            self.user_id = user_id

    def __repr__(self):
        return '<User %r>' % self.user_id

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
