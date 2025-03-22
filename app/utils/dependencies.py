from fastapi import Header, Request, HTTPException

async def validate_domain(domain: str = Header(...)):
    """
    Validate x-api-token as part of authentication
    """
    if domain is None:
        raise HTTPException(status_code=400, detail="Forbidden! Business domain missing")
    return {
        "msg":"Do something"}

def get_business_domain(request: Request):
    return request.state.user_context.business_domain

def get_db(request: Request):
    return request.state.user_context.db