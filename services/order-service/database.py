from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# The database URL (SQLite creates a local file named orders.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./orders.db"

# Engine is responsible for the actual connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models to inherit from
Base = declarative_base()

# Dependency to get the database session in our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()