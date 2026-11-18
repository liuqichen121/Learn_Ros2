import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/liuqichen121/Learn_Ros2/L01_helloworld/install/learning_qos'
