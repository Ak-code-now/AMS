import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            text_to_speech('Please enter the subject name.')
            return

        base_path = r"D:\AMS\Attendance"
        subject_path = os.path.join(base_path, Subject)
        if not os.path.isdir(subject_path):
            messagebox.showerror("Error", "Subject directory does not exist.")
            return

        # Define the file paths
        filenames = glob(os.path.join(subject_path, f"{Subject}*.csv"))
        if not filenames:
            messagebox.showerror("Error", "No CSV files found for the subject.")
            return

        # Read and merge CSV files
        df_list = [pd.read_csv(f) for f in filenames]
        merged_df = pd.concat(df_list, ignore_index=True)
        merged_df.fillna(0, inplace=True)

        # Create or update the subject CSV file with date-wise columns
        today_date = datetime.now().strftime("%Y-%m-%d")
        subject_file = os.path.join(base_path, f"{Subject}.csv")

        if os.path.isfile(subject_file):
            existing_df = pd.read_csv(subject_file)
            if today_date in existing_df.columns:
                messagebox.showinfo("Info", "Attendance for today is already recorded.")
                return
            else:
                # Add new date column with attendance percentages
                existing_df[today_date] = merged_df.iloc[:, 2:].mean(axis=1).round().astype(int)
                existing_df[today_date] = existing_df[today_date].astype(str)
                existing_df.to_csv(subject_file, index=False)
        else:
            new_df = pd.DataFrame()
            new_df["Enrollment"] = merged_df["Enrollment"]
            new_df[today_date] = merged_df.iloc[:, 2:].mean(axis=1).round().astype(int).astype(str)
            new_df.to_csv(subject_file, index=False)

        # Display the updated attendance data
        root = tk.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")

        with open(subject_file) as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                for c, cell in enumerate(row):
                    label = tk.Label(
                        root,
                        width=15,
                        height=1,
                        fg="yellow",
                        font=("times", 15, "bold"),
                        bg="black",
                        text=cell,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)

        root.mainloop()
        print(f"Updated attendance data for {Subject}.")

    def Attf():
        sub = tx.get()
        if sub == "":
            text_to_speech("Please enter the subject name!")
        else:
            subject_path = os.path.join(r"D:\AMS\Attendance", sub)
            if os.path.isdir(subject_path):
                os.startfile(subject_path)
            else:
                messagebox.showerror("Error", "Subject directory does not exist.")

    # Main GUI setup
    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="white")

    titl = tk.Label(subject, bg="sky blue", relief=tk.FLAT, bd=10, font=("Arial Bold", 30))
    titl.pack(fill=tk.X)

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="sky blue",
        fg="white",
        font=("Arial Bold", 25),
    )
    titl.place(x=50, y=12)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="white",
        fg="black",
        bd=5,
        relief=tk.FLAT,
        font=("Arial Bold", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="white",
        fg="black",
        relief=tk.RIDGE,
        font=("Arial", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=5,
        font=("Arial Bold", 15),
        bg="green",
        fg="white",
        height=1,
        width=12,
        relief=tk.FLAT,
    )
    fill_a.place(x=195, y=170)

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
        relief=tk.FLAT,
    )
    attf.place(x=360, y=170)

    subject.mainloop()

