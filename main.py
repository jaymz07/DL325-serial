'''
Simple example showing the DL325 translation stage
moving back and fourth with a pre-defined velocity between two pre-defined positions.

Set the proper device string for your system in ts_control.py.
'''

# Import the DL325 control module
import ts_control as tsc

# Define our two positions
POS_1 = 155 - 40
POS_2 = 155 + 40

# Velocity that we move back and fourth with
VELOCITY_MEAS = 1.0

# Number of times to move one-way distance
NUM_TRAVELS = 10

# Velocity that we get into initial position with
VELOCITY_INIT = 100.0


if __name__ == '__main__':
    # Initialize, home, and wait for stage to stop moving
    tsc.initialize()
    tsc.wait_to_stop()
    tsc.enable()

    # The state variable will act as an index for the positions list
    state = 0
    positions = [POS_1, POS_2]

    # Get Current Position
    pos_curr = tsc.get_pos()

    # Determine closest starting position
    state = 0 if abs(pos_curr - POS_1) < abs(pos_curr - POS_2) else 1
    pos_next = positions[state]

    # Go to closest starting position
    tsc.set_vel(VELOCITY_INIT)
    tsc.go_pos(pos_next)
    tsc.wait_to_stop()

    # Loop to move back and fourth
    for _ in range(NUM_TRAVELS):
        # Go to other position
        state = 1-state
        pos_next = positions[state]
        tsc.set_vel(VELOCITY_MEAS)
        tsc.go_pos(pos_next)
        tsc.wait_to_stop()
