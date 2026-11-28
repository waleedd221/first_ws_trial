import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    gp_gazebo = get_package_share_directory('gp_gazebo')
    nav2 = get_package_share_directory('nav2_bringup')
    this_pkg = get_package_share_directory('inspection_navigation_gp')

    # 1) Robot in Gazebo (+ scan filter + EKF, from gp_gazebo)
    sim = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(gp_gazebo, 'launch', 'gp_simulation.launch.py')))

    # 2) Map + AMCL (settings and map from gp_localization)
    loc = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(this_pkg, 'launch', 'gp_localization.launch.py')))

    # 3) Nav2 navigation only (no map_server / AMCL)
    nav = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(nav2, 'launch', 'navigation_launch.py')),
        launch_arguments={'params_file': os.path.join(this_pkg, 'config', 'nav2_params.yaml'),
                          'use_sim_time': 'true', 'autostart': 'true'}.items())

    # 4) RViz with Nav2's layout
    rviz = Node(package='rviz2', executable='rviz2', output='screen',
                arguments=['-d', os.path.join(nav2, 'rviz', 'nav2_default_view.rviz')],
                parameters=[{'use_sim_time': True}])

    return LaunchDescription([
        sim,
        TimerAction(period=8.0, actions=[loc]),
        TimerAction(period=12.0, actions=[nav, rviz]),
    ])
