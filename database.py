from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./task.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
# sessionlocal creates a session like session factory.
# when we receive a request we go to sessionlocal() and create session for that request.