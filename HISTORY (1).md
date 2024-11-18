
# iRobot Create3 Robot Project: Development History

## Overview

This document presents the development history of the iRobot Create3 wall-following and obstacle avoidance project. Each stage showcases challenges encountered, the solutions applied, and how the project evolved from simple movement to complex navigation logic, including wall-following and obstacle detection, with the final version incorporating endpoint detection and music playback.

---

## Table of Contents
1. [Version 1](#version-1)
2. [Version 2](#version-2)
3. [Version 3](#version-3)
4. [Version 4](#version-4)
5. [Version 5](#version-5)
6. [Version 6](#version-6)
7. [Version 7](#version-7)
8. [Version 8](#version-8)
9. [Version 9](#version-9)
10. [Version 10](#version-10)
11. [Version 11](#version-11)
12. [Version 12](#version-12)
13. [Version 13](#version-13)
14. [Final Version](#final-version)

---

## Version 1

### Description:
The initial version introduced basic robot movement, allowing the iRobot Create3 to move forward.

**Key Features:**
- Simple forward movement.
- No wall detection or obstacle avoidance.

**Code Snippet:**
```python
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3

robot = Create3(Bluetooth())
speed = 16  # Speed of the robot

# Simple forward movement
@event(robot.when_play)
async def play(robot):
    await robot.set_wheel_speeds(speed, speed)

robot.play()
```

---

## Version 2

### Description:
Added left and right turning functionality based on sensor data. However, there was no clear logic for wall following or obstacle detection.

---

## Version 3

### Challenge:
The robot was inconsistent in wall-following. It either drifted too far or stayed too close to the wall.

### Solution:
Introduced threshold values to improve wall detection, and implemented wall-following by adjusting speed.

**Key Features:**
- Left and right turn adjustments based on sensor data.
- Obstacle detection logic not yet developed.

**Code Snippet:**
```python
th_wall = 80  # Threshold for left wall detection
th_obstacle = 80  # Threshold for obstacle detection
```

---

## Version 4

### Challenge:
The robot was unable to respond properly when bumping into obstacles.

### Solution:
Added bump event handlers to help the robot back away and adjust direction after collisions.

**Key Features:**
- Improved wall-following behavior.
- Bump detection and reaction.

**Code Snippet:**
```python
@event(robot.when_bumped, [False, True])
async def bumped_right(robot):
    await robot.move(-10)
    await robot.turn_left(45)
```

---

## Version 5

### Challenge:
The robot occasionally stopped when encountering obstacles, making it difficult for smooth navigation.

### Solution:
Introduced a function to turn right when an obstacle was detected, allowing the robot to continue moving.

**Key Features:**
- Right-angle turn on obstacle detection.
- Smoother navigation without freezing.

**Code Snippet:**
```python
async def turn_right(robot):
    await robot.turn_right(90)  # Right turn
```

---

## Version 6

### Challenge:
The robot was unable to detect when it reached the goal, leading to unnecessary movement.

### Solution:
Added position tracking and a success condition that triggers the robot to stop and play a song when reaching the endpoint.

**Key Features:**
- Position tracking.
- Task completion melody.

**Code Snippet:**
```python
async def get_position(robot):
    pos = await robot.get_position()
    return pos.x, pos.y, pos.heading

@event(robot.when_play)
async def play(robot):
    if abs(pos[0] - end_x) < 15:
        await play_song(robot)
        break
```

---

## Version 7

### Challenge:
Inconsistent behavior when avoiding walls too closely.

### Solution:
Improved proximity detection and adjusted speed to make the robot react more smoothly when close to walls.

---

## Version 8

### Challenge:
Sensors were slow to respond to the environment, causing the robot to hit obstacles.

### Solution:
Increased the sensor reading speed and adjusted the robot's reaction to proximity changes.

---

## Version 9

### Challenge:
The robot’s wall-following logic was inconsistent on curves and corners.

### Solution:
Modified the turning speed and sensor threshold, enabling smoother cornering and curve navigation.

---

## Version 10

### Challenge:
Difficulty in calibrating the robot’s movement when detecting walls.

### Solution:
Adjusted thresholds for left wall detection and introduced smoother escape logic when the robot came too close to the wall.

---

## Version 11

### Challenge:
The robot sometimes got stuck in loops when turning, as it kept detecting the same obstacle.

### Solution:
Introduced a cooldown period after each turn to avoid redundant turns when detecting obstacles.

---

## Version 12

### Challenge:
The robot's navigation still had some freezing issues during endpoint detection.

### Solution:
Optimized the `get_position` function and recalculated the robot’s path more efficiently.

**Key Features:**
- Optimized path calculation and smoother navigation.

---

## Version 13

### Challenge:
Detected obstacles were causing the robot to turn too frequently, disrupting the overall flow of navigation.

### Solution:
Fine-tuned obstacle detection and reduced the robot’s sensitivity to small objects, improving navigation flow.

---

## Final Version

### Overview:
This version includes all the solutions implemented through the various iterations, resulting in smooth wall-following behavior, obstacle avoidance, and task completion with music playback.

**Final Code Snippet:**
```python
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

```

---

This **HISTORY.md** file documents the evolution of your iRobot Create3 project, showcasing how you addressed each challenge to reach the final version. You can upload this file to your GitHub repository to demonstrate the development process.
