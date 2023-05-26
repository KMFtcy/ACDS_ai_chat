import openai
import requests

from app.model.message import Message as MessageModel
from app.service import logger
from app.dao import daoPool
from app.service import context

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
    ai_reply = get_reply_from_openai(user_id,history, new_message)
    user_message_model = MessageModel(user_id=user_id,data = new_message,author="user")
    sqlDAO.session.add(user_message_model)
    ai_message_model = MessageModel(user_id=user_id,data = ai_reply,author="ai")
    sqlDAO.session.add(ai_message_model)
    sqlDAO.session.commit()
    return ai_message_model

def get_reply_from_openai(user_id,history, message):

    URL = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 1.0,
        "messages": history
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    # response = requests.post(URL, headers=headers, json=payload)
    # response = response.json()
    # reply = response["choices"][0]["message"]["content"]

    reply = "Sorry, I can't hear you clearly. Please speak louder!"
    return reply

def insert_first_reply(user_id):
    default_message = '''Hello! I am ShoppingBot, an automated assistant to help you find the ideal product in this online shopping mall. How can I assist you today? Would you like me to make a recommendation or summarize product reviews?Hello! I am ShoppingBot, an automated assistant to help you find the ideal product in this online shopping mall. How can I assist you today? Would you like me to make a recommendation or summarize product reviews?
    '''
    first_message = MessageModel(user_id=user_id,data = default_message,author="ai")
    sqlDAO.session.add(first_message)
    sqlDAO.session.commit()
    return first_message