from fastapi import APIRouter, FastAPI, Request, Response
from app.dto.dto import UserContext
from app.utils.logger import logger, api_logger
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.database.db_connection import create_workspace_connection as db_conn
from app.routers import db_setup, orders, products
from app import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Server has started successfully!")
    yield  # Startup logic runs before this, and shutdown logic goes after
    logger.info("🛑 Server is shutting down...")

app = FastAPI(
    title="FastAPI Logging Demo",
    description=config.info.app_description,
    version=config.settings.api_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log API requests"""
    response = Response("Internal server error", status_code=500)
    try:
        user_context = UserContext()
        domain = request.headers['domain']
        setattr(user_context, 'business_domain', domain)
        logger.info(f"API Request: {request.method} {request.url}")
        async with db_conn(domain.replace("-", "_")) as db:
            setattr(user_context, 'db', db)  # Attach the database connection to request state
            request.state.user_context = user_context
            response = await call_next(request)
            logger.info(f"API Response: {response.status_code}")
    finally:
        request.state.db = None
    return response

router = APIRouter(prefix="/api/v1")
router.include_router(db_setup.router)
router.include_router(orders.router)
router.include_router(products.router)

# Default route to check fastapi service status
@router.get("/info")
async def root():
    '''Check service health and version'''
    return {
        "app_name": config.info.app_name,
        "version": config.settings.api_version,
        "status": "running"
    }

app.include_router(router)
