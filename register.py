import cv2
import os

# Student Name
name = "Sravani"

# Create Folder Path
folder = f"dataset/{name}"

# Create Folder If Not Exists
if not os.path.exists(folder):
    os.makedirs(folder)

# Load Face Detector
face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

# Open Webcam
cap = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        # Crop Face
        face = frame[y:y+h, x:x+w]

        count += 1

        # Save Face Image
        image_path = f"{folder}/{count}.jpg"
        cv2.imwrite(image_path, face)

        print(f"Saved: {image_path}")

        # Draw Rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Registration", frame)

    # Stop After 30 Images
    if count >= 30:
        break

    # Press Q To Exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print(f"\nTotal Images Saved: {count}")
print("Registration Completed Successfully!")