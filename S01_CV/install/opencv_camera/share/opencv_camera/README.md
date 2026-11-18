# opencv_camera

基于 **OpenCV** 的 ROS 2 摄像头功能包。它使用 `cv2.VideoCapture` 采集摄像头画面，
通过 `cv_bridge` 转换成 `sensor_msgs/msg/Image` 消息后发布；任何节点都可以订阅该
话题，例如本包自带的 `camera_viewer`、`rqt_image_view` 或 `rviz2`。

## 功能

- `camera_publisher`：打开摄像头并把图像发布到 `image_raw`（默认）
- `camera_viewer`：订阅 `image_raw`，使用 OpenCV 窗口显示画面（按 `q` 退出）
- `camera.launch.py`：一次启动发布节点，可选同时启动显示节点
- 摄像头打不开或读取失败时自动重试，不会直接崩溃

## 目录结构

```text
S01_CV/src/opencv_camera/
├── launch/camera.launch.py          # 启动文件
├── opencv_camera/
│   ├── camera_publisher.py          # 摄像头图像发布节点
│   └── camera_viewer.py             # 图像订阅/显示节点
├── resource/opencv_camera
├── package.xml
├── setup.cfg
└── setup.py
```

## 环境依赖

- ROS 2（当前环境为 `lyrical`）
- `rclpy`、`sensor_msgs`、`cv_bridge`
- OpenCV Python：`cv2`（当前环境为 4.10.0）
- 摄像头设备，例如 `/dev/video0`

检查摄像头是否可用：

```bash
ls /dev/video*
python3 -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened()); cap.release()"
```

## 编译

```bash
source /opt/ros/lyrical/setup.bash
cd ~/Learn_Ros2/S01_CV
colcon build --packages-select opencv_camera
source install/setup.bash
```

每次打开新终端运行节点前，都需要 source 工作空间：

```bash
source /opt/ros/lyrical/setup.bash
source ~/Learn_Ros2/S01_CV/install/setup.bash
```

## 运行

### 1. 发布会话（摄像头内容）

```bash
ros2 run opencv_camera camera_publisher
```

默认参数：`device=/dev/video0`、`fps=30.0`、`width=640`、`height=480`。
可通过 ROS 参数覆盖：

```bash
ros2 run opencv_camera camera_publisher --ros-args \
  -p device:=/dev/video1 \
  -p fps:=15.0 \
  -p width:=1280 \
  -p height:=720 \
  -p frame_id:=camera_link
```

查看话题：

```bash
ros2 topic list
ros2 topic info /image_raw
ros2 topic hz /image_raw
ros2 topic echo /image_raw --once
```

### 2. 订阅并显示

在另一个终端中运行：

```bash
ros2 run opencv_camera camera_viewer
```

也可以使用 ROS 2 自带的图像查看工具：

```bash
ros2 run rqt_image_view rqt_image_view /image_raw
```

### 3. 使用 launch 文件

只启动摄像头发布节点：

```bash
ros2 launch opencv_camera camera.launch.py
```

同时启动发布与显示窗口：

```bash
ros2 launch opencv_camera camera.launch.py viewer:=true
```

指定设备、分辨率与话题名：

```bash
ros2 launch opencv_camera camera.launch.py \
  device:=/dev/video0 fps:=15.0 width:=1280 height:=720 \
  image_topic:=camera/image_raw viewer:=true
```

## 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `device` | `/dev/video0` | 摄像头设备路径；也可填写索引，如 `0` |
| `fps` | `30.0` | 采集/发布帧率 |
| `width` | `640` | 期望图像宽度 |
| `height` | `480` | 期望图像高度 |
| `frame_id` | `camera_link` | 图像消息的坐标系 |
| `window_name` | `OpenCV Camera` | 显示节点窗口标题（仅 `camera_viewer`） |

## 话题

| 话题 | 类型 | 方向 | 说明 |
| --- | --- | --- | --- |
| `image_raw` | `sensor_msgs/msg/Image` | 发布 | 摄像头原始图像，编码为 `bgr8` |
| `image_raw` | `sensor_msgs/msg/Image` | 订阅 | `camera_viewer` 订阅并显示 |

图像话题使用 `SensorDataQoS`（best effort），订阅端也使用相同的 QoS，
与 `rqt_image_view`、`rviz2` 等常用工具兼容。

## 常见问题

- **提示无法打开摄像头**：确认 `/dev/video0` 存在、没有被其他程序占用，
  当前用户有访问权限（可执行 `sudo usermod -aG video $USER` 后重新登录）。
- **画面分辨率与设置不一致**：摄像头不一定支持指定的分辨率/帧率，
  节点会使用驱动实际返回的参数，并在启动日志中打印实际值。
- **没有图形界面**：`camera_viewer` 依赖 `cv2.imshow`，需要有效的 `DISPLAY`；
  服务器环境可以只运行发布节点，用 `ros2 topic echo` 或 `rqt_image_view` 验证。
