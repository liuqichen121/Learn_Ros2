#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""订阅 ROS 2 图像话题，并用 OpenCV 窗口显示摄像头画面。"""

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class CameraViewer(Node):
    """订阅 sensor_msgs/msg/Image，并将图像显示在 OpenCV 窗口中。"""

    def __init__(self, node_name='camera_viewer'):
        super().__init__(node_name)
        self.declare_parameter('window_name', 'OpenCV Camera')
        self.window_name = self.get_parameter('window_name').value

        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, 'image_raw', self._image_callback, qos_profile_sensor_data)
        self.get_logger().info('正在等待图像话题 image_raw ...')

    def _image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as exc:
            self.get_logger().error(
                f'ROS 图像消息转换为 OpenCV 图像失败：{exc}',
                throttle_duration_sec=5.0)
            return

        cv2.imshow(self.window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.get_logger().info('收到退出按键，关闭显示窗口')
            rclpy.shutdown()

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraViewer('camera_viewer')
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
