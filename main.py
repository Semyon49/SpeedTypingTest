import time, threading, random
import tkinter as tk
from tkinter import ttk
import sv_ttk

is_start = False
text = open('texts.txt', 'r').read().split('\n')
timer = 0
cps = 0
cpm = 0

def start(newval):
    global is_start
    is_start = True
    entery_text.insert(0, newval)
    t = threading.Thread(target=timer_prorgamm) 
    t.start()

def timer_prorgamm():
    global is_start, timer, cps, cpm
    timer = 0
    if not is_start:
        timer = 0
        sample_lable.config(text=f"Speed: \nTimer: {timer:.2f} \nCPS: {cps:.2f} \nCPM: {cpm:.2f}")

    while is_start:
        
        color_text()
        if timer != 0: cps = len(entery_text.get()) / timer
        cpm = cps * 60
        sample_lable.config(text=f"Speed: \nTimer: {timer:.2f} \nCPS: {cps:.2f} \nCPM: {cpm:.2f}")
        time.sleep(0.1)
        timer += 0.1
        if entery_text.get() == (text_label.cget('text')):
            is_start = False
            entery_text.config(foreground='green')
            save_record()

def color_text():
    if entery_text.get() in (text_label.cget('text')):
        entery_text.config(foreground='white')
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
    global is_start, timer, cps, cpm
    is_start = False
    timer = 0
    cps = 0
    cpm = 0
    sample_lable.config(text=f"Speed: \nTimer: 0.00 \nCPS: {cps:.2f} \nCPM: {cpm:.2f}")
    entery_text.delete(0, tk.END)
    text_label.config(text=random.choice(text))
    entery_text.config(validate="key", validatecommand=check)

root = tk.Tk()
root.title('SpeedTypingTest')
root.geometry('800x450')

sv_ttk.set_theme("dark")

style = ttk.Style()
style.configure('.', font='MonoLisa 16', foreground='white')
style.configure('.', width = 45, borderwidth=3, focusthickness=3, anchor="center")

style.configure('wTLabel', width = 45, borderwidth=3, focusthickness=3, anchor="center")



check = (root.register(start),  "%P")

frame = tk.Frame(root)

text_label = ttk.Label(frame, text=random.choice(text), width=10)
text_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

entery_text = ttk.Entry(frame, validate="key", validatecommand=check, width=50)
entery_text.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

sample_lable = ttk.Label(frame, text=f'Speed: \nTimer: 0.00\nCPS: 0.00 \nCPM: 0.00')
sample_lable.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

Buttom_Start = ttk.Button(frame, text='Reset', command=reset, width=25)
Buttom_Start.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

t = (open('record.txt', 'r').read()).split('\n')
record_lable = ttk.Label(root, text=f'Record: \nTimer {float(t[0]):.2f} \nCPS: {float(t[1]):.2f} \nCPM: {float(t[2]):.2f}', anchor="nw")
record_lable.pack(anchor="nw")

frame.pack(anchor="n")
root.mainloop()