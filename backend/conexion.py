from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
URL_DB = "mysql+mysqlconnector://root:1806@localhost:3306/registro"
=======
URL_DB = "mysql+mysqlconnector://root:231219@localhost:3306/registro"
>>>>>>> 36bd3d0bfa1645b93da6907cb5f16ec72d7479be
engine = create_engine(URL_DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
