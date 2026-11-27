
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # Get the converted SDF file
    sdf_path = os.path.join(
        get_package_share_directory('dummybot_description'),
        'urdf',
        'dummybot.sdf'
    )

    # Launch configuration variables
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    robot_name = LaunchConfiguration('robot_name')

    # Declare launch arguments
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose',
        default_value='0.0',
        description='Specify x position of the robot'
    )

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose',
        default_value='0.0',
        description='Specify y position of the robot'
    )

    declare_robot_name_cmd = DeclareLaunchArgument(
        'robot_name',
        default_value='dummybot',
        description='Specify the name of the robot'
    )

    # Spawn robot directly from SDF instead of robot_description
    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', robot_name,
            '-file', sdf_path,
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.5'
        ],
        output='screen',
    )

    # ROS-Gazebo bridge
    bridge_params = os.path.join(
        get_package_share_directory('dummybot_gazebo'),
        'config',
        'bridge.yaml'
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen',
    )

    ld = LaunchDescription()

    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)
    ld.add_action(declare_robot_name_cmd)

    ld.add_action(start_gazebo_ros_spawner_cmd)
    ld.add_action(start_gazebo_ros_bridge_cmd)

    return ld
