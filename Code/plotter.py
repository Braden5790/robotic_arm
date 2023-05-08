"""
This program reads data from a CSV file and displays positional data
from a robot arm, either from a servo or joystick, in a Tkinter window.
The user can select which data to display by clicking on one of three
buttons. The program uses the matplotlib and PIL libraries to plot and
display the data.

The program opens the 'data.csv' file and extracts the timestamps and
values for the servo and joystick into separate lists. It defines three
functions to update the plot based on the user's button presses:
plot_servo, plot_joystick, and plot_servo_and_joystick. Each function
clears the current plot and plots the timestamp versus positional data
for the corresponding device. The functions also set the x-axis label
to 'Timestamp', the y-axis label to 'Value', and the title to the
appropriate title.

The program creates a Tkinter window and a canvas to display the plot.
It also loads an image of the robot arm using the Pillow library,
resizes it to fit within the screen, and displays it using a Label
widget. The program creates three buttons to select which data to
display and packs them into the window. When a user clicks one of the
buttons, the corresponding function is called to update the plot. The
program sets the protocol for the WM_DELETE_WINDOW event to root.quit()
and starts the Tkinter main loop.
"""
import csv
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Open the data files and read the contents
# Change to 'sample_data.csv' if you want to use the sample data
with open('data.csv', 'r') as f:
    data = list(csv.reader(f))

# Extract the timestamps and values into separate lists
timestamps = [float(row[0]) for row in data[1:]]
servo_values = [int(row[1]) for row in data[1:]]
joystick_values = [int(row[2]) for row in data[1:]]

# Define functions to update the plot based on button presses
def plot_servo():
    """
    Clear the current plot and plot the timestamp versus servo
    positional data.
    
    This function clears the current plot and
    plots the timestamps versus servo positional data.
    It sets the x-axis label to 'Timestamp', the y-axis label
    to 'Value', and the title to 'Positional Data: Servo'.
    Finally, it draws the updated plot.
    """
    plt.clf()
    plt.plot(timestamps, servo_values, color='blue', label='Servo')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Positional Data: Servo')
    canvas.draw()

def plot_joystick():
    """
    Clear the current plot and plot the timestamp versus joystick
    positional data.
    
    This function clears the current plot and plots the timestamps
    versus joystick positional data. It sets the x-axis label to
    'Timestamp', the y-axis label to 'Value', and the title to
    'Positional Data: Joystick'. Finally, it draws the updated plot.
    """
    plt.clf()
    plt.plot(timestamps, joystick_values, color='red', label='Joystick')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Positional Data: Joystick')
    canvas.draw()

def plot_servo_and_joystick():
    """
    Clear the current plot and plot the timestamp versus servo
    and joystick positional data.
    
    This function clears the current plot and plots the timestamps
    versus servo and joystick positional data. It sets the x-axis
    label to 'Timestamp', the y-axis label to 'Value', and the
    title to 'Positional Data: Servo vs. Joystick'. Finally, it
    draws the updated plot with a legend indicating the servo and
    joystick lines.
    """
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
image = Image.open('robot_arm_final.jpg')

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

intro_label = tk.Label(master=root, 
                       text="Click a button to see positional data",
                       font=('Arial', 16))
intro_label.pack(side=tk.TOP, pady=20)

# Create a Label widget to display the image
label = tk.Label(master=root, image=photo, padx=0, pady=0,
                 borderwidth=0, highlightthickness=0)

# Add the Label widget to the window
label.pack()

# Create three buttons to select the data to display
button_data1 = tk.Button(master=root, text='Servo', 
                         font=('Arial', 20), command=plot_servo)
button_data1.pack(side=tk.LEFT)

button_data2 = tk.Button(master=root, text='Joystick', 
                         font=('Arial', 20), command=plot_joystick)
button_data2.pack(side=tk.LEFT)

button_data1_and_data2 = tk.Button(master=root, 
                                   text='Servo vs. Joystick', 
                                   font=('Arial', 20), 
                                   command=plot_servo_and_joystick)
button_data1_and_data2.pack(side=tk.LEFT)

button_data1.pack(side=tk.LEFT, anchor=tk.CENTER, padx=50, pady=10)
button_data2.pack(side=tk.LEFT, anchor=tk.CENTER, padx=50, pady=10)
button_data1_and_data2.pack(side=tk.LEFT, anchor=tk.CENTER, padx=50, 
                            pady=10)

# Set the protocol for the WM_DELETE_WINDOW event to root.quit()
root.protocol("WM_DELETE_WINDOW", root.quit)

# Start the Tkinter main loop
tk.mainloop()
