from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import serial
import string
import csv
from datetime import datetime, time


#global var
sample_no = 0
width = 1024
height = 720
target_wavelength_data = np.array([]) 
target_sensor = 4
time_stamp = np.array([])
current_data = np.zeros(288,)
 
csv_file = f"test{sample_no}.csv"
time_getData = datetime.now()

#state
state_run = False

#pre-compute wavelengths values according to formula
wavelength = np.array(range(1,289))
wavelength = 3.068464691e2 + 2.707179585 * wavelength -1.45040638e-3 * wavelength**2 -4.596809405e-6 * wavelength**3 - 3.105844784e-9 * wavelength**4 + 2.269126371e-11 * wavelength**5
wavelength = np.round(wavelength, decimals=2)

#initalize Serial communcation
arduinoData = serial.Serial("com6",115200)
start_time = datetime.now()

#GUI setup
root = Tk()
root.geometry(f"{width}x{height}")

#plotting the graph 
fig = Figure(figsize = (10,5), dpi = 100)
canvas = FigureCanvasTkAgg(fig, master = root) #declare a canvas object
canvas.get_tk_widget().pack(fill='x') #place the canvas in root
canvas.draw()



def reset_array(a : tuple):
    x = ((np.array([])),) * len(a)
    return x

def get_data(income_data : bytes) -> tuple[int,int]:
    packet = income_data
    packet = str(packet,"utf-8")
    packet = packet.strip()
    packet = packet.split(',')
    sensor_number = int(packet[0])
    sensor_reading = int(packet[1])
    return sensor_number, sensor_reading

def loop():
    global time_stamp, current_data, target_wavelength_data, wavelength, state_run, time_getData
    n_sensor = 0
    value = 0

    if arduinoData.in_waiting > 0 and state_run:
        current_data = np.array([])
        
        while n_sensor != 288:
            (n_sensor, value) = get_data(arduinoData.readline())

            if n_sensor == 1:
                time_getData = datetime.now()
                time_passed = (time_getData-start_time).total_seconds()
                time_stamp = np.append(time_stamp, time_passed)

            if n_sensor == target_sensor:
                target_wavelength_data = np.append(target_wavelength_data, value)
            current_data = np.append(current_data, value)
    
        
        with open(csv_file,'a', newline='') as f:
            w = csv.writer(f)
            w.writerow(np.concatenate(([str(time_getData)], current_data), axis = 0)) #adding the current time stamp to the front of the csv line

    
    fig.clf()

    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(time_stamp, target_wavelength_data)
    ax1.set_xlabel("Elapsed Time (Seconds)")
    ax1.set_ylabel("Fluorescence (RFU)")
    ax1.set_title("TARGET WAVELENGTH")
    ax1.set_ylim([0,1030])

    ax2 = fig.add_subplot(1,2,2) 
    ax2.plot(wavelength, current_data)
    ax2.set_xlabel("Wavelength")
    ax2.set_ylabel("Intensity (UNIT)")
    ax2.set_title("INSTANT SPECTRUM")
    ax2.set_ylim([0, 1030]) # change or comment out if need (e.g. testing)

    canvas.draw()
    root.after(1,loop)


def new_sample():
    global time_stamp, current_data, target_wavelength_data, sample_no, state_run, csv_file, current_sample

    state_run = False

    target_wavelength_data = np.array([]) 
    time_stamp = np.array([])
    current_data = np.zeros(288,)
    sample_no += 1
    csv_file = f"test{sample_no}.csv"

    with open(csv_file,'a', newline='') as f:
        w = csv.writer(f)
        w.writerow([f"sample no: {sample_no} "])
    
    current_sample.config(text=f"Current Sample No.:{sample_no}")

    if (button_start["state"] ==  DISABLED):
        button_start["state"] = NORMAL

def gui_start():
    global state_run, start_time, button_start
    state_run = True
    start_time = datetime.now()
    button_start["state"] = DISABLED



#widget
current_sample = Label(text=f"Current Sample No.:{sample_no}")
current_sample.pack(fill='x')


button_start = Button(text="START", command = gui_start)
button_start.pack()

button_new_sample = Button(text="NEW SAMPLE", command = new_sample)
button_new_sample.pack()



root.after(1,loop)
root.mainloop()

