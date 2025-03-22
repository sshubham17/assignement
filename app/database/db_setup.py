import traceback

from fastapi import Depends, HTTPException, Request

from app.config import db
from app.database.db_creation import create_database
from app.utils.dependencies import get_business_domain


async def setup(
    request: Request,
    business_domain = Depends(get_business_domain),
    ):
    '''
    Endpoint to create a database for a business domain.

    If the database already exists, it returns a message indicating that.
    If the payload is missing, it returns an error message.
    If any other unexpected error occurs, it returns a 500 Internal Server Error.

    Args:
        request: FastAPI Request object
        business_domain: Business domain obtained from dependencies

    Returns:
        A response indicating the success or failure of database creation.
    '''
    try:
        try:
            body = await request.json()
        except ValueError:
            return {'error':True, 'message':'Payload is missing.'}

        db_creation_response = create_database(db.DB_USER, db.DB_PASSWORD, db.DB_HOST, db.DB_PORT, business_domain, db.DB_DEFAULT_DATABASE)

        return db_creation_response
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        raise HTTPException(status_code=500,detail={'error':True,'message':str(error)}) from error
    finally:
       pass
