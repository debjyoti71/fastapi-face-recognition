from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services import face_service
import face_recognition
import numpy as np
from PIL import Image
import io
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
        # Load image and convert to numpy array
        image = np.array(Image.open(io.BytesIO(file.file.read())))
        logger.info(f"Verification image loaded successfully, shape: {image.shape}")

        # Encode face
        encodings = face_recognition.face_encodings(image)
        if len(encodings) == 0:
            logger.warning(f"No face detected in verification image for event: {event_name}")
            return JSONResponse({"verified": False, "username": None, "info": "No face detected in image"})
        
        embedding = encodings[0].tolist()
        logger.info(f"Face encoding generated for verification in event: {event_name}")

        # Call face_service
        result = face_service.verify_face(event_name, embedding)
        logger.info(f"Verification result: {result.get('verified')} for event: {event_name}")
        return JSONResponse(result)

    except Exception as e:
        logger.error(f"Error verifying face in event {event_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
