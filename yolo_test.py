from ultralytics import YOLO
from datetime import datetime

model = YOLO("yolo26n.pt")

results = model("events/peopleCar.jpg")
detectionCount = len(results[0].boxes)
detections = []

highAlert = ["person", "car", "motorcycle", "truck", "bicycle"]

for i in range(detectionCount):
    classId = int(results[0].boxes.cls[i])
    className = results[0].names[classId]
    confidence = (float(results[0].boxes.conf[i]))
    detections.append((className, confidence))

    print("Detected:", className)
    print(f"Confidence: {(confidence*100):.2f} %")

highAlertD = {
    key: any(key == detection[0] for detection in detections)
    for key in highAlert
}

event = {
    "timestamp": datetime.now().isoformat(),
    "detections": detections
}
event["image"] = filename

# sendToGemini = any(highAlertD.values())
# print("Send to Gemini:", sendToGemini)

print(highAlertD)
print(detections)