# FAST-LIO2 ROS2 / Agras

ROS 包名保留为 `fast_lio`。本包是 FAST-LIO2 的 ROS2 移植与 Agras 适配，
使用 ikd-Tree 和迭代误差状态滤波；当前未包含历史说明提及的回环、GTSAM 和重定位模块。

独立启动：`ros2 launch fast_lio mapping.launch.py`（需要已运行的雷达驱动）。
组合启动：`ros2 launch agras_bringup fast_lio2.launch.py`。

可用参数：`params_file`、`output_dir`、`rviz`、`rviz_cfg`、`use_sim_time`、`sensor_frame`。
世界系默认为 `map`，机体系 `body`，传感器系 `livox_frame`。
来源说明：<https://github.com/hku-mars/FAST_LIO>。

默认点云输入目标为 20 Hz，内置 IMU 保持原生频率，不做 180 Hz 重采样。
原仓库 FAST-LIO 说明完整保存在 [README.upstream.md](README.upstream.md)，仅供历史参考；
其中其他包的功能与旧启动命令不代表当前包集合已提供。
