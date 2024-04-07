import time, threading, random
import tkinter as tk
from tkinter import ttk

is_start = False
timer = 0
cps = 0
cpm = 0
text = open('texts.txt', 'r').read().split('\n')

def start(newval):
    global is_start
    is_start = True
    entery_text.insert(0, newval)
    t = threading.Thread(target=timer_prorgamm) 
    t.start()

def timer_prorgamm():
    global is_start, timer, cps, cpm
    while is_start:
        time.sleep(0.1)
        timer += 0.1
        color_text()
        cps = len(entery_text.get()) / timer
        cpm = cps * 60
        sample_lable.config(text=f"Speed: \nTimer {timer:.2f} \nCPS: {cps:.2f} \nCPM: {cpm:.2f}")
        if entery_text.get() == (text_label.cget('text')):
            is_start = False
            entery_text.config(foreground='green')
            save_record()


def color_text():
    if entery_text.get() in (text_label.cget('text')):
        entery_text.config(foreground='black')
    else:
        entery_text.config(foreground='red')

def save_record():
    old = (open('record.txt', 'r').read()).split('\n')
    if float(old[0]) > timer and float(old[0]) != 0:
        with open('record.txt', 'w') as f:
            f.write(str(timer) + '\n')
            f.write(str(cps) + '\n')
            f.write(str(cpm) + '\n')

def reset():
    sample_lable.config(text=f'Speed: \nTimer: 0.00\nCPS: 0.00 \nCPM: 0.00')
    entery_text.delete(0, tk.END)
    text_label.config(text=random.choice(text))
    entery_text.config(validate="key", validatecommand=check)

root = tk.Tk()
root.title('SpeedTypingTest')
root.geometry('1000x650')

check = (root.register(start),  "%P")

frame = tk.Frame(root)

text_label = ttk.Label(frame, text=random.choice(text))
text_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

entery_text = ttk.Entry(frame, validate="key", validatecommand=check)
entery_text.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

sample_lable = ttk.Label(frame, text=f'Speed: \nTimer: 0.00\nCPS: 0.00 \nCPM: 0.00')
sample_lable.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

Buttom_Start = ttk.Button(frame, text='Reset', command=reset)
Buttom_Start.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

t = (open('record.txt', 'r').read()).split('\n')
record_lable = ttk.Label(frame, text=f'Record: \nTimer {float(t[0]):.2f} \nCPS: {float(t[1]):.2f} \nCPM: {float(t[2]):.2f}')
record_lable.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

frame.pack()
root.mainloop()