from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import (
    create_engine,
    MetaData
)

# access sqlite

engine = create_engine('sqlite:///sss.sqlite', echo=False)
m = MetaData(bind=engine)
Base = declarative_base(metadata=m)   

Base.metadata.create_all(engine)
sss_session_maker = sessionmaker(bind=engine)
