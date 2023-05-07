# Robotic Arm 

The goal of this project is to create a robotic arm. This exercise is being done to learn more about MicroPython, Raspberry Pi, and robotic programming. In building this robotic arm, I utilized CAD, coding, and circuit analysis skills to create a robotic arm.

## Getting Started

### Software Requirements
This code is utilized in **two major ways**. The **first** way is using an IDE that is suitable for MicroPython and interacting with a Raspberry Pi. In this case, I used Thonny. In using Thonny, the main.py code can be delivered to the Raspberry Pi, and the CSV file can be retrieved from the Raspberry Pi. The **second** way is using a "typical"  IDE like VS Code to run the plotting program. 

Thonny Dependencies:
* SSD1306 OLED LCD Library (on board)

Plotting Dependencies:
* Matplotlib

### Hardware Requirements
Access to a 3D printer is required to make this robotic arm. The CAD files will need to be put through a slicer (my favorite is Ultimaker Cura) to be able to be 3D printed. 

* Raspberry Pi Pico W (x1)
* SG-90 Servo Motors (x3)
* PS2 Joystick (x1)
* SSD1306 OLED LCD (x1)
* Breadboard (x1)

### Assembly

Circuit:
* Info about the circuit

Hardware:
* Info about the 3D printed parts, screws, and motors

### First Test
To get started, the main.py file will need to be uploaded to the Raspberry Pi. This can be done using softwares such as Thonny. After uploading that file to the Raspberry Pi, the file can be run. Given everything in Assembly went well, the joystick should be controlling the movement of the servo motors, actuating the arm. After starting the script, a CSV file will be generated and will have positional data of the servo motors and joystick stored on it.

To use the plotter.py functionality of this project, the CSV file will have to be collected from the Raspberry Pi and saved to the same folder as the plotter.py file. This will ensure the plotter.py program will have a CSV file to read from.

## Author

Braden Barlean
