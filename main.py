"""
Legacy main.py - redirects to new layered architecture.
"""

# Import and run the new layered application
from src.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
