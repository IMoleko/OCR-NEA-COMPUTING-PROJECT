import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

class MessageBoardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message Board")
        self.create_widgets()

    def create_widgets(self):
        # Create a scrolled text widget to display messages
        self.message_board = ScrolledText(self.root, width=60, height=20)
        self.message_board.pack(padx=10, pady=10)

        # Create an entry widget for users to input mess    ages
        self.message_entry = tk.Entry(self.root, width=60)
        self.message_entry.pack(padx=10, pady=(0, 10))

        # Create a button to send messages
        send_button = tk.Button(self.root, text="Send", command=self.send_message)
        send_button.pack(padx=10, pady=(0, 10))

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.message_board.insert(tk.END, f"{timestamp} - You: {message}\n")
            self.message_board.see(tk.END)  # Scroll to the end of the message board
            self.message_entry.delete(0, tk.END)  # Clear the message entry
        else:
            messagebox.showwarning("Warning", "Please enter a message.")

def main():
    root = tk.Tk()
    app = MessageBoardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
