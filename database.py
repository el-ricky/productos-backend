from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://neondb_owner:npg_k5FeGP0RrNmT@ep-polished-unit-acxgu91a.sa-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()