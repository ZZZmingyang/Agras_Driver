"""One driver and one RViz, displaying the PointCloud2 side of dual output."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('agras_bringup')
    driver = os.path.join(get_package_share_directory('livox_ros_driver2'), 'launch', 'driver.launch.py')
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('rviz_config', default_value=os.path.join(share, 'rviz', 'pointcloud.rviz')),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(driver), launch_arguments={'xfer_format': '4'}.items()),
        # A viewer-local reference only; SLAM launches publish their own estimated TF.
        Node(package='tf2_ros', executable='static_transform_publisher',
             arguments=['--frame-id', 'view_origin', '--child-frame-id', LaunchConfiguration('frame_id')],
             condition=IfCondition(LaunchConfiguration('rviz'))),
        Node(package='rviz2', executable='rviz2', name='rviz2',
             arguments=['-d', LaunchConfiguration('rviz_config'), '-f', LaunchConfiguration('frame_id')],
             condition=IfCondition(LaunchConfiguration('rviz'))),
    ])
