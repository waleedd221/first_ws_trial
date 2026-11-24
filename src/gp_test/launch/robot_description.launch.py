import os
from ament_index_python.packages import (get_package_prefix, get_package_share_directory)
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    package_description = 'gp_test'

    pkg_share = get_package_share_directory(package_description)
    
    # Set the Path to Robot Mesh Models for Loading in Gazebo Sim
    
    install_description_dir_path = get_package_prefix(package_description) + "/share"

    if "GZ_SIM_RESOURCE_PATH" in os.environ:
        if install_description_dir_path not in os.environ["GZ_SIM_RESOURCE_PATH"]:
            os.environ["GZ_SIM_RESOURCE_PATH"] += (':' + install_description_dir_path)
    else:
        os.environ["GZ_SIM_RESOURCE_PATH"] = (':'.join(install_description_dir_path))

    urdf_path = os.path.join(pkg_share,'urdf','gp_test.xacro')

    robot_description= ParameterValue(

        Command(['xacro ', urdf_path]),
        value_type=str
    )

    robot_state_publisher_node= Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description}]
    )


    return LaunchDescription([

        robot_state_publisher_node
    ])