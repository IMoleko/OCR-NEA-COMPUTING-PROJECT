import tkinter as tk
from tkinter import ttk, Menu, messagebox
import mysql.connector
from Data_Extration import DataExtractor
import hashlib

def logout():
    # Implement logout functionality here
    pass

def display_table_gui(cursor, parent_frame, table_name, column_widths=None):
    try:
        # Create a frame to hold the treeview widget
        table_frame = tk.Frame(parent_frame)
        table_frame.pack(pady=10, padx=10)

        # Create a treeview widget to display the data
        tree = ttk.Treeview(table_frame)
        tree["columns"] = [desc[0] for desc in cursor.description]

        # Execute a SQL query to select all data from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        table_data = cursor.fetchall()

        # Define column headings
        for col in tree["columns"]:
            tree.heading(col, text=col)

        # Insert data into the treeview
        for i, row in enumerate(table_data, start=1):
            tree.insert("", "end", text=str(i), values=row)

        # Set column widths if provided
        if column_widths:
            for i, width in enumerate(column_widths):
                tree.column(tree["columns"][i], width=width)

        # Pack the treeview widget
        tree.pack(expand=True, fill="both")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def update_frames(connection, user_id, title_frame, top_frame, bottom_frame):
    # Clear existing frames
    for widget in title_frame.winfo_children():
        widget.destroy()

    # Implement frame update logic here
    pass

def main_class(connection, user_id, title_frame, top_frame, bottom_frame, window):
    # Create DataExtractor object
    with DataExtractor(connection, user_id) as data_extractor:
        # Display student name
        user_name = data_extractor.get_user_name()
        title_label = tk.Label(title_frame, text=f"Student Name: {user_name}", font=("Helvetica", 16))
        title_label.grid(row=1, column=2)

        def show_button_pressed(show_entry):
            try:
                # Implement show button logic here
                pass

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

        # Display student name
        user_name = data_extractor.get_user_name()
        title_label = tk.Label(title_frame, text=f"Student Name: {user_name}", font=("Helvetica", 16))
        title_label.grid(row=1, column=2)

        # Show id
        show_label = tk.Label(title_frame, text="Show ID")
        show_entry = tk.Entry(title_frame)
        show_entry.grid(row=1, column=3)
        show_button = tk.Button(title_frame, text="Show", command=lambda: show_button_pressed(show_entry))
        show_button.grid(row=1, column=4)

        # Add logout button
        logout_button = tk.Button(title_frame, text="Logout", command=logout)
        logout_button.grid(row=1, column=5)

        # Implement other UI elements and logic here

        # Close the database connection
        connection.close()

def main():
    try:
        # Connect to the database
        db_connection = mysql.connector.connect(
            user='thapelomoleko',
            password='your_password',
            host='localhost',
            database='tracker'
        )

        # Create the main window
        win_tmain = tk.Tk()
        win_tmain.title("StudentTracker")
        win_tmain.geometry("1438x865")
        win_tmain.resizable(0, 0)

        # Create a menubar
        menubar = tk.Menu(win_tmain)
        win_tmain.config(menu=menubar)

        # Create a menu
        teach_menu = tk.Menu(menubar)

        # Add a menu item to the menu
        teach_menu.add_command(label='Log Out', command=lambda: logout())  # Sign out to main

        # Add the File menu to the menubar
        menubar.add_cascade(label="Settings", menu=teach_menu)

        # Create a notebook widget
        note_tmain = ttk.Notebook(win_tmain)
        note_tmain.pack(expand=1, fill=tk.BOTH)

        # Create tabs
        tab_main = tk.Frame()
        tab_input_data = tk.Frame()
        tab_show_data = tk.Frame()
        tab_accounts = tk.Frame()

        # Add tabs to the notebook
        note_tmain.add(tab_main, text="Class Data")
        note_tmain.add(tab_input_data, text="Input Data")
        note_tmain.add(tab_show_data, text="Show Data")
        note_tmain.add(tab_accounts, text="Account Settings")

        # Call main_class for tab_main
        main_class(db_connection, user_id, title_frame_1, top_frame_1, bottom_frame_1, win_tmain)

        # Display the GUI
        win_tmain.mainloop()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        # Handle the database error

if __name__ == "__main__":
    main()
