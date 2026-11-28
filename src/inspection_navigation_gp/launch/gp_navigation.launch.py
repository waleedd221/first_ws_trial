import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

TOOLS = os.path.expanduser('~/inspection_ws/tools')

def generate_launch_description():
    gp_gazebo = get_package_share_directory('gp_gazebo')
    nav2 = get_package_share_directory('nav2_bringup')

    # 1) Robot in Gazebo (+ scan filter)
    sim = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(gp_gazebo, 'launch', 'gp_simulation.launch.py')))

    # 2) EKF: wheels (vx, vy) + IMU (yaw rate) -> odom -> base_link
    ekf = Node(package='robot_localization', executable='ekf_node',
               name='ekf_filter_node', output='screen',
               parameters=[os.path.join(TOOLS, 'ekf_gp.yaml'), {'use_sim_time': True}])

    # 3) Map + AMCL
    loc = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(TOOLS, 'gp_localization_local.launch.py')))

    # 4) Nav2 navigation only (no map_server / AMCL)
    nav = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(nav2, 'launch', 'navigation_launch.py')),
        launch_arguments={'params_file': os.path.join(TOOLS, 'nav2_params_gp.yaml'),
                          'use_sim_time': 'true', 'autostart': 'true'}.items())

    # 5) RViz with Nav2's layout
    rviz = Node(package='rviz2', executable='rviz2', output='screen',
                arguments=['-d', os.path.join(nav2, 'rviz', 'nav2_default_view.rviz')],
                parameters=[{'use_sim_time': True}])

    return LaunchDescription([
        sim,
        TimerAction(period=8.0, actions=[loc]),
        TimerAction(period=12.0, actions=[nav, rviz]),
    ])
