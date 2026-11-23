"""One driver; built-in IMU; optional RViz. No SLAM or serial devices."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package = get_package_share_directory('livox_ros_driver2')
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='false'),
        DeclareLaunchArgument('config', default_value=os.path.join(
            package, 'config', 'AGRAS_MID360_config.json')),
        Node(
            package='livox_ros_driver2', executable='livox_ros_driver2_node',
            name='livox_lidar_publisher', output='screen',
            parameters=[{
                'xfer_format': 0, 'multi_topic': 0, 'data_src': 0,
                'publish_freq': 10.0, 'output_data_type': 0,
                'frame_id': 'livox_frame', 'ext_imu_enable': False,
                'user_config_path': LaunchConfiguration('config'),
                'cmdline_input_bd_code': 'livox0000000001',
            }]),
        Node(
            package='tf2_ros', executable='static_transform_publisher',
            arguments=['--frame-id', 'map', '--child-frame-id', 'livox_frame'],
            condition=IfCondition(LaunchConfiguration('rviz'))),
        Node(
            package='rviz2', executable='rviz2',
            arguments=['-d', os.path.join(package, 'config', 'agras_minimal.rviz')],
            condition=IfCondition(LaunchConfiguration('rviz'))),
    ])
