
# iRobot Create3 Wall Following and Obstacle Avoidance Program

## Overview

This project controls an iRobot Create3 to autonomously navigate an environment using wall-following behavior while avoiding obstacles. The robot will follow walls, make turns when necessary, and navigate toward an endpoint. It also plays a song when the task is completed.

The program makes use of the `irobot_edu_sdk` library, allowing interaction with the iRobot Create3 robot via Bluetooth. The robot uses its proximity sensors to detect walls and obstacles and makes decisions to navigate through the environment.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [How It Works](#how-it-works)
  - [Sensors and Thresholds](#sensors-and-thresholds)
  - [Movement Functions](#movement-functions)
  - [Bump Event Handling](#bump-event-handling)
  - [Music Playback](#music-playback)
  - [Navigation Logic](#navigation-logic)
- [How to Run](#how-to-run)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the required dependencies for running this project, ensure you have:

- Python 3.8 or above
- `irobot_edu_sdk` for interacting with the Create3 robot

You can install the required Python package using pip:

```bash
pip install irobot-edu-sdk
```

## How It Works

### Sensors and Thresholds

The robot uses its infrared (IR) proximity sensors to detect obstacles and walls. The following thresholds control its behavior:

- **Left Wall Threshold (`th_wall`)**: The minimum sensor value that indicates a wall is present on the left side. The robot will follow this wall.
- **Obstacle Threshold (`th_obstacle`)**: The minimum sensor value for detecting obstacles in front of the robot.
- **Right Wall Detection (`th_wall_left`)**: A threshold for detecting the left wall when it gets too close to the wall.

### Movement Functions

The following functions define the robot's movement:

- `move_forward(robot)`: Moves the robot straight ahead.
- `turn_left(robot)`: Makes a slight left turn when moving away from the wall.
- `turn_right(robot)`: Makes a 90-degree right turn when an obstacle is detected.
- `escape_left_turn_right(robot)`: Adjusts the robot's direction when it gets too close to the left wall.

### Bump Event Handling

The program includes bump event handling to manage collisions:

- `bumped_Right(robot)`: Triggered when the right bumper is hit. The robot backs up and turns left.
- `bumped_Left(robot)`: Triggered when the left bumper is hit. The robot backs up and turns right.

### Music Playback

When the robot reaches its endpoint, it plays a series of notes as a song:

```python
notes = [
    (440, 0.5),  # A4
    (493.88, 0.5),  # B4
    (523.25, 0.5),  # C5
    (493.88, 1.0),  # B4
]
```

### Navigation Logic

The main navigation logic is handled in the `play` function:

1. The robot continuously moves forward while following walls.
2. If an obstacle is detected, the robot turns right.
3. If no left wall is detected, the robot turns left.
4. If the robot reaches the predefined endpoint, it stops and plays a song.

The robot's current position is recorded using the `get_position` function, and its proximity sensors are read to detect obstacles and walls.

## How to Run

1. Ensure your Create3 robot is powered on and connected via Bluetooth.
2. Run the Python script:

```bash
python create3_wall_following.py
```

3. The robot will begin navigating its environment. Once it reaches the endpoint, it will stop and play a song.

## Contributing

Feel free to contribute by submitting a pull request or reporting issues. Any improvements to navigation efficiency, obstacle handling, or additional features are welcome.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.
