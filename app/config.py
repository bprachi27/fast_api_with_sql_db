from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dayabse_url = "postgresql://postgres:prachi123@localhost:5432/company_db"

engine = create_engine(dayabse_url)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()