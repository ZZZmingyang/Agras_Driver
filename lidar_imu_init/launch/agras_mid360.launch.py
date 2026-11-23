"""LI-Init only; agras_bringup/calibration.launch.py also starts the driver."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package = get_package_share_directory('lidar_imu_init')
    output = os.path.join(os.environ.get('ROS_HOME', os.path.expanduser('~/.ros')), 'agras', 'calibration')
    return LaunchDescription([
        DeclareLaunchArgument('params_file', default_value=os.path.join(package, 'config', 'agras_mid360.yaml')),
        DeclareLaunchArgument('output_dir', default_value=output),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        Node(package='lidar_imu_init', executable='li_init', name='lidar_imu_init', output='screen',
             parameters=[LaunchConfiguration('params_file'), {
                 'output_dir': LaunchConfiguration('output_dir'),
                 'point_filter_num': 2, 'max_iteration': 5, 'cube_side_length': 2000.0,
                 'use_sim_time': ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool),
             }]),
        Node(package='rviz2', executable='rviz2', name='rviz2',
             arguments=['-d', os.path.join(package, 'rviz_cfg', 'fast_lo.rviz')],
             condition=IfCondition(LaunchConfiguration('rviz'))),
    ])
