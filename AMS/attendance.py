import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# engine = pyttsx3.init()
# engine.say("Welcome!")
# engine.say("Please browse through your options..")
# engine.runAndWait()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "D:\\AMS\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "D:\\AMS\\Trainner.yml"
)
trainimage_path = "D:\\AMS\\TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "D:\\AMS\\StudentDetails\\studentdetails.csv"
)
attendance_path = "D:\\AMS\\Attendance"


window = Tk()
window.title("Face Recognition-Based Attendance Management System")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="white")


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="black")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="black",
        font=("times", 20, " bold "),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="black",
        width=9,
        height=1,
        activebackground="Red",
        font=("times", 20, " bold "),
    ).place(x=110, y=50)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


logo = Image.open("D:\\AMS\\UI_Image\\0001.png")
logo = logo.resize((70, 52), Image.Resampling.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="skyblue", relief=FLAT, bd=10, font=("arial", 35))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1,)
l1.place(x=120, y=10)

titl = tk.Label(
    window, text="INSTITUTE OF MANAGAMENT & ENTREPRENUERSHIP DEVELOPMENT", bg="skyblue", fg="white", font=("Arial Bold", 27),
)
titl.place(x=225, y=12)

a = tk.Label(
    window,
    text="Welcome to the Face Recognition Based\nAttendance Management System",
    bg="white",
    fg="black",
    bd=10,
    font=("arial", 35),
)
a.pack()

ri = Image.open("D:\\AMS\\UI_Image\\register.jpg")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r)
label1.image = r
label1.place(x=100, y=270)

ai = Image.open("D:\\AMS\\UI_Image\\attendance.jpg")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a)
label2.image = a
label2.place(x=650, y=270)

vi = Image.open("D:\\AMS\\UI_Image\\verifyy.jpg")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v)
label3.image = v
label3.place(x=1200, y=270)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="white")
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="sky blue", relief=FLAT, bd=10, font=("arial bold", 35))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register Student Face", bg="skyblue", fg="white", font=("Arial Bold", 30),
    )
    titl.place(x=210, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="White",
        fg="black",
        bd=10,
        font=("Arial Bold", 24),
    )
    a.place(x=280, y=80)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Class Roll No",
        width=10,
        height=2,
        bg="White",
        fg="black",
        bd=5,
        relief=FLAT,
        font=("Arial Bold", 14),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="White",
        fg="green",
        relief=RIDGE,
        font=("Arial", 25, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="White",
        fg="black",
        bd=5,
        relief=FLAT,
        font=("Arial Bold", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="White",
        fg="green",
        relief=RIDGE,
        font=("Arial", 25, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="white",
        fg="black",
        bd=5,
        relief=FLAT,
        font=("Arial Bold", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=34,
        height=2,
        bd=5,
        bg="White",
        fg="green",
        relief=FLAT,
        font=("Arial", 14,),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Arial Bold", 18),
        bg="green",
        fg="white",
        height=1,
        width=13,
        relief=FLAT,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="Train Image\n(After Take Image)",
        command=train_image,
        bd=10,
        font=("Arial Bold", 18),
        bg="green",
        fg="white",
        height=1,
        width=14,
        relief=FLAT,
    )
    trainImg.place(x=360, y=350)


r = tk.Button(
    window,
    text="Register New Student",
    command=TakeImageUI,
    font=("Arial Bold", 16),
    bg="green",
    fg="white",
    height=2,
    width=17,
)
r.place(x=100, y=520)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    font=("Arial Bold", 16),
    bg="green",
    fg="white",
    height=2,
    width=17,
)
r.place(x=650, y=520)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    font=("Arial Bold", 16),
    bg="green",
    fg="white",
    height=2,
    width=17,
)
r.place(x=1200, y=520)
r = tk.Button(
    window,
    text="EXIT",
    command=quit,
    font=("Arial Bold", 16),
    bg="red",
    fg="white",
    height=2,
    width=17,
)
r.place(x=650, y=660)

window.mainloop()
