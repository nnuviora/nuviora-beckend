from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scr.conf.config import config

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/postgres"
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://${config.PG_USER}:${config.PG_PASSWORD}@${config.PG_DOMAIN}:${config.PG_PORT}/${config.PG_DB}"
SQLALCHEMY_DATABASE_URL = config.DB_URL
#print(f'SQLALCHEMY_DATABASE_URL = {SQLALCHEMY_DATABASE_URL}')
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
