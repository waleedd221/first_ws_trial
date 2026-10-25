import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    nav2_dir = get_package_share_directory('nav2_bringup')
    my_dir = get_package_share_directory('inspection_navigation')          # NEW
    params = os.path.join(my_dir, 'config', 'nav2_params.yaml')            # NEW

    headless = LaunchConfiguration('headless')

    declare_headless = DeclareLaunchArgument(
        'headless', default_value='False',
        description='Run Gazebo without its window')

    sim_and_nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_dir, 'launch', 'tb3_simulation_launch.py')),
        launch_arguments={'headless': headless,
                          'params_file': params}.items())                  # NEW

    patrol = Node(
        package='inspection_navigation',
        executable='patrol',
        output='screen',
        parameters=[{'use_sim_time': True}])

    return LaunchDescription([declare_headless, sim_and_nav, patrol])