from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from app.config import Config

# Define the base class for declarative models
Base = declarative_base()

# Create the engine using the database URI from the configuration
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={"timeout": 15})

# Define a scoped session
session = scoped_session(sessionmaker(bind=engine))


def add_worker(new_worker):
    """
    Adds a new worker record to the database with proper transaction handling.

    :param new_worker: An instance of your Worker model.
    """
    try:
        # Add the new worker to the session
        session.add(new_worker)
        # Commit the transaction
        session.commit()
        print("Worker added successfully!")
    except Exception as e:
        # Roll back the transaction on error
        session.rollback()
        print("An error occurred, transaction rolled back:", e)
        # Optionally re-raise the exception to handle it further up the chain
        raise
    finally:
        # Remove the session from the scoped_session registry
        session.remove()
