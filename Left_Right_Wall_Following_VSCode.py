# Import necessary libraries from the iRobot SDK
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from irobot_edu_sdk.music import Note

# Initialize the robot with Bluetooth connection
robot = Create3(Bluetooth("Robot 3"))

# Robot speed settings and thresholds
robot_speed = 15  # Speed of the robot
wall_detection_threshold = 50  # Threshold value for detecting walls (applies to both modes)
close_wall_threshold = 160  # Threshold for detecting when the wall is too close (both modes)
obstacle_detection_threshold = 50  # Threshold value for detecting obstacles
destination_x, destination_y = 184, -103  # Destination coordinates
offset_x, offset_y = 0, 0  # Offsets to adjust the final destination

# List to track the robot's positions
robot_positions = []

# Function to make the robot move forward
async def move_forward(robot):
    await robot.set_lights_on_rgb(0, 255, 0)  # Set light to green
    await robot.set_wheel_speeds(robot_speed, robot_speed)  # Move forward at set speed

# --- Bumper event handling ---
@event(robot.when_bumped, [False, True])  # Right bumper hit
async def handle_right_bump(robot):
    print("Bumped on the right side")
    await robot.move(-10)  # Move backward
    await robot.turn_left(45)  # Turn left by 45 degrees

@event(robot.when_bumped, [True, False])  # Left bumper hit
async def handle_left_bump(robot):
    print("Bumped on the left side")
    await robot.move(-10)  # Move backward
    await robot.turn_right(45)  # Turn right by 45 degrees

# --- Left Wall Following Logic ---
async def follow_left_wall(robot):
    # Function for slight left turn
    async def turn_left(robot):
        await robot.set_lights_on_rgb(255, 0, 0)  # Set light to red
        await robot.set_wheel_speeds(robot_speed * 0.7, robot_speed * 1.6)  # Slight left turn

    # Function for a sharp right turn
    async def turn_right(robot):
        await robot.set_lights_on_rgb(0, 0, 255)  # Set light to blue
        await robot.turn_right(90)  # Sharp right turn

    # Function to escape when too close to the left wall by turning slightly right
    async def escape_left_turn_right(robot):
        await robot.set_lights_on_rgb(0, 0, 255)  # Set light to blue
        await robot.set_wheel_speeds(robot_speed * 1.4, robot_speed * 0.8)  # Turn slightly right

    # Check if the robot is near the left wall
    def is_near_left_wall(sensors):
        return sensors[0] > wall_detection_threshold or sensors[1] > wall_detection_threshold

    # Check if the robot is too close to the left wall
    def should_turn_slight_right(sensors):
        return sensors[1] >= close_wall_threshold or sensors[0] >= close_wall_threshold

    # Function to get the robot's position
    async def get_robot_position(robot):
        try:
            pos = await robot.get_position()
            return pos.x, pos.y, pos.heading
        except:
            return None

    # Main loop for left wall following
    while True:
        sensors = (await robot.get_ir_proximity()).sensors  # Get sensor data

        pos = await get_robot_position(robot)  # Get robot position
        robot_positions.append(pos)
        print(robot_positions)

        # Check if the robot reached the destination
        if pos:
            print('Position (x, y, heading):', pos)
            if 0 < abs(pos[0] - destination_x) < 15 and 0 < abs(pos[1] - destination_y) < 15:
                await robot.navigate_to((destination_x + offset_x), (destination_y + offset_y))  # Navigate to final position
                await robot.set_wheel_speeds(0, 0)  # Stop the robot

                # Play a song at the end
                notes = [
                    (440, 0.5),  # A4
                    (493.88, 0.5),  # B4
                    (523.25, 0.5),  # C5
                    (493.88, 1.0),  # B4
                ]
                for note, duration in notes:
                    await robot.play_note(note, duration)

                print("STOP!")
                break

        # Check for obstacles and walls
        if check_obstacle(sensors):
            await turn_right(robot)
        elif not is_near_left_wall(sensors):
            await turn_left(robot)
        elif should_turn_slight_right(sensors):
            if sensors[0] <= 70 or sensors[1] <= 70:
                await move_forward(robot)
            else:
                await escape_left_turn_right(robot)
        else:
            await move_forward(robot)

# --- Right Wall Following Logic ---
async def follow_right_wall(robot):
    # Function for a slight right turn
    async def turn_right(robot):
        await robot.set_lights_on_rgb(0, 0, 255)  # Set light to blue
        await robot.set_wheel_speeds(robot_speed * 1.4, robot_speed * 0.5)  # Slight right turn

    # Function for a sharp left turn
    async def turn_left(robot):
        await robot.set_lights_on_rgb(255, 0, 0)  # Set light to red
        await robot.turn_left(90)  # Sharp left turn

    # Function to escape when too close to the right wall by turning slightly left
    async def escape_right_turn_left(robot):
        await robot.set_lights_on_rgb(255, 0, 0)  # Set light to red
        await robot.set_wheel_speeds(robot_speed * 0.6, robot_speed * 1.4)  # Turn slightly left

    # Check if the robot is near the right wall
    def is_near_right_wall(sensors):
        return sensors[6] > wall_detection_threshold or sensors[5] > wall_detection_threshold

    # Check if the robot is too close to the right wall
    def should_turn_slight_left(sensors):
        return sensors[5] >= close_wall_threshold or sensors[6] >= close_wall_threshold

    # Main loop for right wall following
    while True:
        sensors = (await robot.get_ir_proximity()).sensors  # Get sensor data

        pos = await get_robot_position(robot)  # Get robot position
        robot_positions.append(pos)
        print(robot_positions)

        # Check if the robot reached the destination
        if pos:
            print('Position (x, y, heading):', pos)
            if 0 < abs(pos[0] - destination_x) < 15 and 0 < abs(pos[1] - destination_y) < 15:
                await robot.navigate_to((destination_x + offset_x), (destination_y + offset_y))  # Navigate to final position
                await robot.set_wheel_speeds(0, 0)  # Stop the robot

                # Play a song at the end
                notes = [
                    (440, 0.5),  # A4
                    (493.88, 0.5),  # B4
                    (523.25, 0.5),  # C5
                    (493.88, 1.0),  # B4
                ]
                for note, duration in notes:
                    await robot.play_note(note, duration)

                print("STOP!")
                break

        # Check for obstacles and walls
        if check_obstacle(sensors):
            await turn_left(robot)
        elif not is_near_right_wall(sensors):
            await turn_right(robot)
        elif should_turn_slight_left(sensors):
            if sensors[6] <= 70 or sensors[5] <= 70:
                await move_forward(robot)
            else:
                await escape_right_turn_left(robot)
        else:
            await move_forward(robot)

# Function to check if an obstacle is detected
def check_obstacle(sensors):
    return sensors[3] > obstacle_detection_threshold and sensors[2] > obstacle_detection_threshold and sensors[4] > obstacle_detection_threshold

# User selects either left or right wall-following mode
@event(robot.when_play)
async def play(robot):
    await robot.reset_navigation()

    # Ask the user to choose either left or right wall following
    choice = input("Choose wall-following mode (left/right): ").strip().lower()

    # Run the corresponding wall-following logic
    if choice == "left":
        await follow_left_wall(robot)
    elif choice == "right":
        await follow_right_wall(robot)
    else:
        print("Invalid choice. Please enter 'left' or 'right'.")

# Start the robot
robot.play()
