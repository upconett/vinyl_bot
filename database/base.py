from sqlalchemy import create_engine

from database.models import Base

engine = create_engine("sqlite:///location_test.db", echo=True)

if not engine.dialect.has_table(engine.connect(), 'users'):
    Base.metadata.create_all(engine)