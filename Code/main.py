'''
Robotic Arm
Author: Braden Barlean

Materials:
1 - Raspberry Pi Pico W
3 - SG-90 Servo Motors
1 - PS2 Joystick
1 - SSD1306 OLED LCD

Maps the joystick movement to servo 1's movement.
This is done using only the x-axis of the joystick.

This data is displayed on the OLED, as well as
being graphed above the displayed text. Only one of the positional
data is plotted becuase they correspond to each other.

The button function of the joystick controls servo 2 to act as the
switch that will open and close the hand of the robot arm.

The state of servo 2 is displayed on the OLED as shut or open to
represent the hand state of the robot's hand.

This program will also be recording positional data of the joystick
and the servo motors and will export that data in a csv file.
This can then be used by a seperate Python program file to visualize
the data using matplotlib and tkinter.
'''
from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime


class OLED:
    """
    A class representing an OLED display that can be controlled
    using the MicroPython language. This class uses the SSD1306_I2C
    driver to communicate with the OLED display over I2C.

    Attributes:

    * width (int): The width of the OLED display, in pixels.
    * height (int): The height of the OLED display, in pixels.
    * oled (SSD1306_I2C): An instance of the SSD1306_I2C driver, used
      to communicate with the OLED display over I2C.
    * graph_buffer (bytearray): A buffer used for displaying graphics
      on the OLED display. This buffer is half the height of the OLED
      display, since the display is split into two sections.
    * graph_framebuf (framebuf.FrameBuffer): An instance of the
      MicroPython framebuf module used for displaying graphics on the
      OLED display.
    
    Methods:

    * line(x1, y1, x2, y2, color): Draws a line on the OLED display
      between the points (x1, y1) and (x2, y2), with the given color.
    * text(text, x, y): Displays the given text on the OLED display
      at the specified position (x, y).
    * fill_rect(x, y, width, height, color): Fills a rectangular area
      on the OLED display with the given color.
    * blit(framebuf, x, y): Copies the contents of the given frame
      buffer to the OLED display at the specified position (x, y).
    * show(): Updates the OLED display with any changes that have
      been made.
    * fill(color): Fills the entire OLED display with the given color.
    """
    def __init__(self, i2c, width=128, height=64):
        self.width = width
        self.height = height
        self.oled = SSD1306_I2C(width, height, i2c)
        self.graph_buffer = bytearray(width * (height//2) // 8)
        self.graph_framebuf = framebuf.FrameBuffer(memoryview
                                                   (self.graph_buffer),
                                                   width, (height//2),
                                                   framebuf.MONO_HLSB)

    def line(self, x1, y1, x2, y2, color):
        self.oled.line(x1, y1, x2, y2, color)

    def text(self, text, x, y):
        self.oled.text(text, x, y)

    def fill_rect(self, x, y, width, height, color):
        self.oled.fill_rect(x, y, width, height, color)

    def blit(self, framebuf, x, y):
        self.oled.blit(framebuf, x, y)

    def show(self):
        self.oled.show()

    def fill(self, color):
        self.oled.fill(color)

class Servo:
    """
    A class representing a servo motor that can be controlled using
    the MicroPython language. This class uses the machine.PWM module
    to generate pulse-width modulation signals that are used to control
    the position of the servo motor.

    Attributes:

    * pin (int): The pin number to which the servo motor is connected.
    * pwm (machine.PWM): An instance of the machine.PWM module used to
      generate PWM signals for controlling the servo motor.
    
    Methods:

    * set_position(position): Sets the position of the servo motor to
      the specified value. The position value should be an integer
      between 0 and 65535, representing the duty cycle of the PWM
      signal in microseconds. This method converts the position value
      to a 16-bit unsigned integer and sets the duty cycle of the PWM
      signal to that value, causing the servo motor to move to the
      corresponding position.
    """
    def __init__(self, pin):
        self.pin = pin
        self.pwm = machine.PWM(machine.Pin(pin))
        self.pwm.freq(50)

    def set_position(self, position):
        self.pwm.duty_u16(int(position))

class Joystick:
    """
    A class representing a joystick that can be read using the
    MicroPython language. This class uses the machine.ADC and
    machine.Pin modules to read the analog position values of the
    joystick and the digital state of the joystick button.

    Attributes:

    * x_pin (int): The pin number to which the X-axis of the joystick
      is connected.
    * y_pin (int): The pin number to which the Y-axis of the joystick
      is connected.
    * sw_pin (int): The pin number to which the button of the joystick
      is connected.
    
    Methods:

    * read_position(): Reads the current position of the joystick and
      returns a list containing the X and Y position values as unsigned
      16-bit integers. The X and Y position values range from 0 to
      65535, with 0 representing the minimum position and 65535
      representing the maximum position.
    * read_button_state(): Reads the current state of the joystick
      button and returns a boolean value representing the button state.
      True indicates that the button is pressed, while False indicates
      that the button is released.
    """
    def __init__(self, x_pin, y_pin, sw_pin):
        self.x_pin = machine.ADC(x_pin)
        self.y_pin = machine.ADC(y_pin)
        self.sw_pin = machine.Pin(sw_pin, machine.Pin.IN, machine.Pin.PULL_UP)

    def read_position(self):
        x_val = self.x_pin.read_u16()
        y_val = self.y_pin.read_u16()
        return [x_val, y_val]

    def read_button_state(self):
        return self.sw_pin.value()

def joystick_servo_mapping(x_val, servo_max, servo_min, pwm1):
    """
    A function that maps the position values of a joystick to the
    position of a servo motor. This function takes the X-axis position
    value of a joystick, the maximum and minimum positions of the servo
    motor, and an instance of the machine.PWM module used to control
    the servo motor as input parameters.

    Parameters:

    * x_val (int): The X-axis position value of the joystick as an
      unsigned 16-bit integer. The X-axis position value ranges from 0
      to 65535, with 0 representing the minimum position and 65535
      representing the maximum position.
    * servo_max (int): The maximum position of the servo motor in
      microseconds. This value should be an integer between 0 and 65535.
    * servo_min (int): The minimum position of the servo motor in
      microseconds. This value should be an integer between 0 and 65535.
    * pwm1 (machine.PWM): An instance of the machine.PWM module used
      to control the servo motor.
    
    Returns:

    * servo_position (int): The position of the servo motor in microseconds
      as an integer. If the joystick isn't moving, the function returns a
      fixed value to prevent the motor from shaking. Otherwise, the function
      returns the mapped servo position value as an integer.
    
    The function first maps the joystick position value to the range of the
    servo motor position using linear interpolation. Then, if the joystick
    isn't moving, it sends back a fixed position value to prevent the servo
    motor from shaking. Otherwise, it sets the duty cycle of the PWM signal
    to the mapped servo position value, causing the servo motor to move to
    the corresponding position. Finally, the function returns the servo
    position value as an integer.
    """  
    # Map joystick positional data to servo motor position
    servo_position = round(((x_val - 0) / (65536 - 0)
                            * (servo_max - servo_min) + servo_min))

    # If the joystick isn't moving send back a single value to
    # prevent motor shake
    if servo_position < 3900:
        pwm1.duty_u16(3800)
    # Else sends new servo position to the servo motor
    else:
        pwm1.duty_u16(int(servo_position))
    
    return servo_position    

def plotting(x_val, servo_position, graph_framebuf, oled):
    """
    Plots joystick and servo positional data on an OLED screen.

    Parameters:
    
    * x_val (int): Positional data of the joystick.
    * servo_position (int): Positional data of the servo motor.
    * graph_framebuf (framebuf): A frame buffer used to draw the
      graph on the OLED.
    * oled (OLED): An OLED display to plot the data on.

    Returns:
    
    * None
    """
    # Creates screen segmentation and hand status title
    oled.line(0, 38, 125, 38, 1)
    oled.line(85, 38, 85, 63, 1)
    oled.text("Hand:", 90, 40)

    # Draw the graph
    # Shift the existing graph one pixel to the left
    graph_framebuf.scroll(-1, 0)
    # Clear the rightmost column of the graph
    graph_framebuf.fill_rect(127, 0, 1, 38, 0)
    # Calculate the position of the joystick and servo on the graph
    joystick_position = 31 - (x_val // 2048)
    # Draw the line for the joystick positions
    graph_framebuf.line(126, joystick_position, 127,
                        joystick_position, 1)

    # Blit the graph to the OLED display
    oled.blit(graph_framebuf, 0, 0)

    # Displays joystick and servo data to the OLED
    oled.text("PS2:" + str(x_val), 0, 40)
    oled.text("SG90:" + str(servo_position), 0, 50)

    # Show on the OLED
    oled.show()

    # Wait a short time
    utime.sleep_ms(50)

    # Clear the OLED
    oled.fill(0)

def main():
    """
    Controls the robotic arm by reading the position of the joystick,
    mapping it to the joint servo motor, and displaying the positions
    of the joystick and servo motor on an OLED screen. Opens and closes
    the hand servo motor based on the state of the joystick button.
    Records the position of the servo motor and joystick to a CSV file
    for later analysis. Exits when the CSV file has recorded 500 data points.
    """
    data = open('data.csv', 'w')
    data.write('timestamp,servo_pos,joystick_pos\n')
    
    # Create an I2C object
    i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=200000)
    screen = OLED(i2c)
    
    # Create the servo objects
    joint_servo = Servo(2)
    hand_servo = Servo(3)
    
    # Create the joystick object
    joystick = Joystick(26, 27, 28)

    # Define the PWM range for the SG-90 Servo Motor
    servo_min = 500
    servo_max = 7000

    # Set the starting position of the joint servo motors
    joint_servo.set_position(1250)
    hand_servo.set_position(1250)
    
    # Clear the OLED
    screen.oled.fill(0)
    count = 0
    
    while True:
        # Stores the positional data of the joystick and the button
        joystick_position = joystick.read_position()
        button_state = joystick.read_button_state()
        
        # Stores the servo position relative to the joystick position
        servo = joystick_servo_mapping(joystick_position[0], servo_max,
                                       servo_min, joint_servo.pwm)
        
        # Uses the joystick position to plot on OLED
        plotting(joystick_position[0], servo, screen.graph_framebuf,
                 screen.oled)
        
        # Maps the on/off state of the joystick button to turn a motor.
        # This motor will be the one that opens and closes the hand.
        if button_state == 1:
            hand_servo.pwm.duty_u16(1250)
            screen.text("Shut", 95, 50)
        elif button_state == 0:
            hand_servo.pwm.duty_u16(3800)
            screen.text("Open", 95, 50)
        
        # Checks the count to collect a max of 500 readings for the CSV
        if count > 0 and count < 501:
            timestamp = utime.time()           
            data.write('{},{},{}\n'.format(timestamp, servo,
                                           joystick_position[0]))
            utime.sleep_ms(100)
            
        elif count >= 501:
            data.close()
            print('Data Collected')
                
        count += 1

if __name__ == "__main__":
    main()
        