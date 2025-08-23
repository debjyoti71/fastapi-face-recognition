import numpy as np
import json
import requests
import logging
import tempfile
import os
import time
from app.services import cloud_storage
from app.core import config
from PIL import Image
import io

logger = logging.getLogger(__name__)

# Simple face detection using basic image processing
def extract_simple_features(image_array):
    """Extract simple features from image for demo purposes"""
    # Convert to grayscale
    if len(image_array.shape) == 3:
        gray = np.mean(image_array, axis=2)
    else:
        gray = image_array
    
    # Simple feature extraction (histogram-based)
    hist = np.histogram(gray.flatten(), bins=50)[0]
    # Normalize
    features = hist / np.sum(hist)
    return features.tolist()

def _load_embeddings_from_cloudinary(retry_count=3):
    """Load embeddings directly from Cloudinary with retry mechanism"""
    cache_buster = int(time.time())
    url = f"https://res.cloudinary.com/{config.CLOUD_NAME}/raw/upload/face_recognition/embeddings.json?cb={cache_buster}"
    
    for attempt in range(retry_count):
        try:
            logger.info(f"Loading embeddings from Cloudinary (attempt {attempt + 1})")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                logger.info("Successfully loaded embeddings")
                return response.json()
            
            if attempt < retry_count - 1:
                logger.info(f"Retrying in 2 seconds... (attempt {attempt + 1}/{retry_count})")
                time.sleep(2)
            else:
                logger.warning(f"No embeddings found after {retry_count} attempts, status: {response.status_code}")
                
        except requests.RequestException as e:
            if attempt < retry_count - 1:
                logger.warning(f"Request failed, retrying: {e}")
                time.sleep(2)
            else:
                logger.error(f"Failed to load embeddings after {retry_count} attempts: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in embeddings: {e}")
            break
    
    return {}

def _save_embeddings_to_cloudinary(data):
    """Save embeddings directly to Cloudinary"""
    try:
        logger.info("Saving embeddings to Cloudinary")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        cloud_storage.upload_embeddings(temp_path)
        logger.info("Successfully saved embeddings")
    except Exception as e:
        logger.error(f"Failed to save embeddings: {e}")
        raise
    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)

def add_user_face(event_name: str, username: str, image_file):
    """Add a new user with simple image features"""
    if not event_name or not event_name.strip():
        logger.warning("Add user called with empty event name")
        return {"status": "error", "message": "Event name is required"}
    
    if not username or not username.strip():
        logger.warning("Add user called with empty username")
        return {"status": "error", "message": "Username is required"}

    try:
        logger.info(f"Adding user '{username}' to event '{event_name}'")
        
        # Process image
        image = np.array(Image.open(io.BytesIO(image_file.read())))
        features = extract_simple_features(image)
        
        storage_data = _load_embeddings_from_cloudinary()

        if event_name not in storage_data:
            storage_data[event_name] = {}
            logger.info(f"Created new event: {event_name}")

        if username not in storage_data[event_name]:
            storage_data[event_name][username] = []
            logger.info(f"Created new user: {username}")

        storage_data[event_name][username].append(features)
        
        logger.info(f"Data structure before saving: {list(storage_data.keys())}")
        logger.info(f"Event '{event_name}' has users: {list(storage_data[event_name].keys())}")
        
        _save_embeddings_to_cloudinary(storage_data)

        feature_count = len(storage_data[event_name][username])
        logger.info(f"Successfully added user '{username}' to '{event_name}' (total features: {feature_count})")
        return {
            "status": "success", 
            "message": f"User '{username}' successfully added to event '{event_name}'",
            "feature_count": feature_count
        }
    except Exception as e:
        logger.error(f"Error adding user '{username}' to event '{event_name}': {e}")
        return {"status": "error", "message": "Failed to add user to event"}

def verify_face(event_name: str, image_file):
    """Verify image features against event users"""
    if not event_name or not event_name.strip():
        logger.warning("Verify face called with empty event name")
        return {"verified": False, "username": None, "message": "Event name is required"}

    try:
        logger.info(f"Verifying face against event '{event_name}'")
        
        # Process image
        image = np.array(Image.open(io.BytesIO(image_file.read())))
        features = extract_simple_features(image)
        
        storage_data = _load_embeddings_from_cloudinary()
        event_users = storage_data.get(event_name, {})

        if not event_users:
            logger.info(f"Event '{event_name}' not found or has no users")
            return {
                "verified": False, 
                "username": None, 
                "message": f"Event '{event_name}' not found or has no registered users"
            }

        logger.info(f"Checking against {len(event_users)} users in event '{event_name}'")
        
        # Simple similarity threshold
        THRESHOLD = 0.3
        
        for username, user_features in event_users.items():
            for i, saved_features in enumerate(user_features):
                try:
                    # Simple cosine similarity
                    dot_product = np.dot(features, saved_features)
                    norm_a = np.linalg.norm(features)
                    norm_b = np.linalg.norm(saved_features)
                    similarity = dot_product / (norm_a * norm_b)
                    
                    if similarity > THRESHOLD:
                        logger.info(f"Match found: user '{username}' in event '{event_name}' (similarity: {similarity:.4f})")
                        return {
                            "verified": True, 
                            "username": username, 
                            "message": f"Face verified successfully for user '{username}' in event '{event_name}'",
                            "confidence": round(similarity * 100, 2)
                        }
                except Exception as e:
                    logger.warning(f"Error comparing features {i} for user '{username}': {e}")
                    continue

        logger.info(f"No match found in event '{event_name}'")
        return {
            "verified": False, 
            "username": None, 
            "message": f"No matching face found in event '{event_name}'"
        }
    except Exception as e:
        logger.error(f"Error verifying face in event '{event_name}': {e}")
        return {"verified": False, "username": None, "message": "Face verification failed due to system error"}