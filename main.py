# Importing necessary libraries
import time, threading, random
import tkinter as tk
from tkinter import ttk
import sv_ttk  # Importing a custom module, assuming it's for customizing ttk themes

# Global variables initialization
is_start = False
text = open('texts.txt', 'r').read().split('\n')
timer = 0
cps = 0
cpm = 0

# Function to start the timer and begin the typing test
def start(newval):
    global is_start
    is_start = True
    entery_text.insert(0, newval)  # Inserting the new value into the entry widget
    t = threading.Thread(target=timer_program)  # Starting a new thread for the timer
    t.start()

# Function to handle the timer functionality during the typing test
def timer_program():
    global is_start, timer, cps, cpm
    timer = 0  # Resetting timer
    if not is_start:
        timer = 0
        sample_label.config(text=f"Speed: \nTimer: {timer:.2f} \nCPS: {cps:.2f} \nCPM: {cpm:.2f}")

    while is_start:
        color_text()  # Calling function to handle text color
        if timer != 0: cps = len(entery_text.get()) / timer  # Calculating characters per second
        cpm = cps * 60  # Calculating characters per minute
        sample_label.config(text=f"Speed: \nTimer: {timer:.2f} \nCPS: {cps:.2f} \nCPM: {cpm:.2f}")
        time.sleep(0.1)  # Pausing for 0.1 seconds
        timer += 0.1  # Incrementing timer
        if entery_text.get() == (text_label.cget('text')):
            is_start = False
            entery_text.config(foreground='green')
            save_record()

# Function to color the entered text based on correctness
def color_text():
    if entery_text.get() in (text_label.cget('text')):
        entery_text.config(foreground='white')
    else:
        entery_text.config(foreground='red')

# Function to save the typing test record
def save_record():
    old = (open('record.txt', 'r').read()).split('\n')
    if float(old[0]) > timer and float(old[0]) != 0:
        with open('record.txt', 'w') as f:
            f.write(str(timer) + '\n')
            f.write(str(cps) + '\n')
            f.write(str(cpm) + '\n')

# Function to reset the typing test
def reset():
    global is_start, timer, cps, cpm
    is_start = False
    timer = 0
    cps = 0
    cpm = 0
    sample_label.config(text=f"Speed: \nTimer: 0.00 \nCPS: {cps:.2f} \nCPM: {cpm:.2f}")
    entery_text.delete(0, tk.END)
    text_label.config(text=random.choice(text))
    entery_text.config(validate="key", validatecommand=check)

# Creating the main window
root = tk.Tk()
root.title('SpeedTypingTest')
root.geometry('800x450')

sv_ttk.set_theme("dark")  # Setting a custom theme for ttk widgets

style = ttk.Style()  # Creating a ttk style object
style.configure('.', font='MonoLisa 16', foreground='white')  # Configuring style for all widgets
style.configure('.', width=45, borderwidth=3, focusthickness=3, anchor="center")  # Further style configurations

style.configure('wTLabel', width=45, borderwidth=3, focusthickness=3, anchor="center")  # Configuring style for specific label

# Registering a validation function for entry widget
check = (root.register(start), "%P")

frame = tk.Frame(root)

# Creating and placing widgets inside the frame
text_label = ttk.Label(frame, text=random.choice(text), width=10)
text_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

entery_text = ttk.Entry(frame, validate="key", validatecommand=check, width=50)
entery_text.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

sample_label = ttk.Label(frame, text=f'Speed: \nTimer: 0.00\nCPS: 0.00 \nCPM: 0.00')
sample_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

button_start = ttk.Button(frame, text='Reset', command=reset, width=25)
button_start.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Displaying record
t = (open('record.txt', 'r').read()).split('\n')
record_label = ttk.Label(root, text=f'Record: \nTimer {float(t[0]):.2f} \nCPS: {float(t[1]):.2f} \nCPM: {float(t[2]):.2f}', anchor="nw")
record_label.pack(anchor="nw")

frame.pack(anchor="n")
root.mainloop()  # Starting the main event loop
