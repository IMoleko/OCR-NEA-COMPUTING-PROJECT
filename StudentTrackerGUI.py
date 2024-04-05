from tkinter import *
from tkinter import messagebox

from Validate import IsValid
import hashlib
from teach_main_2 import *
import mysql.connector
from main_page import *
def hash_password(password):
    # Hash the password using a secure hash function (e.g., SHA-256)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password
def authenticate_user(email, password):
    try:
        # Connect to the database
        cnx = mysql.connector.connect(
        user='thapelomoleko',
        password='Thapeloivan2006*',
        host='db4free.net',
        database='tracker'
    )

        cursor = cnx.cursor(dictionary=True)

        # Hash the provided password for comparison with the stored hashed password
        hashed_password = hash_password(password)

        # Execute a SELECT query to check if the user exists
        query = "SELECT * FROM Users WHERE email = %s AND hashed_password = %s"
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()

        # If the result is not None, authentication is successful
        return result is not None

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        # Close the cursor and the connection
        cursor.close()
        cnx.close()

def back(wx):
    wx.destroy()  # destroys    any window passed into this function  # opens main again
def return_start(wx):
    wx.destroy()
    start_page()
def start_page():
    win_start = Tk()
    win_start.title("StudentTracker")
    win_start.geometry("500x310")
    win_start.resizable(0, 0)  # Don't allow resizing in the x or y direction
    frame_start = Frame()
    frame_start.pack()

    lbl_title = Label(frame_start, text="Student Tracker",font=("Arial",40,"bold"))
    #lbl_title.grid(column=1,row=0,columnspan=3,rowspan=2,padx=10,pady=10)
    lbl_title.pack(expand=True)

    studentlog_btn = Button(frame_start,text="Student login",width=15,height=4,command=lambda :student_login(win_start))
    #studentlog_btn.grid(column=1,row=1,columnspan=3,rowspan=2,padx=1,pady=1)
    studentlog_btn.pack(side=LEFT)

    teacherlog_btn = Button(frame_start, text="Teacher login", width=15,height=4,command=lambda: teacher_login(win_start))
   # teacherlog_btn.grid(column=2,row=1,columnspan=3,rowspan=2,padx=1,pady=1)
    teacherlog_btn.pack(side=RIGHT)

    exit_btn = Button(frame_start,text="Exit",width=15,height=4,command=lambda: quit)
   # exit_btn.grid(column=0,row=2,columnspan=3,rowspan=2)
    exit_btn.pack(side=BOTTOM)

    # contact_btn = Button(frame_start,text=con)
    mainloop()
def student_login(x):
   def on_login_button_click():
        entered_email = entry_email.get()
        entered_password = entry_pass.get()

        validate = IsValid()
        if validate.Email(entered_email):
            pass
        else:
            messagebox.showerror("Login Failed", "Invalid Email")
            return False
        # Call the authenticate_user function
        if authenticate_user(entered_email, entered_password):
            messagebox.showinfo("Login Successful", "Student login successful!")
            create_window(entered_email,win_studentlog)

        else:
            messagebox.showerror("Login Failed", "Password incorrect!")
   back(x)
   win_studentlog = Tk()
   win_studentlog.title("Student Login")
   win_studentlog.geometry("325x265")
   win_studentlog.resizable(0, 0)
   frame_student = Frame(win_studentlog)
   frame_student.pack()

   return_btn = Button(frame_student, text="Return", command=lambda: return_start(win_studentlog))
   return_btn.grid()

   lbl_title = Label(frame_student, text="Student Login", font=("Arial", 22))
   lbl_title.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

   lbl_email = Label(frame_student, text="Email: ")
   lbl_email.grid(row=1, column=0, pady=10, padx=10)

   entry_email = Entry(frame_student)
   entry_email.grid(row=1, column=1)

   lbl_pass = Label(frame_student, text="Password: ")
   lbl_pass.grid(row=2, column=0, pady=10, padx=10)

   entry_pass = Entry(frame_student, show="*")
   entry_pass.grid(row=2, column=1)

    # Modify the command attribute to call on_login_button_click
   btn_login = Button(frame_student, text="Login", width=10, command= on_login_button_click)
   btn_login.grid(row=3, column=1, padx=80, pady=30)

   mainloop()
def teacher_login(x):
    def on_login_button_click():
        entered_email = entry_email.get()
        entered_password = txt_pass.get()

        validate = IsValid()
        if validate.Email(entered_email):
            pass
        else:
            messagebox.showerror("Login Failed", "Invalid Email")
            return False
        # Call the authenticate_user function
        if authenticate_user(entered_email, entered_password):
            messagebox.showinfo("Login Successful", "Teacher login successful!")
            main_teach(win_teacherlog,1)
        else:
            messagebox.showerror("Login Failed", "Password incorrect!")

    back(x)
    win_teacherlog = Tk()
    win_teacherlog.title("Teacher Login")
    win_teacherlog.geometry("325x265")
    win_teacherlog.resizable(0, 0)
    frame_teacher = Frame()
    frame_teacher.pack()

    btn_return = Button(frame_teacher, text="Return", command=lambda: return_start(win_teacherlog))
    btn_return.grid()

    lbl_title = Label(frame_teacher, text="Teacher Login", font=("Arial", 22))
    lbl_title.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

    lbl_email = Label(frame_teacher, text="Email: ")
    lbl_email.grid(row=1, column=0, pady=10, padx=10)

    entry_email = Entry(frame_teacher)
    entry_email.grid(row=1, column=1)

    lbl_pass = Label(frame_teacher, text="Password: ")
    lbl_pass.grid(row=2, column=0, pady=10, padx=10)

    txt_pass = Entry(frame_teacher, show="*")
    txt_pass.grid(row=2, column=1)

    # Modify the command attribute to call on_login_button_click
    btn_login = Button(frame_teacher, text="Login", width=10, command= on_login_button_click)
    btn_login.grid(row=3, column=1, padx=80, pady=30)

    mainloop()

if __name__ == "__main__":
    start_page()