from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


username = 'postgres'
password = 'admin'
host = 'localhost'
port = '5432'
database_name = 'sezon'
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database_name}')
Base = declarative_base()
