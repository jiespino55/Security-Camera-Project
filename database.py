import sqlite3
import json

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
    connection = sqlite3.connect("security.db")
    connection.execute(
        "INSERT INTO events (timestamp, image, detections) VALUES (?, ?, ?)",
        (
            event["timestamp"],
            event["image"],
            json.dumps(event["detections"])
        )
    )
    connection.commit()
    connection.close()

def getEvents():
    connection = sqlite3.connect("security.db")
    rows = connection.execute(
        "SELECT * FROM events ORDER BY timestamp DESC"
    ).fetchall()
    connection.close()

    events = []
    for row in rows:
        try:
            detections = json.loads(row[3])
        except json.JSONDecodeError:
            detections = []

        events.append({
            "id": row[0],
            "timestamp": row[1],
            "image": "/images/" + row[2].split("/")[-1],
            "detections": detections
        })

    return events