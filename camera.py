import cv2 as cv
import time
from datetime import datetime
import math
import threading
from ultralytics import YOLO
import requests
import json

model = YOLO("yolo26n.pt")

def analyze_in_background(sampledFrames, timestamp):
    print("AI analysis started")
    highAlert = ["person", "car", "motorcycle", "truck", "bicycle"]

    bestFrame = None
    bestConfidence = 0
    bestDetections = []
    allFrameDetections = []
    finalFrameNumber = 0

    for frameNumber, frame in enumerate(sampledFrames, start=1):
        print(f"\nAnalyzing frame {frameNumber} of 5")
        results = model(frame)
        detectionCount = len(results[0].boxes)
        detections = []
        frameIsBest = False

        for i in range(detectionCount):
            classId = int(results[0].boxes.cls[i])
            className = results[0].names[classId]
            confidence = float(results[0].boxes.conf[i])
            detections.append((className, confidence))

            print("Detected:", className)
            print(f"Confidence: {(confidence*100):.2f} %")

            if className in highAlert and confidence > bestConfidence:
                bestConfidence = confidence
                bestFrame = frame
                frameIsBest = True
                finalFrameNumber = frameNumber

        allFrameDetections.append(detections.copy())

        if frameIsBest:
            bestDetections = detections.copy()

    if bestFrame is None:
        bestFrame = sampledFrames[2]
        bestDetections = allFrameDetections[2]
        finalFrameNumber = 3

    filename = f"events/motion_{timestamp}.jpg"
    cv.imwrite(filename, bestFrame)

    event = {
        "timestamp": datetime.now().isoformat(),
        "image": filename,
        "detections": bestDetections
    }
    with open(filename, "rb") as imageFile:
        files = {
            "image": imageFile
        }

        data = {
            "timestamp": event["timestamp"],
            "detections": json.dumps(event["detections"])
        }

        response = requests.post(
            "https://security-camera-backend.onrender.com/events",
            files=files,
            data=data
        )

    print("Backend response:", response.status_code)
    if response.status_code == 200:
        print(f"Event with frame {finalFrameNumber} sent to backend")
    else:
        print("Backend error:", response.status_code, response.text)
        print(event)

    return bestDetections

camera = 1
cameraStart = time.time()
cap = cv.VideoCapture(camera)
time.sleep(2)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)

elapsed_time = time.time()-cameraStart
w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

print(f'Initializing camera {camera} took {elapsed_time:.2f} seconds')
print(f'Frame size = ({h} ,{w})')

count = 0

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
        
        if motionScore > 1.2 and currentTime - lastMotionTime > 15: 
            print("Motion detected!!")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            sampledFrames = []
            startTime = time.time()
            nextSampleTime = 0

            while len(sampledFrames) < 5:
                ret, frame = cap.read()

                if not ret:
                    continue

                elapsedTime = time.time() - startTime

                if elapsedTime >= nextSampleTime:
                    sampledFrames.append(frame)
                    nextSampleTime += 0.5

            thread = threading.Thread(
                target=analyze_in_background,
                args=(sampledFrames, timestamp)
            )

            thread.start()

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

