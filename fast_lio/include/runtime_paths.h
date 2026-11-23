#pragma once
#include <cstdlib>
#include <filesystem>
#include <string>
#include <stdexcept>

namespace agras_runtime {
inline std::string default_output_dir(const std::string& component) {
  const char* ros_home = std::getenv("ROS_HOME");
  const char* home = std::getenv("HOME");
  std::filesystem::path base = ros_home && *ros_home ? ros_home :
      (home && *home ? std::filesystem::path(home) / ".ros" : std::filesystem::temp_directory_path() / "ros");
  return (base / "agras" / component).string();
}
inline std::string& output_dir() {
  static std::string path;
  return path;
}
inline void set_output_dir(const std::string& requested) {
  output_dir() = std::filesystem::absolute(requested).lexically_normal().string();
  for (const char* subdir : {"Log", "PCD", "result"}) {
    std::filesystem::create_directories(std::filesystem::path(output_dir()) / subdir);
  }
}
}  // namespace agras_runtime
