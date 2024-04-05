from imports import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from Validate import IsValid
from data_collect_v2 import Data
import re


def submit_score(user_id_entry, test_id_entry, score_entry, accept_var):
    try:
        # Your data insertion code here using the connection object
        insertData = Data()
        accepted = accept_var.get()
        if accepted == "Accepted":
            # Test info
            user_id = user_id_entry.get()
            test_id = test_id_entry.get()
            score = score_entry.get()
            try:
                user_id = int(user_id)
                test_id = int(test_id)
                score = int(score)
            except ValueError:
                tk.messagebox.showwarning(title="Error", message="Invalid data")
                return

            if user_id and test_id and score:
                # Consider adding more validation logic for score
                if insertData.checkUserIdExists(user_id):
                    pass
                else:
                    tk.messagebox.showwarning(title="Error", message="User does not exist")
                if insertData.checkTestExists(test_id):
                    pass
                else:
                    tk.messagebox.showwarning(title="Error", message="Test does not exist")

                # Score>max score check
                if insertData.isScoreValid(test_id,score):
                    pass
                else:
                    tk.messagebox.showwarning(title="Error", message="Invalid Score")

                # Insert data into the database
                insertData.insertStudentData(user_id, test_id, score)

                # Display a message indicating successful data entry
                messagebox.showinfo("Success", "Data has been successfully entered into the database.")

            else:
                tk.messagebox.showwarning(title="Error", message="All data is required")
        else:
            tk.messagebox.showwarning(title="Error", message="You have not accepted the terms")

    except mysql.connector.Error as e:
        # Handle any MySQL connection errors
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def main_student_data(window):
    frame = tk.Frame(window)
    frame.pack(side=tk.TOP)

    student_score_frame = tk.LabelFrame(frame, text="Student Score")
    student_score_frame.grid(row=0, column=0, padx=20, pady=10)

    user_id_label = tk.Label(student_score_frame, width=15, text="Student ID")
    user_id_label.grid(row=0, column=0, pady=5, padx=5)
    user_id_entry = tk.Spinbox(student_score_frame, from_=0, to="infinity")
    user_id_entry.grid(row=1, column=0, pady=5, padx=5)

    test_id_label = tk.Label(student_score_frame, text="Test ID")
    test_id_entry = tk.Spinbox(student_score_frame, from_=0, to="infinity")
    test_id_label.grid(row=0, column=2, pady=5, padx=5)
    test_id_entry.grid(row=1, column=2, pady=5, padx=5)

    score_label = tk.Label(student_score_frame, text="Score")
    score_label.grid(row=0, column=1, pady=5, padx=5)
    score_entry = tk.Spinbox(student_score_frame, from_=0, to="infinity")
    score_entry.grid(row=1, column=1, pady=5, padx=5)

    for widget in student_score_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # Accept terms
    terms_frame = tk.LabelFrame(frame, text="Verification")
    terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    accept_var = tk.StringVar(value="Not Accepted")
    terms_check = tk.Checkbutton(terms_frame, text="All data has been inputted correctly",
                                      variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0, pady=5, padx=5)

    # Button
    button = tk.Button(frame, text="Enter data", command=lambda: submit_score(user_id_entry,
                                                                              test_id_entry, score_entry, accept_var))
    button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Student Score Form")
    main_student_data(window)
    window.mainloop()
