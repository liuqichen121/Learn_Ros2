#include "rclcpp/rclcpp.hpp"

int main(int argc, char **argv)
{
  
  // 初始化
  rclcpp::init(argc, argv);
  // 创建节点
  auto node = rclcpp::Node::make_shared("helloworld_node");
  // 输出
  RCLCPP_INFO(node->get_logger(), "Hello world!By C++.\n");
  // 释放资源
  rclcpp::shutdown();
  return 0;
}