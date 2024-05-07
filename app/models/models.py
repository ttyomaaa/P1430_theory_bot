import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = 'question'
    id_question = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    id_chapter = Column(Integer, nullable=False)
    q_number = Column(Integer, nullable=False)
    q_file = Column(String(1000), unique=False, nullable=True)
    question = Column(String(1000), unique=False, nullable=False)


class Answer(Base):
    __tablename__ = 'answer'
    id_answer = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    id_question = Column(Integer, ForeignKey('question.id_question'))
    a_number = Column(Integer, nullable=False)
    answer = Column(String(1000), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    id_chapter = relationship('Question')
    q_number = relationship('Question')


class Form(Base):
    __tablename__ = 'form'
    id_form = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    id_question = Column(Integer, ForeignKey('question.id_question'))
    id_answer = Column(Integer, ForeignKey('answer.id_answer'))
    user_tg_id = Column(String(1000), nullable=False)
    id_tg = Column(Integer, nullable=False)
    id_forms_data = Column(Integer, ForeignKey('forms_data.id_forms_data'))
    id_chapter = relationship('Question')
    question = relationship('Question')
    answer = relationship('Answer')


class FormsData(Base):
    __tablename__ = 'forms_data'
    id_forms_data = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    result = Column(Integer, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    id_chapter = Column(Integer, nullable=True)
    form = relationship('Form')


