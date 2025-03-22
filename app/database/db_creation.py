import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.db_table_orm_models import Base

def create_database(db_user, db_password, db_host, db_port, new_db_name, db_default_database):
    if not database_exists(db_user, db_password, db_host, db_port, new_db_name):
        # Create the new database using psycopg2
        conn = psycopg2.connect(
            dbname=db_default_database,
            user=db_user,
            password=db_password,
            host=db_host,
            port=int(db_port)
        )

        # Call the function to create the table and insert default data
        # create_and_insert_database_version_history(conn, current_db_version)

        conn.autocommit = True  # Disable transaction for creating a database

        cursor = conn.cursor()
        # NOTE: PostgreSQL database names cannot contain hyphens ("-") so we replace hyphens with underscores.
        new_db_name = new_db_name.replace("-", "_")
        cursor.execute(f'CREATE DATABASE {new_db_name};')
        cursor.close()
        conn.close()

        # Now, switch to the newly created database
        SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{int(db_port)}/{new_db_name}"
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)

        conn = psycopg2.connect(
            dbname=new_db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=int(db_port)
        )
        conn.autocommit = True  # Disable transaction for creating a database

        # Close the connection
        conn.close()

        return {'error': False, 'message': 'Database created successfully.', 'data': {}}
    else:
        return {'error': False, 'message': 'Database already exists.', 'data': {}}


def database_exists(db_user, db_password, db_host, db_port, database_name):
    try:
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{int(db_port)}/{database_name}"
        # Parse the database URL to extract connection parameters
        conn_params = psycopg2.extensions.parse_dsn(database_url)

        # Establish a connection to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)

        # Close the connection
        conn.close()

        return True
    except OperationalError:
        return False