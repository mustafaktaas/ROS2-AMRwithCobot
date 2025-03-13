import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.actions import SetEnvironmentVariable, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    package_name = 'sdv_gazebo'
    # sdv_description paketinden robot modelinizin bulunduğu dizini alın
    pkg_description = get_package_share_directory('sdv_description')
    # Robotunuzun xacro dosyasının yolu (örneğin devna.urdf.xacro)
    xacro_file = os.path.join(pkg_description, 'urdf', 'devna.urdf.xacro')

    # Robot URDF'sini xacro komutu ile üretip /robot_description konusuna parametre olarak aktarın
    robot_description = {'robot_description': Command(['xacro ', xacro_file])}

    #  Mesh dosyalarınızın bulunduğu dizin (örneğin: urdf/meshes)
    meshes_path = os.path.join('/home/developer/ros2_ws/src/sdv_description/urdf/meshes')

    set_gazebo_model_path = SetEnvironmentVariable('GAZEBO_MODEL_PATH', meshes_path)

    gazebo_params_file = os.path.join('/home/developer/ros2_ws/src/sdv_gazebo/params/gazebo_params.yaml')

    # # Gazebo simülatörünü başlatan node (gzserver)
    # gazebo_server = Node(
    #     package='gazebo_ros',
    #     executable='/usr/bin/gzserver',
    #     output='screen',
    #     arguments=['-s', 'libgazebo_ros_factory.so']  # Factory plugin, spawn işlemi için gereklidir
    # )

    # # Opsiyonel: Gazebo istemcisini (GUI) başlatan node
    # gazebo_client = Node(
    #     package='gazebo_ros',
    #     executable='/usr/bin/gzclient',
    #     output='screen'
    # )

        # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
        remappings=[('/robot_description', '/robot_description')]
    )

    # Robotu Gazebo ortamına spawn eden node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'devna',  # Robotunuzun Gazebo’daki ismi
            '-topic', '/robot_description'
        ],
        output='screen'
    )

    spawn_entity_delay = TimerAction(
        period=5.0,
        actions=[spawn_entity]
    )

    return LaunchDescription([
        set_gazebo_model_path,
        robot_state_publisher,
        # gazebo_server,
        # gazebo_client,
        gazebo,
        spawn_entity,
        # robot_state_publisher,
        joint_state_publisher_node,
        # Robot modelinin tanımlandığı parametreyi robot_state_publisher'ın da çalıştığı sdv_description paketi tarafından yayınlanması gerekiyor.
        # Eğer sdv_description paketinde robot_state_publisher çalışıyorsa, onu ayrı bir launch dosyasında çalıştırıp
        # /robot_description konusunu sağladığından emin olun.
    ])
