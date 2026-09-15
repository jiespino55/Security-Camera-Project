# AI Security Camera

An AI-powered security camera system built with Python, OpenCV, and YOLO. The system monitors a live camera feed for motion, captures security events, uses object detection to identify relevant objects, and sends event data to a cloud-hosted backend.

Captured events are stored using PostgreSQL and private object storage through Supabase and can be viewed through a web dashboard.

## Features

- Real-time camera monitoring with OpenCV
- Motion detection and automatic event capture
- YOLO object detection for captured security events
- Background processing using Python threads
- REST API built with FastAPI
- PostgreSQL event storage with Supabase
- Private image storage with Supabase Storage
- Secure temporary image URLs for viewing captured events
- Web dashboard for viewing security events
- Automatic dashboard updates for new events
- Cloud-hosted backend deployed on Render

## How It Works

1. OpenCV continuously reads frames from the camera.
2. Consecutive frames are compared to detect significant motion.
3. When motion is detected, the system waits briefly before capturing an image so that the moving object has more time to enter the frame.
4. YOLO analyzes the captured image and identifies detected objects and their confidence scores.
5. The camera client sends the event information and captured image to the FastAPI backend using an HTTP POST request.
6. The backend uploads the image to a private Supabase Storage bucket.
7. Event metadata, including the timestamp, image path, and detections, is stored in a PostgreSQL database.
8. The web dashboard retrieves events through the FastAPI API.
9. Temporary signed URLs provide secure access to captured images stored in the private bucket.
10. The dashboard periodically checks for new events and displays them automatically.

## Architecture

```text
Camera / OpenCV
        |
        v
Motion Detection
        |
        v
YOLO Object Detection
        |
        v
FastAPI REST API (Render)
        |
        +-------------------+
        |                   |
        v                   v
PostgreSQL             Supabase Storage
(Event Data)             (Images)
        |                   |
        +---------+---------+
                  |
                  v
             Web Dashboard
```

## Technologies

- Python
- OpenCV
- YOLO
- FastAPI
- PostgreSQL
- Supabase
- Supabase Storage
- Render
- HTML, CSS, and JavaScript
- REST APIs
- Git and GitHub

## Project Status

The core security camera pipeline is functional, including motion detection, object detection, cloud event storage, private image storage, and remote event viewing through the web dashboard.

Additional features are currently being developed, including real-time push notifications for security-relevant events.
