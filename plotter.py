import csv
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Open the data files and read the contents
with open('data.csv', 'r') as f:
    data = list(csv.reader(f))

# Extract the timestamps and values into separate lists
timestamps = [float(row[0]) for row in data[1:]]
servo_values = [int(row[1]) for row in data[1:]]
joystick_values = [int(row[2]) for row in data[1:]]

# Define functions to update the plot based on button presses
def plot_servo():
    plt.clf()
    plt.plot(timestamps, servo_values, color='blue', label='Servo')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Positional Data: Servo')
    canvas.draw()

def plot_joystick():
    plt.clf()
    plt.plot(timestamps, joystick_values, color='red', label='Joystick')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Positional Data: Joystick')
    canvas.draw()

def plot_servo_and_joystick():
    plt.clf()
    plt.plot(timestamps, servo_values, color='blue', label='Servo')
    plt.plot(timestamps, joystick_values, color='red', label='Joystick')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Positional Data: Servo vs. Joystick')
    plt.legend()
    canvas.draw()

# Create a Tkinter window and canvas to display the plot
root = tk.Tk()
root.title('Positional Data')
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Load the image file using Pillow
image = Image.open('robot_arm.jpg')

# Resize the image to fit within the screen
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
aspect_ratio = image.width / image.height
if aspect_ratio > width / height:
    new_width = width - 100
    new_height = int(new_width / aspect_ratio)
else:
    new_height = height - 100
    new_width = int(new_height * aspect_ratio)
image = image.resize((new_width, new_height))

# Convert the Pillow image to a format that PhotoImage can use
photo = ImageTk.PhotoImage(image)

intro_label = tk.Label(master=root, text="Click a button to see positional data", font=('Arial', 16))
intro_label.pack(side=tk.TOP, pady=20)

# Create a Label widget to display the image
label = tk.Label(master=root, image=photo, padx=0, pady=0, borderwidth=0, highlightthickness=0)

# Add the Label widget to the window
label.pack()

# Create three buttons to select the data to display
button_data1 = tk.Button(master=root, text='Servo', font=('Arial', 20), command=plot_servo)
button_data1.pack(side=tk.LEFT)

button_data2 = tk.Button(master=root, text='Joystick', font=('Arial', 20), command=plot_joystick)
button_data2.pack(side=tk.LEFT)

button_data1_and_data2 = tk.Button(master=root, text='Servo vs. Joystick', font=('Arial', 20), command=plot_servo_and_joystick)
button_data1_and_data2.pack(side=tk.LEFT)

button_data1.pack(side=tk.LEFT, anchor=tk.CENTER, padx=50, pady=10)
button_data2.pack(side=tk.LEFT, anchor=tk.CENTER, padx=50, pady=10)
button_data1_and_data2.pack(side=tk.LEFT, anchor=tk.CENTER, padx=50, pady=10)

# Set the protocol for the WM_DELETE_WINDOW event to root.quit()
root.protocol("WM_DELETE_WINDOW", root.quit)

# Start the Tkinter main loop
tk.mainloop()
