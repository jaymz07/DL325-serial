'''
Serial control for Newport DL325 translation stage.
Used as a module

The translation stage controller acts as a USB-Serial device.
Baud rate is 921600.
'''

import serial
import time

#ser = serial.Serial('COM3', 921600) # For Windows systems
ser = serial.Serial('/dev/ttyACM0', 921600) # For Linux systems

WAIT_TIME = 0.01

print("-------------------Translation Stage Control (Serial Version)-----------------")

# ----------Serial Communication-----------------

'''
Send serial command. No return character needed.
'''
def send(comm):
    ser_command = (comm + '\r\n').encode()
    ser.write(ser_command)

'''
Read Serial Response.
'''
def read():
    data = b''
    while True:
        charOut = ser.read()
        data = data + charOut
        if(charOut == b'\n'):
            break
    return data.decode().replace('\r\n', '')

'''
Send command, and listen for response.
'''
def query(comm):
    send(comm)
    return read()

print("Translation Stage Controller Firmware Version:")
response = query('VE')

# ----------Simple Utility Functions.-----------------

'''
Sets the velocity used for positioning.
'''
def set_vel(vel):
    send('VA%.6f' % vel)

'''
Go to the specified position.
'''
def go_pos(pos):
    send('PA%.6f' % pos)

'''
Returns the current position as float.
'''
def get_pos():
    response = query('PA?')
    val = response.replace('PA','')
    return float(val)

'''
Returns True if controller is in motion state.
'''
def is_moving():
    state = query('TS')
    return state[-2:] == '3C'

'''
Pauses execution until motion stops.
'''
def wait_to_stop():
    while is_moving():
        time.sleep(WAIT_TIME)

'''
Turns off the motor so that the stage can be moved by hand.
'''
def disable():
    send("MM0")

'''
Turns on the active positioning and the stage moter.
The stage cannot be moved by hand.
'''
def enable():
    send("MM1")

'''
Brings controller to state which is ready for positioning.
'''
def initialize():
    # Set initialization state
    send('IE')

    wait_to_stop()

    # Execute homing on TS stage
    send('OR')

    wait_to_stop()
