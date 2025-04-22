from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
URL_DB = "mysql+mysqlconnector://root:231219@localhost:3306/registro"
=======
URL_DB = "mysql+mysqlconnector://root:nomelase123@localhost:3306/registro"
>>>>>>> d9034e8 (Correcciones generales)

engine = create_engine(URL_DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
