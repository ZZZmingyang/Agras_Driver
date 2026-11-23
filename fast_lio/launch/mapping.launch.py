"""FAST-LIO2 only; the caller supplies a running lidar driver."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package = get_package_share_directory('fast_lio')
    output = os.path.join(os.environ.get('ROS_HOME', os.path.expanduser('~/.ros')), 'agras', 'fast_lio2')
    return LaunchDescription([
        DeclareLaunchArgument('config_path', default_value=os.path.join(package, 'config')),
        DeclareLaunchArgument('config_file', default_value='agras_mid360.yaml'),
        DeclareLaunchArgument('params_file', default_value=PathJoinSubstitution([
            LaunchConfiguration('config_path'), LaunchConfiguration('config_file')])),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('rviz_cfg', default_value=os.path.join(package, 'rviz', 'fastlio.rviz')),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('output_dir', default_value=output),
        DeclareLaunchArgument('sensor_frame', default_value='livox_frame'),
        DeclareLaunchArgument('diag', default_value='false'),
        Node(package='fast_lio', executable='fastlio_mapping', name='fast_lio', output='screen',
             parameters=[LaunchConfiguration('params_file'), {
                 'output_dir': LaunchConfiguration('output_dir'),
                 'frames.sensor_frame': LaunchConfiguration('sensor_frame'),
                 'use_sim_time': ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool),
             }]),
        Node(package='rviz2', executable='rviz2', name='rviz2',
             arguments=['-d', LaunchConfiguration('rviz_cfg')],
             condition=IfCondition(LaunchConfiguration('rviz'))),
        Node(package='fast_lio', executable='imu_lidar_sync_diag.py', name='imu_lidar_sync_diag',
             condition=IfCondition(LaunchConfiguration('diag'))),
    ])
