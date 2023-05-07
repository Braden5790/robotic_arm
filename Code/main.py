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
This can then be used by the second Python file to visualize the data
using matplotlib and tkinter.

Next Steps: 
* Potentially add another servo to act as the rotational axis (this
requires a dive into the documentation about the maximum capacity),
this could be mapped to the y-axis of the joystick.
'''
from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime


class OLED:
    def __init__(self, i2c, width=128, height=64):
        self.width = width
        self.height = height
        self.oled = SSD1306_I2C(width, height, i2c)
        self.graph_buffer = bytearray(width * (height//2) // 8)
        self.graph_framebuf = framebuf.FrameBuffer(memoryview(self.graph_buffer), width, (height//2), framebuf.MONO_HLSB)

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
    def __init__(self, pin):
        self.pin = pin
        self.pwm = machine.PWM(machine.Pin(pin))
        self.pwm.freq(50)

    def set_position(self, position):
        self.pwm.duty_u16(int(position))

class Joystick:
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
    # Map joystick positional data to servo motor position
    servo_position = round(((x_val - 0) / (65536 - 0) * (servo_max - servo_min) + servo_min))

    # If the joystick isn't moving send back a single value to prevent motor shake
    if servo_position < 3900:
        pwm1.duty_u16(3800)
    # Else sends new servo position to the servo motor
    else:
        pwm1.duty_u16(int(servo_position))
    
    return servo_position    

def plotting(x_val, servo_position, graph_framebuf, oled):
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
    graph_framebuf.line(126, joystick_position, 127, joystick_position, 1)

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
    data = open('data.csv', 'w')
    data.write('timestamp,servo_pos,joystick_pos\n')
    
    # Create an I2C object
    i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=200000)
    screen = OLED(i2c)
    
    joint_servo = Servo(2)
    hand_servo = Servo(3)
    
    joystick = Joystick(26, 27, 28)

    # Define the PWM range for the SG-90 Servo Motor
    servo_min = 500
    servo_max = 7000

    joint_servo.set_position(1250)
    hand_servo.set_position(1250)
    
    screen.oled.fill(0)
    count = 0
    
    
    while True:
        joystick_position = joystick.read_position()
        button_state = joystick.read_button_state()
        
        servo = joystick_servo_mapping(joystick_position[0], servo_max, servo_min, joint_servo.pwm)
        
        plotting(joystick_position[0], servo, screen.graph_framebuf, screen.oled)
        
        # Maps the on/off state of the joystick button to turn a motor.
        # This motor will be the one that opens and closes the hand.
        if button_state == 1:
            hand_servo.pwm.duty_u16(1250)
            screen.text("Shut", 95, 50)
        elif button_state == 0:
            hand_servo.pwm.duty_u16(3800)
            screen.text("Open", 95, 50)
        
        if count > 0 and count < 501:
            timestamp = utime.time()
            
            
            data.write('{},{},{}\n'.format(timestamp, servo, joystick_position[0]))
            utime.sleep_ms(100)
            
        elif count >= 501:
            data.close()
            print('done')
                
        count += 1

if __name__ == "__main__":
    main()
        
