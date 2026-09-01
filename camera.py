import cv2 as cv
import time
from datetime import datetime
import math
# from ai import analyze_image
import threading
from ultralytics import YOLO
from database import saveEvent

# database = sqlite3.connect("security.db")
# database.execute("""
#     CREATE TABLE IF NOT EXISTS events (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         timestamp TEXT NOT NULL,
#         image TEXT NOT NULL,
#         detections TEXT NOT NULL
#     )
# """)
# database.commit()
model = YOLO("yolo26n.pt")

# def saveEvent(event):
#     connection = sqlite3.connect("security.db")
#     connection.execute(
#         "INSERT INTO events (timestamp, image, detections) VALUES (?, ?, ?)",
#         (
#             event["timestamp"],
#             event["image"],
#             json.dumps(event["detections"])
#         )
#     )
#     connection.commit()
#     connection.close()

def analyze_in_background(filename):
    print("AI analysis started")
    # result = analyze_image(filename)
    # print(result)
    # print("Fake AI response")
    results = model(filename)
    detectionCount = len(results[0].boxes)
    detections = []

    highAlert = ["person", "car", "motorcycle", "truck", "bicycle"]

    for i in range(detectionCount):
        classId = int(results[0].boxes.cls[i])
        className = results[0].names[classId]
        confidence = float(results[0].boxes.conf[i])
        detections.append((className, confidence))

        print("Detected:", className)
        print(f"Confidence: {(confidence*100):.2f} %")

    highAlertD = {
        key: any(key == detection[0] for detection in detections)
        for key in highAlert
    }

    event = {
        "timestamp": datetime.now().isoformat(),
        "image": filename,
        "detections": detections
    }
    saveEvent(event)
    print("Event saved to database")
    print(event)

    return detections

camera = 0
cameraStart = time.time()
cap = cv.VideoCapture(camera)
time.sleep(2)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

elapsed_time = time.time()-cameraStart
w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

print(f'Initializing camera {camera} took {elapsed_time:.2f} seconds')
print(f'Frame size = ({h} ,{w})')

count = 0
# start = time.time()

for _ in range(15):
    cap.read()

lastMotionTime = 0
ok, firstFrame = cap.read()

if not ok:
    print("Error reading initial frame")
    cap.release()
    exit()

prevFrame = cv.cvtColor(firstFrame, cv.COLOR_BGR2GRAY)
prevFrame = cv.GaussianBlur(prevFrame, (21, 21), 0)

start = time.time()

while True:

    count+=1

    ok, img = cap.read()
    if not ok:
        print('Error reading image')
        break

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (21, 21), 0)

    if prevFrame is not None:
        diff = cv.absdiff(prevFrame, blurred)
        motionScore = diff.mean()

        currentTime = time.time()
        
        if motionScore > 3.0 and currentTime - lastMotionTime > 15: 
            print("Motion detected!!")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            #I want to save the image as "events/motion_detection_YYYY-MM-DD_HH-MM-SS.jpg"
            filename = f"events/motion_{timestamp}.jpg"
            cv.imwrite(filename, img)

            thread = threading.Thread(
                target=analyze_in_background,
                args=(filename,)
            )
            thread.start()
            
            # result = analyze_image(filename)
            # print(result)
            
            print(f"Saved: {filename}")

            lastMotionTime = currentTime

    prevFrame = blurred

    cv.imshow('Image',img)
    k = cv.waitKey(1) # if character 'q' is pressed, exit
    if k == ord('q'):
        break
        

        
elapsed_time = time.time()-start
gcd = math.gcd(img.shape[0], img.shape[1])
print(f'Image shape: {img.shape}')
print(f'Aspect ratio: {img.shape[0]//gcd}/{img.shape[1]//gcd}')
print(f'Captured {count} frames')
print(f'Capture speed: {count/elapsed_time:.2f} frames per second')
cap.release()
cv.destroyAllWindows()

