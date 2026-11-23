# Optional ROS2 development environment. The repository is mounted into /ws/src.
FROM ros:humble-ros-base-jammy@sha256:a18afd4a42ad603579d03b9012385dfeaf2e848423f0a6c41699766e7849c86c
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake python3-colcon-common-extensions python3-rosdep \
    libapr1-dev libaprutil1-dev libpcl-dev libeigen3-dev libceres-dev \
    python3-dev python3-numpy python3-matplotlib \
    ros-humble-ament-cmake-auto ros-humble-pcl-ros ros-humble-pcl-conversions \
    ros-humble-tf2-ros ros-humble-tf2-eigen ros-humble-std-srvs ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /ws
CMD ["bash"]
