from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import db

def create_workspace_connection(workspace_name: str) -> AsyncSession:
    """
    Creates a connection to the database for a specific workspace.

    Args:
        workspace_name (str): The name of the workspace (database).

    Returns:
        async_session (sessionmaker): A sessionmaker for managing async sessions.

    Raises:
        ValueError: If there is an error creating the database connection.
    """
    # Construct the connection URL
    workspace_db_url = f"postgresql+asyncpg://{db.DB_USER}:{db.DB_PASSWORD}@{db.DB_HOST}:{db.DB_PORT}/{workspace_name}"

    try:
        # Create an asynchronous engine
        engine = create_async_engine(
            workspace_db_url,
            future=True,
            echo=False,
            pool_size=30,
            max_overflow=50,
            pool_recycle=120,
            pool_pre_ping=True
        )

        # Create a sessionmaker for managing async sessions
        async_session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            # expire_on_commit=False,
            class_=AsyncSession
        )
        SessionLocal = scoped_session(async_session)

        return SessionLocal()
    except SQLAlchemyError as e:
        raise ValueError(f"Error creating database connection: {str(e)}") from e
