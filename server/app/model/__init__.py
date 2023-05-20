def init_model(sqlDAO):
    from .message import Message
    sqlDAO.create_all()