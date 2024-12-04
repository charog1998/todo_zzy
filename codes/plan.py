from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class Plan(Base):
    """计划类"""

    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    state = Column(Boolean)
    description = Column(String)
    deadline = Column(DateTime)
    cycle = Column(Integer)

    # 以下三项用 #98# 作为分隔符，把字符串变成列表
    url = Column(String)
    localFile = Column(String) # 弃用了
    imgList = Column(String) # 发现其实只保留一个图就行

    def __repr__(self) -> str:
        return f"Plan(id={self.id!r}, topic={self.topic!r}, state={self.state!r}, description={self.description!r}, deadline={self.deadline!r}, cycle={self.cycle!r}, url={self.url!r}, imgList={self.imgList!r})"


if __name__ == "__main__":
    plan = Plan(
        topic="主题",
        description="描述",
        deadline=datetime.now(),
        cycle=1,
        url="",
        localFile="",
        imgList="",
    )
    print(plan)
    print(plan.deadline)
    print(plan.deadline.strftime("%d/%m/%Y, %H:%M:%S"))
