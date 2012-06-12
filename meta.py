from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///teste.sqlite', echo=False)
session = sessionmaker(bind=engine)()
Base = declarative_base()

def criar_metadados():
    Base.metadata.create_all(engine)
