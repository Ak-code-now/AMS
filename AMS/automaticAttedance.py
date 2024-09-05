import tkinter as tk
from tkinter import *
import os
import cv2
import csv
import pandas as pd
import datetime
import time

haarcasecade_path = "D:\\AMS\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "D:\\AMS\\TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "D:\\AMS\\TrainingImage"
studentdetail_path = (
    "D:\\AMS\\StudentDetails\\studentdetails.csv"
)
attendance_path = "D:\\AMS\\Attendance"

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20

        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read(trainimagelabel_path)

            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)

            while True:
                ret, im = cam.read()
                if not ret:
                    print("Failed to capture image from camera.")
                    break

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                    if conf < 70:
                        Subject = sub
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                        aa = df.loc[df["Enrollment"] == Id]["Name"].values
                        tt = str(Id) + "-" + aa
                        attendance.loc[len(attendance)] = [Id, aa]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0), 4)
                    else:
                        Id = "Unknown"
                        tt = str(Id)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                if time.time() > future:
                    break

                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                cv2.imshow("Filling Attendance...", im)
                if cv2.waitKey(30) & 0xFF == 27:
                    break

            cam.release()
            cv2.destroyAllWindows()

            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            Hour, Minute, Second = timeStamp.split(":")

            path = os.path.join(attendance_path, sub)
            os.makedirs(path, exist_ok=True)  # Create the directory if it does not exist

            fileName = os.path.join(
                path,
                f"{sub}.csv"
            )

            attendance[date] = 1
            attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
            attendance.to_csv(fileName, index=False)

            m = f"Attendance Filled Successfully for {sub}"
            Notifica.configure(
                text=m,
                bg="white",
                fg="green",
                width=33,
                relief=FLAT,
                bd=5,
                font=("Arial bold", 15,),
            )
            text_to_speech(m)
            Notifica.place(x=20, y=250)

            print(f"Attendance file saved at: {fileName}")

            root = tk.Tk()
            root.title(f"Attendance of {sub}")
            root.configure(background="white")

            with open(fileName, newline="") as file:
                reader = csv.reader(file)
                r = 0
                for col in reader:
                    c = 0
                    for row in col:
                        label = tk.Label(
                            root,
                            width=10,
                            height=1,
                            fg="yellow",
                            font=("times", 15, "bold"),
                            bg="black",
                            text=row,
                            relief=tk.RIDGE,
                        )
                        label.grid(row=r, column=c)
                        c += 1
                    r += 1

            root.mainloop()

        except Exception as e:
            f = f"An error occurred: {str(e)}"
            text_to_speech(f)
            cv2.destroyAllWindows()
            

    # GUI setup
    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="white")

    titl = tk.Label(subject, bg="sky blue", relief=FLAT, bd=10, font=("Arial Bold", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="sky blue",
        fg="white",
        font=("Arial Bold", 25),
    )
    titl.place(x=100, y=12)

    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("Arial", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(os.path.join(attendance_path, sub))

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=5,
        font=("Arial Bold", 15),
        bg="green",
        fg="white",
        height=1,
        width=10,
        relief=FLAT,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="White",
        fg="black",
        bd=5,
        relief=FLAT,
        font=("Arial Bold", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="White",
        fg="Black",
        relief=RIDGE,
        font=("Arial Bold", 30,),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=5,
        font=("Arial Bold", 15),
        bg="green",
        fg="white",
        height=1,
        width=12,
        relief=FLAT,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()
