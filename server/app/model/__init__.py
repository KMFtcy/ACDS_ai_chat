def init_model(sqlDAO):
    from .message import User
    sqlDAO.create_all()