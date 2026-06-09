import csv
import os
from datetime import datetime

def mark_attendance(name):

    today = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    file_name = "attendance.csv"

    if not os.path.exists(file_name):
        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Date", "Time"])

    already_marked = False

    with open(file_name, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) > 1:
                if row[0] == name and row[1] == today:
                    already_marked = True
                    break

    if not already_marked:
        with open(file_name, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, today, current_time])

        print(f"Attendance Marked: {name}")