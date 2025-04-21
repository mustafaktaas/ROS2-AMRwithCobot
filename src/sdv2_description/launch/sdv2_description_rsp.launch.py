import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration,Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro


def generate_launch_description():
  
    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'sdv2_description'
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')   
    file_subpath = os.path.join(get_package_share_directory(pkg_name),'urdf','sdv.urdf.xacro')
    use_ros2_control = LaunchConfiguration("use_ros2_control", default='true')

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = Command(['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control])

    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw, 'use_sim_time': use_sim_time}] # add other parameters here if required
    )

    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen',
        parameters=[{'source_list': ['/joint_states'],'use_sim_time': use_sim_time}] # add other parameters here if required
    )
    
    sdv2_diff_drive_controller_spawn = Node(
      package="controller_manager",
      executable="spawner",
      arguments=["sdv2_diff_drive_controller"]
      )

    joint_state_broadcaster_spawn = Node(
      package="controller_manager",
      executable="spawner",
      arguments=["joint_state_broadcaster"]
        )
    
    # Run the node
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2 control if true.'),
        node_robot_state_publisher,
        node_joint_state_publisher,
        sdv2_diff_drive_controller_spawn,
        joint_state_broadcaster_spawn
    ])