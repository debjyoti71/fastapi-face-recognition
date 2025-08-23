from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services import simple_face_service as face_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/")
async def verify_user(event_name: str = Form(...), file: UploadFile = File(...)):
    """
    Verify if a given face image belongs to a registered user in the event.
    """
    logger.info(f"POST /verify endpoint accessed for event: {event_name}")
    
    if not event_name:
        logger.warning("Verify request with empty event name")
        return JSONResponse({"verified": False, "username": None, "info": "No event was provided"})

    try:
        logger.info(f"Processing verification image for event: {event_name}")
        
        # Verify face with image file
        result = face_service.verify_face(event_name, file.file)
        logger.info(f"Verification result: {result.get('verified')} for event: {event_name}")
        return JSONResponse(result)

    except Exception as e:
        logger.error(f"Error verifying face in event {event_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
