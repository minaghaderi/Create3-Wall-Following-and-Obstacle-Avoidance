# Import necessary libraries from the iRobot SDK
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from irobot_edu_sdk.music import Note

# Initialize the robot with Bluetooth connection
robot = Create3(Bluetooth())

# Robot speed settings and thresholds
robot_speed = 16  # Speed of the robot
wall_detection_threshold = 50  # Threshold value for detecting a wall on the left side
left_wall_close_threshold = 160  # Threshold when the left wall is too close
obstacle_detection_threshold = 50  # Threshold value for detecting obstacles
x_offset = -75  # X coordinate adjustment for navigating
y_offset = 238  # Y coordinate adjustment for navigating

# List to keep track of robot positions
robot_positions = []

# Musical notes to be played when the robot reaches its destination
song_notes = [
    (440, 0.5),  # A4
    (440, 0.5),  # A4
    (493.88, 0.5),  # B4
    (493.88, 0.5),  # B4
    (523.25, 0.5),  # C5
    (523.25, 0.5),  # C5
    (493.88, 1.0),  # B4
    (440, 0.5),  # A4
    (440, 0.5),  # A4
    (493.88, 0.5),  # B4
    (493.88, 0.5),  # B4
    (523.25, 0.5),  # C5
    (523.25, 0.5),  # C5
    (493.88, 1.0),  # B4
]

# Function triggered when the right bumper is hit
@event(robot.when_bumped, [False, True])
async def handle_right_bump(robot):
    print("Bumped into something on the right")
    await robot.move(-10)  # Move backward
    await robot.turn_left(45)  # Turn left by 45 degrees

# Function triggered when the left bumper is hit
@event(robot.when_bumped, [True, False])
async def handle_left_bump(robot):
    print("Bumped into something on the left")
    await robot.move(-10)  # Move backward
    await robot.turn_right(45)  # Turn right by 45 degrees

# Function to play a song when the robot reaches its destination
async def play_completion_song(robot):
    for note, duration in song_notes:
        await robot.play_note(note, duration)

# Function to make the robot move forward
async def move_forward(robot):
    await robot.set_lights_on_rgb(0, 255, 0)  # Set green light
    await robot.set_wheel_speeds(robot_speed, robot_speed)  # Move forward at set speed

# Function to make a slight left turn (when moving away from a wall)
async def slight_left_turn(robot):
    await robot.set_lights_on_rgb(255, 0, 0)  # Set red light
    await robot.set_wheel_speeds(robot_speed * 0.7, robot_speed * 1.6)  # Slight left turn

# Function to make a sharp right turn (when an obstacle is detected)
async def sharp_right_turn(robot):
    await robot.set_lights_on_rgb(0, 0, 255)  # Set blue light
    await robot.turn_right(90)  # Turn 90 degrees to the right

# Function to escape when too close to the left wall by turning slightly right
async def slight_right_escape(robot):
    await robot.set_lights_on_rgb(0, 0, 255)  # Set blue light
    await robot.set_wheel_speeds(robot_speed * 1.4, robot_speed * 0.8)  # Turn slightly right

# Function to check if the robot is near the left wall
def is_near_left_wall(sensor_data):
    return sensor_data[1] > wall_detection_threshold or sensor_data[0] > wall_detection_threshold

# Function to check if the robot detects an obstacle
def is_obstacle_detected(sensor_data):
    return (sensor_data[3] > 60 and sensor_data[2] > 60 and sensor_data[4] > 60) or sensor_data[3] > 180

# Function to check if the robot is too close to the left wall and needs to turn right
def should_turn_slight_right(sensor_data):
    return sensor_data[1] >= left_wall_close_threshold or sensor_data[0] >= left_wall_close_threshold

# Function to get the robot's current position (x, y, and heading)
async def get_robot_position(robot):
    try:
        position = await robot.get_position()
        return position.x, position.y, position.heading
    except:
        return None

# Main event function that runs when the robot starts
@event(robot.when_play)
async def play(robot):
    await robot.reset_navigation()

    # Coordinates for the destination point
    end_x, end_y = -195, 0

    # Main loop for navigation
    while True:
        # Get sensor data
        sensor_data = (await robot.get_ir_proximity()).sensors

        # Get and record the robot's position
        position = await get_robot_position(robot)
        robot_positions.append(position)
        print(robot_positions)

        # If a valid position is received, check if the robot has reached its destination
        if position:
            print('Position (x, y, heading):', position)
            if 0 < abs(position[0] - end_x) < 15 and 0 < abs(position[1] - end_y) < 15:
                await robot.navigate_to((end_x + x_offset), (end_y + y_offset))  # Move to final destination
                await robot.set_wheel_speeds(0, 0)  # Stop the robot
                await play_completion_song(robot)  # Play the song at the destination
                print("Task completed!")
                break

        # Check for obstacles and walls to decide the next movement
        if is_obstacle_detected(sensor_data):
            await sharp_right_turn(robot)
        elif not is_near_left_wall(sensor_data):
            await slight_left_turn(robot)
        elif should_turn_slight_right(sensor_data):
            if sensor_data[0] <= 70 or sensor_data[1] <= 70:
                await move_forward(robot)
            else:
                await slight_right_escape(robot)
        else:
            await move_forward(robot)

# Start the robot's play function
robot.play()
