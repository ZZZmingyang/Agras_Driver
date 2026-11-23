#!/usr/bin/env python3
"""Render synthetic points in RViz inside Xvfb; optionally save a PNG."""
import json
import os
from pathlib import Path
import signal
import socket
import struct
import subprocess
import tempfile
import time
import zlib

import rclpy
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import PointCloud2

from smoke_test import loopback_config, packet


def save_xwd_as_png(source, target):
    data = source.read_bytes()
    h = struct.unpack_from('>25I', data)
    header_size, _, _, depth, width, height = h[:6]
    byte_order, bits_per_pixel, stride = h[7], h[11], h[12]
    assert depth == 24 and bits_per_pixel == 32 and byte_order == 0, h
    assert h[14:17] == (0xff0000, 0xff00, 0xff), h
    pixels = data[header_size + h[19] * 12:]
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for x in range(width):
            b, g, r = pixels[y * stride + x * 4:y * stride + x * 4 + 3]
            rows.extend((r, g, b))
    def chunk(kind, body):
        return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body))
    target.write_bytes(b'\x89PNG\r\n\x1a\n' +
                      chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) +
                      chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


def main():
    rclpy.init()
    node = rclpy.create_node('rviz_smoke_monitor')
    observed = []
    subscription = node.create_subscription(PointCloud2, '/livox/lidar/pointcloud', observed.append, qos_profile_sensor_data)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)
        env = dict(os.environ, DISPLAY=':91', LIBGL_ALWAYS_SOFTWARE='1')
        xvfb = subprocess.Popen(['Xvfb', ':91', '-screen', '0', '1920x1080x24', '-fbdir', directory],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        application = None
        with (path / 'rviz.log').open('w+') as log, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
            try:
                for _ in range(50):
                    if Path('/tmp/.X11-unix/X91').exists():
                        break
                    time.sleep(0.1)
                assert xvfb.poll() is None
                config = path / 'network.json'
                config.write_text(json.dumps(loopback_config()))
                application = subprocess.Popen([
                    'ros2', 'launch', 'agras_bringup', 'view.launch.py', 'config:=' + str(config),
                ], env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                sender.bind(('127.0.0.2', 60001))
                points = b''.join(struct.pack('<iiiBB', 1000 + i * 150, j * 150, 0, 100, 0x10)
                                  for i in range(20) for j in range(20))
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline:
                    sender.sendto(packet(1, points, count=400), ('127.0.0.1', 60001))
                    rclpy.spin_once(node, timeout_sec=0.001)
                    time.sleep(0.03)
                log.flush()
                log.seek(0)
                output = log.read()
                assert application.poll() is None, output
                assert len(observed) >= 5, 'No PointCloud2 received while rendering'
                names = node.get_node_names()
                assert names.count('livox_lidar_publisher') == 1, names
                assert names.count('rviz2') == 1, names
                assert '[ERROR]' not in output and 'Failed to' not in output, output
                result = Path('/tmp/agras-rviz.png')
                save_xwd_as_png(path / 'Xvfb_screen0', result)
                application.send_signal(signal.SIGINT)
                assert application.wait(timeout=10) == 0
                print(json.dumps(dict(status='PASS', check='view-launch-software-render',
                                     driver_count=1, rviz_count=1, clouds=len(observed), screenshot=str(result))))
            finally:
                if application is not None and application.poll() is None:
                    os.killpg(application.pid, signal.SIGKILL)
                    application.wait()
                if xvfb.poll() is None:
                    xvfb.terminate()
                    xvfb.wait(timeout=3)
                node.destroy_node()
                rclpy.shutdown()


if __name__ == '__main__':
    main()
