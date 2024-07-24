import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/anthonyubuntu/Desktop/inmind/session6/Anthony-Moundalak-ROS2-Assignment-Session6/ros2ws/install/warehouse_robot'
