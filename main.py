from tkinter import *
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
from serial import Serial
import serial
import pandas as pd
import time
import datetime
import csv
from tkinter import Label, Entry

# Create the main window
root = customtkinter.CTk()
root.title("Contaminant Sensing")

# Set window dimensions to full screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width/2}x{screen_height/3}")
customtkinter.set_default_color_theme("green")

# Create the matplotlib figure and axis
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
line, = ax.plot([], [])
ax.set_title("Contaminant Sensing")
ax.set_xlabel("Current")
ax.set_ylabel("Voltage")
ax.grid()
canvas = FigureCanvasTkAgg(fig, master=root)

# global variables
x_data = []
y_data = []

animation_running = False
max_time = 60

# set up BT
outgoingPort = 'dev/tty.HC-05-DevB'
incomingPort = 'dev/tty.HC-05-DevB'
arduino = "filler"

# functions
def update_plot(i):
    if animation_running:
        if len(x_data) == max_time:
            stop_animation()
        x_data.append(len(x_data))
        y_data.append(np.random.random())
        line.set_color('blue')
        line.set_data(x_data, y_data)

        # Dynamically adjust the x and y axis limits based on data
        ax.relim()
        ax.autoscale_view(tight=True)


def start_animation():
    global animation_running
    animation_running = True
    ani.event_source.start()
    log_message("Experiment started")

def stop_animation():
    global animation_running
    animation_running = False
    log_message("Experiment stopped")

def set_max_time():
    global max_time
    max_time = int(max_time_entry.get())
    log_message(f"Max time set to {max_time} seconds")

def bt_Connect():
    print("ON Clicked")
    global arduino
    try:
        arduino = Serial(outgoingPort, 9600)
        print("Connected")
        log_message("Device Connected")
    except serial.SerialException:
        print("Exception occurred, likely already connected")
    else:
        arduino.write(b'x')
        income = arduino.readline()
        print(income.decode())
        log_message(income.decode())
    # arduino.close()

def bt_Disconnect():
    print("Disconnect")
    global arduino
    try:
        arduino.close()
    except serial.SerialException:
        print("Exception occurred")
        log_message("Serial Exception Occured")
    else:
        log_message("BT device disconnected")

def bt_ON():
    global arduino
    try:
        arduino.write(b'x')
        income = arduino.readline()
        print(income.decode())
        log_message("Device Connected")
        print("Message from arduino: " + income.decode())
    except serial.SerialException:
        # print("Exception occurred, likely no device connected")
        log_message("Exception occurred, likely no device connected")
    except AttributeError:
        # print("Exception occurred, likely no device connected")
        log_message("Exception occurred, likely no device connected")

def bt_OFF():
    global arduino
    try:
        arduino.write(b'b')
        income = arduino.readline()
        print("Message from arduino: " + income.decode())
    except serial.SerialException:
        print("Serial Exception Cccurred")
    except AttributeError:
        print("AttributeError occurred")

def bt_5v():
    global arduino
    try:
        arduino.write(b'y')
        income = arduino.readline()
        print("Message from arduino: " + income.decode())
        log_message("5v Pump Activated")

    except serial.SerialException:
        print("Exception occurred, likely no device connected")
        log_message("Serial Exception Occured")
    except AttributeError:
        print("Exception occurred, likely no device connected")
        log_message("Attribute Error Occured")

def bt_3_5v():
    global arduino
    try:
        arduino.write(b'a')
        income = arduino.readline()
        print("Message from arduino: " + income.decode())
        log_message("3.5v Pump Activated")

    except serial.SerialException:
        print("Exception occurred, likely no device connected")
        log_message("Serial Exception Occured")
    except AttributeError:
        print("Exception occurred, likely no device connected")
        log_message("Attribute Error Occured")

def bt_Disconnect():
    print("OFF Clicked")
    global arduino
    try:
        arduino.write(b'z')
        arduino.close()
    except serial.SerialException:
        print("Exception occurred, likely no device connected")
    except AttributeError:
        print("Exception occurred, likely no device connected")

def save():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"graph_{current_time}.png"
    plt.savefig(filename)
    log_message(f"Saved figure to {filename}")
    df = pd.DataFrame({'Current': x_data, 'Voltage': y_data})
    df.to_csv(f"data_{current_time}.csv", index=False)
    
def log_message(message):
    log_entry.config(state='normal')  # Enable editing of the box
    log_entry.insert(END, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '     ' + message + '\n\n')  # Add message to end
    log_entry.see(END)  # keep the bottom message visible
    log_entry.config(state='disabled')  # Disable editing box 

def reset():
    stop_animation()
    global x_data, y_data
    x_data = []
    y_data = []
    log_message("Experiment reset. Start a new experiment to clear the figure")

# Create the animation
ani = FuncAnimation(fig, update_plot, blit=False, interval=1000)

# Create and arrange the widgets using the grid manager
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, columnspan=5, padx=20, pady=20)

# Arrange buttons using the grid manager
start_button = customtkinter.CTkButton(root, text="Start Experiment", command=start_animation)
start_button.grid(row=2, column=0, padx=10, pady=20)

stop_button = customtkinter.CTkButton(root, text="Stop Experiment", command=stop_animation)
stop_button.grid(row=2, column=1, padx=10, pady=20)

reset_button = customtkinter.CTkButton(root, text="Reset", command=reset)
reset_button.grid(row=2, column=2, padx=10, pady=20)

bt_save = customtkinter.CTkButton(root, text="Save Figure and Data", command=save)
bt_save.grid(row=2, column=3, padx=10, pady=20)

# Add logging text box
log_entry = Text(root, height=8, width=90)  # Adjust height and width as needed
log_entry.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
log_entry.config(state='disabled')  # Make the text widget read-only

bt_buttonConn = customtkinter.CTkButton(root, text="BT Connect", command=bt_Connect, width=10)
bt_buttonConn.grid(row=0, column=0, padx=10, pady=10)

bt_buttonOFF = customtkinter.CTkButton(root, text="BT Disconnect", command=bt_Disconnect, width=10)
bt_buttonOFF.grid(row=0, column=4, padx=10, pady=10)

# Create labels and entry fields for min and max sweep values
min_label = Label(root, text="Min Sweep Value:")
min_label.grid(row=4, column=0, padx=10, pady=10)

min_entry = Entry(root, width=10)  # Adjust the width as needed
min_entry.grid(row=5, column=0, padx=5, pady=10)

max_label = Label(root, text="Max Sweep Value:")
max_label.grid(row=4, column=1, padx=10, pady=10)

max_entry = Entry(root, width=10)  # Adjust the width as needed
max_entry.grid(row=5, column=1, padx=5, pady=10)


# Start the tkinter main loop
root.mainloop()
