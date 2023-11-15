import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np

from serial import Serial
import serial

import time

# Create the main window
root = tk.Tk()
root.title("Contaminant Sensing")

# Set window dimensions to full screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.config(bg="#1a8bab")

# Create a matplotlib figure and axis
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
line, = ax.plot([], [])
ax.set_title("Contaminant Sensing")
ax.set_xlabel("Time")
ax.set_ylabel("Concentration")
ax.grid()
canvas = FigureCanvasTkAgg(fig, master=root)

# Create and arrange the widgets using the grid manager
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

x_data = []
y_data = []

animation_running = False
max_time = 60

# set up BT
outgoingPort = "COM6"
incomingPort = "COM7"
# make bluetooth global
bluetooth = "filler"
dummyText = "Empty"
dummyCount = 0

def update_plot(i):
    if animation_running:
        if len(x_data) == max_time:
            stop_animation()
        x_data.append(len(x_data))
        y_data.append(np.random.random())
        line.set_data(x_data, y_data)

        # Dynamically adjust the x and y axis limits based on data
        ax.relim()
        ax.autoscale_view(tight=True)


def start_animation():
    global animation_running
    animation_running = True
    ani.event_source.start()


def stop_animation():
    global animation_running
    animation_running = False


def set_max_time():
    global max_time
    max_time = int(max_time_entry.get())


def bt_Connect():
    print("ON Clicked")

    global bluetooth
    try:
        bluetooth = Serial(outgoingPort, 9600)
        print("Connected")

    except serial.SerialException:
        print("Exception occurred, likely already connected")

    else:
        print("writing to bluetooth")
        bluetooth.write(b'x')
        print("reading from bluetooth")
        income = bluetooth.readline()
        print("Message from bluetooth: " + income.decode())


    # bluetooth.close()

def bt_ON():
    global bluetooth
    try:
        bluetooth.write(b'x')
        income = bluetooth.readline()
        print("Message from bluetooth: " + income.decode())

    except serial.SerialException:
        print("Exception occurred, likely no device connected")
    except AttributeError:
        print("Exception occurred, likely no device connected")

    dummy_label.config(text="updated")

def bt_OFF():
    global bluetooth
    try:
        bluetooth.write(b'b')
        income = bluetooth.readline()
        print("Message from bluetooth: " + income.decode())

    except serial.SerialException:
        print("Exception occurred, likely no device connected")
    except AttributeError:
        print("Exception occurred, likely no device connected")
def bt_5v():
    global bluetooth
    try:
        bluetooth.write(b'y')
        income = bluetooth.readline()
        print("Message from bluetooth: " + income.decode())

    except serial.SerialException:
        print("Exception occurred, likely no device connected")
    except AttributeError:
        print("Exception occurred, likely no device connected")

def bt_3_5v():
    global bluetooth
    try:
        bluetooth.write(b'a')
        income = bluetooth.readline()
        print("Message from bluetooth: " + income.decode())

    except serial.SerialException:
        print("Exception occurred, likely no device connected")
    except AttributeError:
        print("Exception occurred, likely no device connected")

def bt_Disconnect():
    print("OFF Clicked")
    global bluetooth
    try:
        bluetooth.write(b'z')
        bluetooth.close()
    except serial.SerialException:
        print("Exception occurred, likely no device connected")
    except AttributeError:
        print("Exception occurred, likely no device connected")


# Create the animation
ani = FuncAnimation(fig, update_plot, blit=False, interval=1000)

# Arrange buttons using the grid manager
start_button = Button(root, text="Start Experiment", command=start_animation)
start_button.grid(row=1, column=0)
stop_button = Button(root, text="Stop Experiment", command=stop_animation)
stop_button.grid(row=1, column=1)

bt_buttonConn = Button(root, text="BT Connect", command=bt_Connect)
bt_buttonConn.grid(row=3, column=0)

bt_buttonOFF = Button(root, text="BT Disconnect", command=bt_Disconnect)
bt_buttonOFF.grid(row=3, column=1)

bt_buttonON = Button(root, text="BT ON", command=bt_ON)
bt_buttonON.grid(row=4, column=0)

bt_buttonOFF = Button(root, text="BT OFF", command=bt_OFF)
bt_buttonOFF.grid(row=4, column=1)

bt_buttonPump5v = Button(root, text="5v", command=bt_5v)
bt_buttonPump5v.grid(row=8, column=1)

bt_buttonPump3_5v = Button(root, text="3.5v", command=bt_3_5v)
bt_buttonPump3_5v.grid(row=8, column=0)

# Add text box for configuring maximum time
max_time_label = Label(root, text="Max Time:")
max_time_label.grid(row=5, column=0, padx=10, pady=10)
max_time_entry = Entry(root, textvariable=max_time)
max_time_entry.grid(row=5, column=1, padx=10, pady=10)
max_time_button = Button(root, text="Set Max Time", command=set_max_time)
max_time_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

dummy_label = Label(root, text=dummyText)
dummy_label.grid(row=7, column=0, padx=10, pady=10)
# Start the tkinter main loop
root.mainloop()
