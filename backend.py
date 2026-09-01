from fastapi import FastAPI
from database import getEvents
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
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

