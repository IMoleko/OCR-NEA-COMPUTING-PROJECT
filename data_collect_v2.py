import mysql.connector
import tkinter as tk
import hashlib
from tkinter import ttk

class Data:
    def __init__(self):
        self.conn = mysql.connector.connect(user='thapelomoleko', password='Thapeloivan2006*',
                                      host='db4free.net',
                                      database='tracker')
        self.cursor = self.conn.cursor()

    def createTables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY
                    name VARCHAR(225),
                    title VARCHAR(225),
                    date_of_birth DATE,
                    email VARCHAR(225),
                    phone_number VARCHAR(225), 
                    status ENUM('Student', 'Teacher'),
                    hashed_password VARCHAR(100)
                    );''')
            self.conn.commit()
            print("Users Table is created successfully")

            self.cursor.execute('''CREATE TABLE Tests (
                    test_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    date DATE,
                    time TIME,
                    max_score INT
                    );''')
            self.conn.commit()
            print("Tests Table is created successfully")

            self.cursor.execute('''CREATE TABLE StudentTestRelationship (
                    user_id INT,
                    test_id    INT,
                    student_score int,
                    PRIMARY KEY (user_id, test_id),
                    FOREIGN KEY (user_id) REFERENCES Users (user_id),
                    FOREIGN KEY (test_id) REFERENCES Tests (test_id)
                    );''')
            self.conn.commit()
            print("Student Test table is created successfully")

            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def insertUserData(self, givenName, givenTitle, givenDob, givenEmail, givenNum, givenStatus):
        try:
            # Hash the default password "Password1" using SHA-256
            password = hashlib.sha256("Password1".encode()).hexdigest()
            # Execute the SQL query to insert user data into the database
            self.cursor.execute('''INSERT INTO Users  
                (name, title, date_of_birth, email, phone_number, status, hashed_password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                (givenName, givenTitle, givenDob, givenEmail, givenNum, givenStatus, password))
            # Commit the transaction
            self.conn.commit()
            print("Data inserted successfully")
            return True
        except mysql.connector.Error as err:
            # Print error message if an error occurs during insertion
            print(f"Error: {err}")
            return False

    def insertTestData(self,givenName, givenDesc, givenDate, givenTime, givenScore):
        try:
            self.cursor.execute('''INSERT INTO Tests  
                (name, description, date, time, max_score) 
                VALUES (%s, %s, %s, %s, %s)''',
                                (givenName, givenDesc, givenDate, givenTime, givenScore))
            self.conn.commit()
            print("Data inserted Seccuessfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def checkUserIdExists(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchone()
            return True if result else False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def checkTestExists(self, test_id):
        try:
            self.cursor.execute("SELECT * FROM Tests WHERE test_id = %s", (test_id,))
            result = self.cursor.fetchone()
            return True if result else False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def isScoreValid(self, test_id, score):
        try:
            if score <0:
                return False
            self.cursor.execute("SELECT max_score FROM Tests WHERE test_id = %s", (test_id,))
            max_score = self.cursor.fetchone()[0]
            return int(score) <= max_score
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def insertStudentData(self, user_id, test_id, score):
        try:
            self.cursor.execute('''INSERT INTO StudentTestRelationship  
                (user_id, test_id, score) 
                VALUES (%s, %s, %s)''',
                                (user_id, test_id, score))
            self.conn.commit()
            print("Student data inserted Successfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error inserting student data: {err}")
            return False

    def displayUsersTableGUI(self, frame):
        try:
            table_frame = tk.Frame(frame)
            table_frame.pack(pady=10, padx=10, fill=tk.X, expand=True)
            # Execute a SQL query to select all data from the Users table
            self.cursor.execute("SELECT * FROM Users")
            users_data = self.cursor.fetchall()

            # Create a treeview widget to display the data
            tree = ttk.Treeview(table_frame)
            tree["columns"] = ("User ID", "Name", "Title", "DoB", "Email", "Phone No", "Status")

            # Define column headings
            tree.heading("#0", text="Index")
            for col in tree["columns"]:
                tree.heading(col, text=col)

            # Set column widths
            column_widths = (80, 150, 100, 100, 200, 120, 80)  # Define the desired widths for each column
            for i, width in enumerate(column_widths):
                tree.column(tree["columns"][i], width=width)

            # Insert data into the treeview
            for i, user in enumerate(users_data, start=1):
                tree.insert("", "end", text=str(i), values=user)

            # Pack the treeview widget
            tree.pack(side=tk.TOP)
            # tree.pack(expand=True, fill="both")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def displayTestsTableGUI(self, frame):
        try:
            # Execute a SQL query to select all data from the Tests table
            self.cursor.execute("SELECT * FROM Tests")
            tests_data = self.cursor.fetchall()

            # Create a treeview widget to display the data
            tree = ttk.Treeview(frame)
            tree["columns"] = ("Test ID", "Name", "Description", "Date", "Time", "Max Score")

            # Define column headings
            tree.heading("#0", text="Index")
            for col in tree["columns"]:
                tree.heading(col, text=col)

            # Set column widths
            column_widths = (80, 150, 200, 100, 80, 100)  # Define the desired widths for each column
            for i, width in enumerate(column_widths):
                tree.column(tree["columns"][i], width=width)

            # Insert data into the treeview
            for i, test in enumerate(tests_data, start=1):
                tree.insert("", "end", text=str(i), values=test)

            # Pack the treeview widget
            tree.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def display_table_gui(self, parent_frame, table_name, column_widths=None):
        try:
            # Create a frame to hold the treeview widget
            table_frame = tk.Frame(parent_frame)
            table_frame.pack(pady=10, padx=10)

            # Execute a SQL query to select all data from the specified table
            self.cursor.execute(f"SELECT * FROM {table_name}")
            table_data = self.cursor.fetchall()

            # Create a treeview widget to display the data
            tree = ttk.Treeview(table_frame)
            tree["columns"] = [desc[0] for desc in self.cursor.description]

            # Define column headings
            for col in tree["columns"]:
                tree.heading(col, text=col)

            # Set column widths if provided
            if column_widths:
                for i, width in enumerate(column_widths):
                    tree.column(tree["columns"][i], width=width)

            # Insert data into the treeview
            for i, row in enumerate(table_data, start=1):
                tree.insert("", "end", text=str(i), values=row)

            # Pack the treeview widget
            tree.pack(expand=True, fill="both")

            print("Table complete")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetchAllUserData(self):
        try:
            # Execute a SQL query to select all data from the Users table
            self.cursor.execute("SELECT * FROM Users")
            users_data = self.cursor.fetchall()

            return users_data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def fetchAllTestData(self):
        try:
            # Execute a SQL query to select all data from the Users table
            self.cursor.execute("SELECT * FROM Tests")
            tests_data = self.cursor.fetchall()

            return tests_data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def changePassword(self, user_id, new_password):
        try:
            # Hash the new password using SHA-256
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

            # Update the password in the database
            self.cursor.execute('''UPDATE Users
                                   SET hashed_password = %s
                                   WHERE user_id = %s''',
                                (hashed_password, user_id))
            self.conn.commit()
            print("Password changed successfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def deleteRecord(self, id, table):
        try:
            match table:
                case "Users":
                    table_column = "user_id"
                case "Tests":
                    table_column = "test_id"
                case _:
                    print("Invalid table name")
                    return False

            # Execute the SQL DELETE statement to remove the record
            query = f"DELETE FROM {table} WHERE {table_column} = %s"
            self.cursor.execute(query, (id,))
            self.conn.commit()
            print("Record deleted successfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def updateEmail(self, user_id, new_email):
        try:
            # Execute the SQL UPDATE statement to modify the email address
            self.cursor.execute('''UPDATE Users
                                   SET email = %s
                                   WHERE user_id = %s''',
                                (new_email, user_id))
            self.conn.commit()
            print("Email updated successfully")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False


    def close_connection(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    root = tk.Tk()
    data = Data()
    # data.displayUsersTableGUI(root)
    data.displayTestsTableGUI(root)
    root.mainloop()