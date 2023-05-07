# Robotic Arm 

The goal of this project is to create a robotic arm. This exercise is being done to learn more about MicroPython, Raspberry Pi, and robotic programming. In building this robotic arm, I utilized CAD, coding, and circuit analysis skills to create a robotic arm.

## Getting Started

### Software Requirements
This code is utilized in **two major ways**. The **first** way is using an IDE that is suitable for MicroPython and interacting with a Raspberry Pi. In this case, I used Thonny. In using Thonny, the main.py code can be delivered to the Raspberry Pi, and the CSV file can be retrieved from the Raspberry Pi. The **second** way is using a "typical"  IDE like VS Code to run the plotting program. 

Thonny Dependencies:
* SSD1306 OLED LCD Library (on board)

Plotting Dependencies:
* Matplotlib
* Tkinter

### Hardware Requirements
Access to a 3D printer is required to make this robotic arm. The CAD files will need to be put through a slicer (my favorite is Ultimaker Cura) to be able to be 3D printed. 

* Raspberry Pi Pico W (x1)
* SG-90 Servo Motors (x3)
* PS2 Joystick (x1)
* SSD1306 OLED LCD (x1)
* Breadboard (x1)

### Assembly

**Circuit:**

![alt text](https://github.com/Braden5790/robotic_arm/blob/main/Images/picow-pinout.svg)

The pinout diagram is a very important and useful resource to keep close while working any kind of microprocessor. In this case, this is the pinout diagram for the Raspberry Pi Pico W (RPPW). **Note:** There are two servo motors wired the exact same for both of the joint servos.

RPPW to OLED LCD:

* 18 (GND) to GND 
* 40 (VBUS) to VCC
* 22 (GP17) to SCL
* 21 (GP16) to SDA

RPPW to Joint Servo Motors:

* 18 (GND) to GND
* 4 (GP2) to Signal
* 40 (VBUS) to VCC

RPPW to Hand Servo Motor:

* 18 (GND) to GND
* 5 (GP3) to Signal
* 40 (VBUS) to VCC

RPPW to PS2 Joystick:

* 18 (GND) to GND
* 36 (3V3) to VCC
* 31 (GP26) to VRx
* 32 (GP27) to VRy
* 34 (GP28) to SW


**Hardware:**

The hardware assembly is very straightforward. The motors are fitted to their corresponding holes in the 3D printed part, and are secured via the screws that came with the SG90 servo motors. The other hardware necessary is a M2x20 and a M2x8, and that is what is used to secure arm_3 to arm_4. It is important to note that the base must be securely attached to arm_1 for the robot to stay upright (i.e. using hot glue).

### First Test
To get started, the main.py file will need to be uploaded to the Raspberry Pi. This can be done using softwares such as Thonny. After uploading that file to the Raspberry Pi, the file can be run. Given everything in **Assembly** went smoothly, the joystick should be controlling the movement of the servo motors, actuating the arm. After starting the script, a CSV file will be generated and will have positional data of the servo motors and joystick stored on it. The robotic arm should look something like this:

![alt text](https://github.com/Braden5790/robotic_arm/blob/main/Images/robot_arm.png)

To use the plotter.py functionality of this project, the CSV file will have to be collected from the Raspberry Pi and saved to the same location as the plotter.py file. This will ensure the plotter.py program will have a CSV file to read from. If you do not have a Raspberry Pi, an example of the CSV that would be generated is in the **Data** folder.

Once ran, the plotter.py program will display a pop-up window that will display an image of what an example circuit and arm would look like, and it will have three buttons. The buttons will allow the user to select different versions of displaying the positional data, seen below (Servo Motor Position, Joystick Position, or Servo Motor vs. Joystick Position). All data was plotted using Matplotlib.

![alt text](https://github.com/Braden5790/robotic_arm/blob/main/Images/buttons.png)

## Author

Braden Barlean
