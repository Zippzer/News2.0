from sqlalchemy import Column,Integer,Text
from db.db_connet import Base
from sqlalchemy.types import Date


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(Text)
    dashboard = Column(Text)
    dashboard_url = Column(Text)
    indicators = Column(Text)
    date = Column(Date)




