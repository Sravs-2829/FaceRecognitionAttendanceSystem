import cv2
from attendance import mark_attendance

# ==========================
# Face Recognizer
# ==========================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# ==========================
# Attendance Tracker
# ==========================
attendance_marked = set()

# ==========================
# Face Cascade
# ==========================
face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

# ==========================
# Registered Users
# ==========================
names = {
    0: "Divya",
    1: "Priya",
    2: "Sravani"
}

# ==========================
# Camera
# ==========================
cam = cv2.VideoCapture(0)

prev_x = 0
prev_y = 0
movement_count = 0

while True:
    ret, img = cam.read()

    # ✅ ADDED: Camera safety check
    if not ret:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # ==========================
        # Movement Detection
        # ==========================
        if abs(x - prev_x) > 5 or abs(y - prev_y) > 5:
            movement_count += 1

        prev_x = x
        prev_y = y

        # ==========================
        # Face Recognition
        # ==========================
        face_id, confidence = recognizer.predict(
            gray[y:y+h, x:x+w]
        )

        # ✅ CHANGED: Better confidence threshold
        if confidence < 100:
            name = names.get(face_id, "Unknown")
        else:
            name = "Unknown"

        # ==========================
        # Display Name
        # ==========================
        cv2.putText(
            img,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # ==========================
        # Liveness Check
        # ==========================
        if name != "Unknown":

            if movement_count > 10:

                # ✅ CHANGED:
                # Mark attendance only once
                if name not in attendance_marked:
                    mark_attendance(name)
                    attendance_marked.add(name)

                cv2.putText(
                    img,
                    "REAL FACE",
                    (x, y + h + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            else:
                cv2.putText(
                    img,
                    "SPOOF SUSPECTED",
                    (x, y + h + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

    # ✅ FIXED INDENTATION
    cv2.imshow("Face Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()