# Anthony-Moundalak-ROS2-Assignment-Session6

## Warehouse Robot System with Actions and Services

This ROS2 packages simulate a warehouse robot
system where the robot can deliver items and check stock levels dynamically.
- `item_delivery_action_server`: Handles item delivery requests
- `stock_checker_service_server`: Checks the stock level of a requested item
- `item_delivery_action_client`: Sends delivery requests to the action server
- `stock_checker_service_client`: Sends stock check requests to the service server

## Build and Run

1. Clone this repository

2. Build the packages and source your terminal and launch the launcher file with these command

```sh
colcon build
source install/setup.bash
ros2 launch warehouse_robot warehouse_robot_launch.py
```