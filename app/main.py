from fastapi import FastAPI
import logging
from app.core.logging_config import setup_logging
from app.api import routes_add, routes_verify, events

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Face Recognition Service",
    description="Microservice for user face verification and registration",
    version="1.0.0"
)

# Include routers
app.include_router(routes_verify.router, prefix="/verify", tags=["Verify"])
app.include_router(routes_add.router, prefix="/addUser", tags=["Add User"])
app.include_router(events.router, prefix="/api", tags=["Events"])

logger.info("FastAPI application initialized with all routers")

@app.on_event("startup")
async def startup_event():
    logger.info("Face Recognition API starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Face Recognition API shutting down")

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Face Recognition API is running!"}
