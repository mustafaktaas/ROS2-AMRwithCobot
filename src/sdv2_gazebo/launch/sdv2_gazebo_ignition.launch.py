import os
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node, SetParameter
from launch.substitutions import LaunchConfiguration
import xacro


def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')   
    package_name='sdv2_description' 
    pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
    pkg_sdv2_gazebo = get_package_share_directory('sdv2_gazebo')
    
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','sdv2_description.launch.py'
                )]), launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py'),
        ),
    )
    
    gz_spawn_entity = Node(
        package="ros_ign_gazebo",
        executable="create",
        output="screen",
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'sdv',
            "-name",
            "sdv",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "0",
        ]
    )

    bridge = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        output='screen'
    )
    
# "-file", "/home/developer/sdv_ws/src/sdv2_description/urdf/sdv.urdf.xacro",

    return LaunchDescription([
        DeclareLaunchArgument(
          'ign_args',
          default_value=[os.path.join(pkg_sdv2_gazebo, 'world', 'fuel_preview.sdf') +
                         ' -v 2 --gui-config '],
          description='Ignition Gazebo arguments'),
        rsp,
        gz_spawn_entity,
        bridge,
        gazebo
    ])