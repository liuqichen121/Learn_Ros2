#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""启动 OpenCV 摄像头发布节点，可选同时启动图像显示节点。"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    device = LaunchConfiguration('device')
    fps = LaunchConfiguration('fps')
    width = LaunchConfiguration('width')
    height = LaunchConfiguration('height')
    frame_id = LaunchConfiguration('frame_id')
    image_topic = LaunchConfiguration('image_topic')
    viewer = LaunchConfiguration('viewer')

    return LaunchDescription([
        DeclareLaunchArgument(
            'device', default_value='/dev/video0',
            description='摄像头设备路径或索引，例如 /dev/video0 或 0'),
        DeclareLaunchArgument(
            'fps', default_value='30.0',
            description='摄像头采集和发布帧率'),
        DeclareLaunchArgument(
            'width', default_value='640',
            description='期望的图像宽度（像素）'),
        DeclareLaunchArgument(
            'height', default_value='480',
            description='期望的图像高度（像素）'),
        DeclareLaunchArgument(
            'frame_id', default_value='camera_link',
            description='图像消息的坐标系名称'),
        DeclareLaunchArgument(
            'image_topic', default_value='image_raw',
            description='发布的图像话题名称'),
        DeclareLaunchArgument(
            'viewer', default_value='false',
            description='是否同时启动 OpenCV 显示窗口（true/false）'),

        Node(
            package='opencv_camera',
            executable='camera_publisher',
            name='camera_publisher',
            output='screen',
            parameters=[{
                'device': ParameterValue(device, value_type=str),
                'fps': ParameterValue(fps, value_type=float),
                'width': ParameterValue(width, value_type=int),
                'height': ParameterValue(height, value_type=int),
                'frame_id': ParameterValue(frame_id, value_type=str),
            }],
            remappings=[('image_raw', image_topic)],
        ),

        Node(
            package='opencv_camera',
            executable='camera_viewer',
            name='camera_viewer',
            output='screen',
            condition=IfCondition(viewer),
            remappings=[('image_raw', image_topic)],
        ),
    ])
