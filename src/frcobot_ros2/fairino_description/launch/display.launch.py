#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # fairino_description paketindeki URDF dosyasını kullanın.
    package_share = get_package_share_directory('fairino_description')
    urdf_file = os.path.join(package_share, 'urdf', 'fairino20_v6.urdf')  # Kullanmak istediğiniz URDF dosyasını seçin.
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()

    return LaunchDescription([
        # robot_state_publisher node’u başlatılıyor
        Node(
            package='fairino_hardware',
            executable='ros2_cmd_server',
            name='ros2_cmd_server',
            output='screen',
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}],
            remappings=[
            ('/robot_description', '/robot_description_arm'),
            ]
        ),
        # JointStatePublisher node’unuzun bulunduğu paket ve executable ismini uygun şekilde girin.
        Node(
            package='fairino_description',  # Burayı kendi paket isminizle değiştirin.
            executable='joint_state_publisher.py',
            name='joint_state_publisher',
            output='screen',
        ),
        Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub_base_link_v5',
        arguments=['0', '0', '0.3', '0', '0', '0', '1', 'base_link', 'base_link_v20'],
        ),
        # # RViz2 node’unu başlatabilirsiniz. (Varsa hazır bir rviz konfigürasyon dosyası)
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     output='screen',
        #     arguments=['-d', os.path.join(package_share, 'rviz', 'your_config.rviz')]  # RViz konfigürasyon dosyanızı belirtin.
        # )
    ])

if __name__ == '__main__':
    generate_launch_description()
