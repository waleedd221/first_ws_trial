#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    gp_test_pkg = get_package_share_directory('gp_test')
    gp_gazebo_pkg = get_package_share_directory('gp_gazebo')

    # Lets Gazebo resolve model://simple_building
    set_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.path.join(gp_gazebo_pkg, 'models') + ':' +
              os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    )

    robot_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gp_test_pkg, 'launch', 'robot_description.launch.py')
        )
    )

    robot_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gp_gazebo_pkg, 'launch', 'gp_home.launch.py')
        )
    )

    robot_spawner = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gp_gazebo_pkg, 'launch', 'spawn.launch.py')
        )
    )

    ld = LaunchDescription()

    ld.add_action(set_resource_path)   
    ld.add_action(robot_description)
    ld.add_action(robot_world)
    ld.add_action(robot_spawner)

    return ld