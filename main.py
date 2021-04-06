# Password Generator Project

from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    email = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure that you haven't left any fields empty")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n Email: {email} \n"
                                                              f"Password: {password}\n Is it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as file_data:
                    # reading old data
                    data = json.load(file_data)
            except FileNotFoundError:
                with open("data.json", "w") as file_data:
                    json.dump(new_data, file_data, indent=4)
            else:
                # updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as file_data:
                    # saving updated data
                    json.dump(data, file_data, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_input.get()
    try:
        with open("data.json") as file_data:
            # reading old data
            data = json.load(file_data)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Sorry, No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"Sorry, No details for the {website} Found")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website: ")
website_label.grid(row=1, column=0)

website_input = Entry(width=33)
website_input.grid(row=1, column=1)
website_input.focus()

search_button = Button(width=15, text="Search", command=find_password)
search_button.grid(row=1, column=2)

username_label = Label(text="Email/Username: ")
username_label.grid(row=2, column=0)

username_input = Entry(width=52)
username_input.grid(row=2, column=1, columnspan=2)
username_input.insert(0, "Shruthi@gmail.com")

password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)

password_input = Entry(width=33)
password_input.grid(row=3, column=1)

generate_password_button = Button(width=15, text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(width=44, text="Add", command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
