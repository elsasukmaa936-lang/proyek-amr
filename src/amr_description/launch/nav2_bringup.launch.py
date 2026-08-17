import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    amr_description_pkg = get_package_share_directory('amr_description')
    nav2_bringup_pkg = get_package_share_directory('nav2_bringup')

    params_file = os.path.join(amr_description_pkg, 'config', 'nav2_params.yaml')
    map_file = '/home/amr/amr_ws/maps/ruangan_pertama.yaml'

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

    return LaunchDescription([nav2_launch])
