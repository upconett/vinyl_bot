from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect


from database.models import Base
from create_bot import dbfile

engine = create_engine('sqlite:///{0}'.format(dbfile))

if not inspect(engine).has_table('users'):
    Base.metadata.create_all(engine)
engine.dispose()

async_engine = create_async_engine("sqlite+aiosqlite:///{0}".format(dbfile))
