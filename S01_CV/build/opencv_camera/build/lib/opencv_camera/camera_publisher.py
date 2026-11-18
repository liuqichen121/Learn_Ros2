#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""使用 OpenCV 采集摄像头图像，并以 ROS 2 图像话题发布的节点。"""

import sys
import time

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class CameraPublisher(Node):
    """读取摄像头画面并发布 sensor_msgs/msg/Image 消息。"""

    def __init__(self, node_name='camera_publisher'):
        super().__init__(node_name)

        # 节点参数：可通过命令行或 launch 文件覆盖
        self.declare_parameter('device', '/dev/video0')
        self.declare_parameter('fps', 30.0)
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)
        self.declare_parameter('frame_id', 'camera_link')

        self.device = self.get_parameter('device').value
        self.fps = max(float(self.get_parameter('fps').value), 1.0)
        self.width = int(self.get_parameter('width').value)
        self.height = int(self.get_parameter('height').value)
        self.frame_id = self.get_parameter('frame_id').value

        self.bridge = CvBridge()
        self.cap = None
        self._read_failures = 0
        self._last_open_attempt = 0.0
        self._frame_count = 0

        # 图像话题使用 SensorDataQoS，便于与 rqt_image_view、rviz2 等工具配合
        self.publisher = self.create_publisher(
            Image, 'image_raw', qos_profile_sensor_data)
        self.timer = self.create_timer(1.0 / self.fps, self._timer_callback)

        self._open_camera()

    def _open_camera(self):
        """打开摄像头并设置分辨率/帧率，失败时返回 False 供下次重试。"""
        self._last_open_attempt = time.monotonic()

        # 数字形式的 device（如 "0"）按摄像头索引打开，否则按设备路径打开
        device = int(self.device) if str(self.device).isdigit() else self.device
        backend = cv2.CAP_V4L2 if sys.platform.startswith('linux') else cv2.CAP_ANY

        cap = cv2.VideoCapture(device, backend)
        if not cap.isOpened() and backend != cv2.CAP_ANY:
            cap.release()
            cap = cv2.VideoCapture(device)

        if not cap.isOpened():
            cap.release()
            self.get_logger().error(
                f'无法打开摄像头 {self.device!r}，请检查设备连接和权限',
                throttle_duration_sec=5.0)
            return False

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.fps)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.cap = cap
        self._read_failures = 0
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = cap.get(cv2.CAP_PROP_FPS)
        self.get_logger().info(
            f'摄像头已打开：{self.device}，{actual_width}x{actual_height} @ {actual_fps:.1f} FPS')
        return True

    def _timer_callback(self):
        if self.cap is None or not self.cap.isOpened():
            # 摄像头未就绪时每秒重试一次，避免刷屏或阻塞执行器
            if time.monotonic() - self._last_open_attempt >= 1.0:
                self._open_camera()
            return

        ok, frame = self.cap.read()
        if not ok or frame is None:
            self._read_failures += 1
            if self._read_failures >= 5:
                self.get_logger().warn(
                    '连续读取摄像头失败，正在尝试重新连接',
                    throttle_duration_sec=5.0)
                self.cap.release()
                self.cap = None
                self._last_open_attempt = 0.0
            return

        self._read_failures = 0

        try:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        except Exception as exc:  # cv_bridge 转换异常不应终止节点
            self.get_logger().error(
                f'图像转换为 ROS 消息失败：{exc}', throttle_duration_sec=5.0)
            return

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        self.publisher.publish(msg)

        self._frame_count += 1
        if self._frame_count == 1:
            self.get_logger().info('已开始发布图像话题 image_raw')
        elif self._frame_count % 150 == 0:
            self.get_logger().info(
                f'已发布 {self._frame_count} 帧图像',
                throttle_duration_sec=5.0)

    def destroy_node(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher('camera_publisher')
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
