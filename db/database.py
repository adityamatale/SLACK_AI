import logging
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env into os.environ


# print('env = ',os.environ.get('POSTGRES_DB'))
# exit()

DATABASE_URL = f"postgresql://{str(os.environ.get('POSTGRES_USER','postgres'))}:{str(os.environ.get('POSTGRES_PASSWORD','root'))}@{str(os.environ.get('POSTGRES_SERVER','localhost'))}/{str(os.environ.get('POSTGRES_DB','EmpAI'))}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=50,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=3600
)
metadata = MetaData()
metadata.bind = engine
Base = declarative_base(metadata=metadata)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logging, logging.INFO),
    after=after_log(logging, logging.WARN),
)
def get_db_engine():
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
        return engine
    except Exception as e:
        logging.error(e)
        raise e

def run_init_sql(file_path):
    """Run an SQL file against the database."""
    engine = get_db_engine()
    with engine.connect() as conn:
        with open(file_path, "r") as f:
            sql = f.read()
        conn.execute(text(sql))
        conn.commit()
    print(f"{file_path} executed successfully!")

run_init_sql("SLLACK/db/init/init.sql")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_db_engine())


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()