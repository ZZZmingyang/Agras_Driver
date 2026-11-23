"""Agras driver only. Format 4 publishes CustomMsg and PointCloud2 once per frame."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package = get_package_share_directory('livox_ros_driver2')
    arguments = [
        DeclareLaunchArgument('config', default_value=os.path.join(package, 'config', 'AGRAS_MID360_config.json')),
        DeclareLaunchArgument('xfer_format', default_value='4', description='0=PointCloud2, 1=CustomMsg, 4=both'),
        DeclareLaunchArgument('frame_id', default_value='livox_frame'),
        DeclareLaunchArgument('publish_freq', default_value='20.0',
                              description='Target cloud publication rate; built-in IMU stays at its native rate'),
        DeclareLaunchArgument('ext_imu', default_value='false'),
        DeclareLaunchArgument('ext_imu_port', default_value='/dev/ttyIMU'),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
    ]
    driver = Node(
        package='livox_ros_driver2', executable='livox_ros_driver2_node',
        name='livox_lidar_publisher', output='screen',
        parameters=[{
            'user_config_path': LaunchConfiguration('config'),
            'xfer_format': ParameterValue(LaunchConfiguration('xfer_format'), value_type=int),
            'publish_freq': ParameterValue(LaunchConfiguration('publish_freq'), value_type=float),
            'frame_id': LaunchConfiguration('frame_id'),
            'ext_imu_enable': ParameterValue(LaunchConfiguration('ext_imu'), value_type=bool),
            'ext_imu_port': LaunchConfiguration('ext_imu_port'),
            'ext_imu_frame_id': LaunchConfiguration('frame_id'),
            'ext_imu_publish_rate': 500.0,
            'use_sim_time': ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool),
            'multi_topic': 0, 'data_src': 0, 'output_data_type': 0,
        }])
    return LaunchDescription(arguments + [driver])
