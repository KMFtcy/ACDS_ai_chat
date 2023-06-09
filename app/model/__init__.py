def init_model(sqlDAO):
    from .message import Message
    from .user_behave import Behaviour
    sqlDAO.create_all()