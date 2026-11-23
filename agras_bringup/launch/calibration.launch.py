"""Agras driver + LI-Init; never starts FAST-LIO2 concurrently."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    share = get_package_share_directory('agras_bringup')
    driver = os.path.join(get_package_share_directory('livox_ros_driver2'), 'launch', 'driver.launch.py')
    calibration = os.path.join(get_package_share_directory('lidar_imu_init'), 'launch', 'agras_mid360.launch.py')
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('params_file', default_value=os.path.join(share, 'config', 'calibration.yaml')),
        DeclareLaunchArgument('output_dir', default_value=os.path.join(os.path.expanduser('~'), '.ros', 'agras', 'calibration')),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(driver), launch_arguments={'xfer_format': '4'}.items()),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(calibration), launch_arguments={
            'params_file': LaunchConfiguration('params_file'),
            'rviz': LaunchConfiguration('rviz'),
            'output_dir': LaunchConfiguration('output_dir'),
        }.items()),
    ])
