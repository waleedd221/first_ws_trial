import math
import os
import yaml
import rclpy

from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from ament_index_python.packages import get_package_share_directory

TIMEOUT_S = 30  # give up on a station after 30 sec


def make_pose(nav, x, y, yaw):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = nav.get_clock().now().to_msg()
    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def main():
    rclpy.init()
    nav = BasicNavigator()

    path = os.path.join(get_package_share_directory('inspection_navigation'),
                        'config', 'stations.yaml')
    with open(path) as f:
        cfg = yaml.safe_load(f)

    s = cfg['start']
    nav.setInitialPose(make_pose(nav, s['x'], s['y'], s['yaw']))
    nav.waitUntilNav2Active()

    results = []
    for st in cfg['stations']:
        nav.get_logger().info(f"Going to {st['name']}")
        nav.goToPose(make_pose(nav, st['x'], st['y'], st['yaw']))

        while not nav.isTaskComplete():
            fb = nav.getFeedback()
            if fb and Duration.from_msg(fb.navigation_time) > Duration(seconds=TIMEOUT_S):
                nav.get_logger().warn(f"{st['name']}: timeout, cancelling")
                nav.cancelTask()

        result = nav.getResult()
        ok = result == TaskResult.SUCCEEDED
        results.append((st['name'], 'SUCCEEDED' if ok else str(result)))
        nav.get_logger().info(f"{st['name']}: {results[-1][1]}")

    nav.get_logger().info(f"Patrol finished: {results}")
    rclpy.shutdown()


if __name__ == '__main__':
    main()