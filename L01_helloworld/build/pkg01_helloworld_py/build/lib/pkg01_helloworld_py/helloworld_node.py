import rclpy

def main():
    #初始化
    rclpy.init()
    #创建节点
    node = rclpy.create_node("helloworld_py")
    #文本输出
    node.get_logger().info("Hello world!By py.")
    rclpy.shutdown()

if __name__=='_main_':
    main()