// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from learning_interface:msg/ObjectPosition.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "learning_interface/msg/object_position.hpp"


#ifndef LEARNING_INTERFACE__MSG__DETAIL__OBJECT_POSITION__TRAITS_HPP_
#define LEARNING_INTERFACE__MSG__DETAIL__OBJECT_POSITION__TRAITS_HPP_

#include <stdint.h>

#include <array>
#include <cstddef>
#include <sstream>
#include <string>
#include <string_view>
#include <tuple>
#include <type_traits>
#include <utility>

#include "learning_interface/msg/detail/object_position__struct.hpp"
#include "rosidl_runtime_cpp/buffer__traits.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace learning_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObjectPosition & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObjectPosition & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObjectPosition & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

template<typename T, std::enable_if_t<std::is_same_v<std::decay_t<T>, learning_interface::msg::ObjectPosition>, int> = 0>
constexpr auto as_tuple_ref(T && msg)
{
  return std::forward_as_tuple(
    std::forward<T>(msg).x,
    std::forward<T>(msg).y);
}

}  // namespace msg

}  // namespace learning_interface

namespace rosidl_generator_traits
{

template<>
constexpr const char * data_type<learning_interface::msg::ObjectPosition>()
{
  return "learning_interface::msg::ObjectPosition";
}

template<>
constexpr const char * name<learning_interface::msg::ObjectPosition>()
{
  return "learning_interface/msg/ObjectPosition";
}

template<>
struct has_fixed_size<learning_interface::msg::ObjectPosition>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<learning_interface::msg::ObjectPosition>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<learning_interface::msg::ObjectPosition>
  : std::true_type {};

template<>
struct MessageTraits<learning_interface::msg::ObjectPosition>
{
  static constexpr std::size_t member_count = 2;
  static constexpr std::array<std::string_view, member_count> member_names = {
    "x",
    "y",
  };
};

}  // namespace rosidl_generator_traits

#endif  // LEARNING_INTERFACE__MSG__DETAIL__OBJECT_POSITION__TRAITS_HPP_
