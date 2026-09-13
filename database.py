import sqlite3
import json
import os
from supabase import create_client

supabaseUrl = os.getenv("SUPABASE_URL")
supabaseKey = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(supabaseUrl, supabaseKey)

database = sqlite3.connect("security.db")
database.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        image TEXT NOT NULL,
        detections TEXT NOT NULL
    )
""")
database.commit()
database.close()

def saveEvent(event):
    supabase.table("events").insert({
        "timestamp": event["timestamp"],
        "image": event["image"],
        "detections": event["detections"]
    }).execute()

def getEvents():
    response = supabase.table("events").select("*").order(
        "timestamp",
        desc=True
    ).execute()

    events = response.data

    for event in events:
        signedUrl = supabase.storage.from_("event-images").create_signed_url(
            event["image"],
            3600
        )

        event["image"] = signedUrl["signedURL"]

    return events