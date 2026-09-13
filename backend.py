from fastapi import FastAPI
from database import getEvents, saveEvent
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import UploadFile, File, Form
import os 
import json
from supabase import create_client

supabaseUrl = os.getenv("SUPABASE_URL")
supabaseKey = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(supabaseUrl, supabaseKey)

app = FastAPI()
os.makedirs("events", exist_ok=True)
app.mount("/images", StaticFiles(directory="events"), name="images")

@app.get("/")
def root():
    return {"message": "Security Camera backend is running"}

@app.get("/events")
def events():
    return getEvents()

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")

@app.get("/manifest.json")
def manifest():
    return FileResponse("manifest.json")

@app.get("/service-worker.js")
def serviceWorker():
    return FileResponse("service-worker.js")

@app.post("/events")
async def createEvent(
    image: UploadFile = File(...),
    timestamp: str = Form(...),
    detections: str = Form(...)
):
    fileName = os.path.basename(image.filename)
    imagePath = fileName
    
    imageContents = await image.read()

    supabase.storage.from_("event-images").upload(
        path=fileName,
        file=imageContents,
        file_options={"content-type": "image/jpeg"}
    )

    detectionList = json.loads(detections)

    event = {
        "timestamp": timestamp,
        "image": imagePath,
        "detections": detectionList
    }

    saveEvent(event)

    return {
        "timestamp": timestamp,
        "detections": detections,
        "filename": image.filename
    }
