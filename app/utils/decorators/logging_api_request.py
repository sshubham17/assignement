import time
from fastapi import Request
from functools import wraps

# Import the API logger
from app.utils.logger import api_logger

def log_api_requests(func):
    """
    Decorator to log API request details, including method, URL, user-agent, status code, and execution time.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract request from kwargs (FastAPI injects 'request' automatically if it's a dependency)
        request: Request = kwargs.get("request")
        
        if not request:
            api_logger.warning("No request object found, skipping logging")
            return await func(*args, **kwargs)

        # Capture request details
        method = request.method
        url = str(request.url)
        user_agent = request.headers.get("User-Agent", "Unknown")

        # Detect if it's a browser or mobile device
        if "Mobile" in user_agent:
            device_type = "Mobile"
        elif "Mozilla" in user_agent or "Chrome" in user_agent or "Safari" in user_agent:
            device_type = "Browser"
        else:
            device_type = "Unknown"

        # Start timer
        start_time = time.time()

        # Process request
        response = await func(*args, **kwargs)

        # Capture response details
        status_code = response.status_code
        execution_time = round(time.time() - start_time, 4)  # Time taken in seconds

        # Log the details
        api_logger.info(
            f"{method} {url} - Status: {status_code} - Device: {device_type} - User-Agent: {user_agent} - Time: {execution_time}s"
        )

        return response

    return wrapper
