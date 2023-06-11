import requests

from app.model.user_behave import Behaviour as BehaviourModel
from app.service import logger
from app.dao import daoPool
from app.service import context
from app.utils import chat

sqlDAO = daoPool.sqlDAO


def get_user_behaviour(user_id):
    result = []
    try:
        query_result = (
            sqlDAO.session.query(BehaviourModel)
            .filter(BehaviourModel.user_id == user_id)
            .filter(BehaviourModel.type == "view")
            .all()
        )
        for o in query_result:
            result.append(o.to_dict())
    except Exception as e:
        print(e)
        return e
    return result


def add_one_user_behaviour(user_id, type, data):
    record = BehaviourModel(user_id, type, data)
    sqlDAO.session.add(record)
    sqlDAO.session.commit()
    return record
