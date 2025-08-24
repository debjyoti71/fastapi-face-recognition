from fastapi import APIRouter, File, UploadFile, Form, HTTPException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def get_transaction_details(file: UploadFile = File(...)):
    
    pass