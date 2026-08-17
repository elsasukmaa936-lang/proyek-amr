import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    amr_description_pkg = get_package_share_directory('amr_description')
    sllidar_pkg = get_package_share_directory('sllidar_ros2')
    nav2_bringup_pkg = get_package_share_directory('nav2_bringup')

    params_file = os.path.join(amr_description_pkg, 'config', 'nav2_params.yaml')
    map_file = '/home/amr/amr_ws/maps/ruangan_pertama.yaml'

    # 1. Motor + STM32
    base_control = Node(
        package='base_control_ros2',
        executable='base_control_node',
        name='base_control',
        output='screen'
    )

    # 2. Lidar
    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sllidar_pkg, 'launch', 'sllidar_a1_launch.py')
        ),
        launch_arguments={
            'serial_port': '/dev/rplidar',
            'frame_id': 'laser_link'
        }.items()
    )

    # 3. URDF / TF
    description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(amr_description_pkg, 'launch', 'description.launch.py')
        )
    )

    # 4. Nav2 (localization + planner + controller) - GANTI dari slam_toolbox
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_pkg, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': 'false',
            'autostart': 'true'
        }.items()
    )

    return LaunchDescription([
        base_control,
        lidar_launch,
        description_launch,
        nav2_launch,
    ])