from sqlalchemy import create_engine

from database.models import Base
from create_bot import dbfile

engine = create_engine("sqlite:///{0}".format(dbfile), echo=True)

if not engine.dialect.has_table(engine.connect(), 'users'):
    Base.metadata.create_all(engine)