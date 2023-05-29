import openai
import requests

from app.model.message import Message as MessageModel
from app.service import logger
from app.dao import daoPool
from app.service import context
from app.utils import chat

sqlDAO = daoPool.sqlDAO
openai.api_key  = context.config["OPENAI_API_KEY"]

def get_user_messages(user_id):
    result = []
    try:
        query_result = MessageModel.query.filter_by(user_id=user_id).all()
        if len(query_result) == 0:
            logger.warn("No messages, first init.")
            first_msg = insert_first_reply(user_id)
            result.append(first_msg.to_dict())
        else:
            for o in query_result:
                result.append(o.to_dict())
    except Exception as e:
        print(e)
        return e
    return result

def add_one_message(user_id,new_message):
    history = []
    query_result = MessageModel.query.filter_by(user_id=user_id).all()
    if len(query_result) == 0:
        raise Exception("The user does not chat before, should login first.")
    for o in query_result:
        if o.author == "ai":
            role = "assistant"
        else:
            role = "user"
        content = o.data
        one_message = {
            "role": role,
            "content": content
        }
        history.append(one_message)
    history.append({
        "role": "user",
        "content": new_message
    })
    ai_reply = chat.collect_messages(history)
    user_message_model = MessageModel(user_id=user_id,data = new_message,author="me")
    sqlDAO.session.add(user_message_model)
    ai_message_model = MessageModel(user_id=user_id,data = ai_reply,author="ai")
    sqlDAO.session.add(ai_message_model)
    sqlDAO.session.commit()
    return ai_message_model

def insert_first_reply(user_id):
    default_message = '''Hello! I am ShoppingBot, an automated assistant to help you find the ideal product in this online shopping mall. How can I assist you today? Would you like me to make a recommendation or summarize product reviews?
    '''
    first_message = MessageModel(user_id=user_id,data = default_message,author="ai")
    sqlDAO.session.add(first_message)
    sqlDAO.session.commit()
    return first_message