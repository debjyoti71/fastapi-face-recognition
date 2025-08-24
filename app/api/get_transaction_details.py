from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import pytesseract
import io
import re
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/")
async def get_transaction_details(file: UploadFile = File(...)):
    try:
        # Read the image from the upload
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Extract text using OCR
        text = pytesseract.image_to_string(image)

        # Normalize and parse text
        text = text.replace('\n', ' ').replace('\r', '').strip()

        # Extract key data using regex or keyword parsing
        amount_match = re.search(r'₹\s?(\d+)', text)
        amount = amount_match.group(1) if amount_match else None

        status = "Payment Successful" if "Payment Successful" in text else None

        to_match = re.search(r'To:\s*([A-Za-z\s]+)', text)
        to_name = to_match.group(1).strip() if to_match else None

        from_match = re.search(r'From:\s*([A-Za-z\s]+)', text)
        from_name = from_match.group(1).strip() if from_match else None

        upi_ref_match = re.search(r'UPI Ref\. No\.\s*[:\-]?\s*([\d\s]+)', text)
        upi_ref = upi_ref_match.group(1).strip() if upi_ref_match else None

        date_match = re.search(r'(\d{1,2} [A-Za-z]{3,9} \d{4})', text)
        date = date_match.group(1) if date_match else None

        time_match = re.search(r'(\d{1,2}:\d{2}\s?(?:AM|PM|am|pm))', text)
        time = time_match.group(1) if time_match else None

        response = {
            "status": status,
            "amount": amount,
            "to_name": to_name,
            "from_name": from_name,
            "upi_reference": upi_ref,
            "date": date,
            "time": time,
            "raw_text": text  # Optional: helpful for debugging
        }

        return response

    except Exception as e:
        logger.exception("Failed to extract transaction details")
        raise HTTPException(status_code=500, detail=str(e))
