from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import serial
import string
#import pandas as pd
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
calibration_set = np.zeros(288,) 
csv_file = f"test{sample_no}.csv"

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

def gui_start():
    global state_run
    state_run = True

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
    global time_stamp, current_data, target_wavelength_data, wavelength, state_run
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
        
        current_data -= calibration_set
        
        with open(csv_file,'a', newline='') as f:
            w = csv.writer(f)
            w.writerow(np.insert(current_data, 0, time_getData)) #adding the current time stamp to the front of the csv line

    
    fig.clf()

    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(time_stamp, target_wavelength_data)
    ax1.set_xlabel("Elapsed Time (Seconds)")
    ax1.set_ylabel("Fluorescence (RFU)")
    ax1.set_title("TARGET WAVELENGTH")
    ax1.set_ylim([0,2000])

    ax2 = fig.add_subplot(1,2,2) 
    ax2.plot(wavelength, current_data)
    ax2.set_xlabel("Wavelength")
    ax2.set_ylabel("Intensity (UNIT)")
    ax2.set_title("INSTANT SPECTRUM")
    ax2.set_ylim([-100, 2000]) # change or comment out if need (e.g. testing)

    canvas.draw()
    root.after(1,loop)
    
def calibration():
    global calibration_set, state_run
    
    while arduinoData.in_waiting == 0:
        pass

    for _ in range(5): #change value for better calibration
        nth_sensor = 0
        place_holder = np.array([])
        while nth_sensor != 288:
            (nth_sensor, value) = get_data(arduinoData.readline())
            place_holder = np.append(place_holder, value)
            print(place_holder.size)
        calibration_set += place_holder
    
    calibration_set /= 5.0 #change value for better calibration
    calibration_set = np.round(calibration_set, decimals=2)
    print(calibration_set)
    #print calibration_set to csv for record 

def new_sample():
    global time_stamp, current_data, target_wavelength_data, sample_no 

    target_wavelength_data = np.array([]) 
    time_stamp = np.array([])
    current_data = np.zeros(288,)
    sample_no += 1

    with open(csv_file,'a', newline='') as f:
        w = csv.writer(f)
        w.writerow()

#widget
current_sample = Label(text=f"Current Sample No.:{sample_no}")
current_sample.pack(fill='x')

button_calibration = Button(text = "CALIBRATION", command = calibration)
button_calibration.pack()

button_start = Button(text="START", command = gui_start)
button_start.pack()

button_new_sample = Button(text="NEW SAMPLE", command = new_sample)
button_new_sample.pack()

root.after(1,loop)
root.mainloop()

