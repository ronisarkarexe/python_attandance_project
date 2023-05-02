from datetime import date

import mysql.connector
from tkinter import *

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attendance"
)

root = Tk()
root.geometry("400x400")
root.title("Radio Buttons for User Selection")

# Create a dictionary of options and associated user lists
options = {
    "Division A": ["Roni Sarkar", "Ankur Datta", "Angad Kumar", "Pradip Tharu", "Roki Sarkar", "Sujon Sarkar"],
    "Division B": ["Harandra", "Boni Sarkar", "Robin Sarkar", "Hori Das", "Radha Mohan", "Pradip Tharu", "Roki Sarkar", "Sujon Sarkar"],
    "Division C": ["Puja Das", "Pradip Tharu", "Roki Sarkar", "Sujon Sarkar", "Pradip Tharu", "Roki Sarkar", "Sujon Sarkar", "Pradip Tharu", "Roki Sarkar", "Sujon Sarkar"],
}

# Create a StringVar to store the selected option
selected_option = StringVar()

# Set the initial selected option
selected_option.set("Division A")

# Create the dropdown menu
option_menu = OptionMenu(root, selected_option, *options.keys())
option_menu.pack(pady=20)


# Create a function to handle the selection of an option
def handle_option_selection(selection):
    user_list = options[selection]
    user_frame.config(text="")

    # Clear previously displayed user frames
    for widget in user_frame.winfo_children():
        widget.destroy()

    for user in user_list:
        user_frame_inner = Frame(user_frame)
        user_frame_inner.pack(fill=X)
        user_label = Label(user_frame_inner, text=user, width=20, anchor=W, background="#fff", font=("Arial", 12), borderwidth=2, relief="solid")
        user_label.pack(side=LEFT)
        user_var = StringVar()
        user_var.set("Division A")
        user_option_1 = Radiobutton(user_frame_inner, text="Present", variable=user_var, value="Present")
        user_option_1.pack(side=LEFT, padx=10)
        user_option_2 = Radiobutton(user_frame_inner, text="Absent", variable=user_var, value="Absent")
        user_option_2.pack(side=LEFT)
        user_var.trace_add("write", lambda *args, user=user, var=user_var: handle_user_option(user, var.get()))


# Create a function to handle the selection of an option for a specific user
def handle_user_option(user, option):
    print(f"{user}: {option}")


# Add a frame to display the user list
user_frame = LabelFrame(root, text="Users")
user_frame.pack(pady=10)

# Add a button to update the user list
update_button = Button(root, text="Show User List", bg="blue", fg="white", font=("Arial", 13), padx=10, pady=2, bd=1, command=lambda: handle_option_selection(selected_option.get()))
update_button.pack()

# Add a submit button to update the database
submit_button = Button(root, text="Submit", bg="blue", fg="white", font=("Arial", 13), padx=10, pady=2, bd=1, command=lambda: insert_into_database(selected_option.get()))
submit_button.pack(pady=20)


# Function to insert users into the database
def insert_into_database(option):
    cursor = db.cursor()
    today = date.today()
    for user_list in options.values():
        for user in user_list:
            cursor.execute("INSERT INTO u (name, option, date) VALUES (%s, %s, %s)", (user, option, today))
    db.commit()
    cursor.close()
    submit_button.config(text="Submitted", state=DISABLED)
    update_button.config(state=DISABLED)


root.mainloop()
