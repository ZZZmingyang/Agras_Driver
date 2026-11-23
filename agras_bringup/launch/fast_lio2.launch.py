"""Agras driver + FAST-LIO2; algorithm launch owns the optional RViz."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    share = get_package_share_directory('agras_bringup')
    driver = os.path.join(get_package_share_directory('livox_ros_driver2'), 'launch', 'driver.launch.py')
    mapping = os.path.join(get_package_share_directory('fast_lio'), 'launch', 'mapping.launch.py')
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('params_file', default_value=os.path.join(share, 'config', 'fast_lio2.yaml')),
        DeclareLaunchArgument('output_dir', default_value=os.path.join(os.path.expanduser('~'), '.ros', 'agras', 'fast_lio2')),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(driver), launch_arguments={'xfer_format': '4'}.items()),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(mapping), launch_arguments={
            'params_file': LaunchConfiguration('params_file'),
            'rviz': LaunchConfiguration('rviz'),
            'rviz_cfg': os.path.join(share, 'rviz', 'fast_lio2.rviz'),
            'output_dir': LaunchConfiguration('output_dir'),
            'sensor_frame': LaunchConfiguration('frame_id'),
        }.items()),
    ])
