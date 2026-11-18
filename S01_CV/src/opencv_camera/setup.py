import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'opencv_camera'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'README.md']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='liuqichen121',
    maintainer_email='liuqichen121@todo.todo',
    description='ROS 2 OpenCV camera publisher and viewer',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'camera_publisher = opencv_camera.camera_publisher:main',
            'camera_viewer = opencv_camera.camera_viewer:main',
        ],
    },
)
