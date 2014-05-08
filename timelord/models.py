from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, String

import getpass
import datetime
import os

TIMELORD_INSTALL_DIRECTORY = os.path.join(os.path.expanduser('~'), '.timelord')

db_path = os.path.join(TIMELORD_INSTALL_DIRECTORY, getpass.getuser() + '.db')
engine = create_engine('sqlite:///' + db_path)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class WorkTime(Base):
    __tablename__ = 'work_time'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.now())
    work = Column(Integer, default=1)

    def __repr__(self):
        return '<WorkTime(User: %s, DateTime: %s)>' % (getpass.getuser(), str(self.datetime))


class Milestone(Base):
    __tablename__ = 'milestone'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.now())
    milestone = Column(String(250))

    def __repr__(self):
        return '<Milestone(User: %s, Description: "%s")>' % (getpass.getuser(), self.milestone[:20])

