import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import xacro


def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')   
    use_ros2_control = LaunchConfiguration('use_ros2_control', default='true')
    package_name='sdv2_description' 
    file_subpath = os.path.join(get_package_share_directory(package_name),'rviz','sdv.rviz')

    desc_start = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','sdv2_description_rsp.launch.py'
                )]), launch_arguments={'use_sim_time': use_sim_time, 'use_ros2_control': use_ros2_control}.items()
    )

    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', file_subpath],
        parameters=[{'use_sim_time': use_sim_time}],
    )
    

    # Run the node
    return LaunchDescription([
        desc_start,
        node_rviz
    ])