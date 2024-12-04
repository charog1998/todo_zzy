from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from plan import Base, Plan

engine = create_engine("sqlite:///Plans.db", echo=True)
Session = sessionmaker(bind=engine)
# 实例化
session = Session()


def insert(plan: Plan):
    session.add(plan)
    session.commit()

def delete(plan: Plan):
    session.delete(plan)
    session.commit()

def delete_by_id(id: int):
    plan_deleted = select_by_id(id)
    delete(plan_deleted)

def select_by_topic(topic: str='') -> list[Plan]:
    stmt = session.query(Plan).order_by(Plan.state.asc()).order_by(Plan.deadline.asc()).filter(Plan.topic.like('%'+topic+'%')).all()
    return stmt

def select_by_id(id: int) -> Plan | None:
    stmt = session.query(Plan).order_by(Plan.state.asc()).order_by(Plan.deadline.asc()).filter(Plan.id == id).first()
    return stmt

def replace(plan: Plan):
    '''替换原有记录（用于编辑）'''
    plan_replaced = select_by_id(plan.id)
    plan_replaced = plan
    session.commit()

def init_db():
    Base.metadata.create_all(engine)