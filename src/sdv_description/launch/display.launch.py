import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    package_name = 'sdv_description'
    pkg_share = get_package_share_directory(package_name)

    fairino_share_dir = get_package_share_directory('fairino_description')
    # display.launch.py dosyasının tam yolunu oluşturuyoruz
    display_launch_file = os.path.join(fairino_share_dir, 'launch', 'display.launch.py')

    # xacro dosyasının yolu
    xacro_file = os.path.join(pkg_share, 'urdf', 'devna.urdf.xacro')
    robot_description = {'robot_description': Command(['xacro ', xacro_file])}

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
    )

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
        remappings=[('/robot_description', '/robot_description')]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_share, 'rviz', 'default.rviz')]
    )

    display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(display_launch_file)
    )

    # Bu aksiyonu 3 saniye sonra çalıştırmak için TimerAction kullanıyoruz:
    display_launch_delayed = TimerAction(
        period=3.0,  # 3 saniye gecikme
        actions=[display_launch]
    )

    return LaunchDescription([
        rsp_node,
        joint_state_publisher_node,
        rviz_node,
        display_launch_delayed
    ])
