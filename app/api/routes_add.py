from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services import simple_face_service as face_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/")
async def add_user(event_name: str = Form(...), username: str = Form(...), file: UploadFile = File(...)):
    """
    Add a new user with a face image to a specific event.
    """
    logger.info(f"POST /addUser endpoint accessed for event: {event_name}, user: {username}")
    
    if not event_name:
        logger.warning("Add user request with empty event name")
        return JSONResponse({"status": "error", "message": "No event was provided"})

    try:
        logger.info(f"Processing image upload for user: {username}")
        
        # Add user with image file
        result = face_service.add_user_face(event_name, username, file.file)
        logger.info(f"Add user result: {result.get('status')} for {username}")
        return JSONResponse(result)

    except Exception as e:
        logger.error(f"Error adding user {username} to event {event_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
