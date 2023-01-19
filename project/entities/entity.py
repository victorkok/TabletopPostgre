from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Abaixo são as variaveis da database que eu criei no meu localhost, provavelmente não vai funcionar no seu caso mão crie a mesma db
"""

db_url = 'localhost:5433'
db_name = 'siprojeto'
db_user = 'postgres'
db_password = 'victor01'
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity():
    id = Column(Integer, primary_key=True)