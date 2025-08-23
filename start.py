import os
import sys

# Ensure dlib-bin is used instead of dlib
try:
    import dlib
except ImportError:
    pass

# Start the application
if __name__ == "__main__":
    from app.main import app
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)