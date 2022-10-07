from mimos.skeleton.base import FrameData, Skeleton
from mimos.network import stream_socket
import time
import subprocess as sp
import shlex
from pathlib import Path


class Blender(Skeleton):
    def __init__(self, blend_file_path: str):
        parent_dir = Path(__file__).parent
        cmd = f"blender -y {blend_file_path} -P {parent_dir}/operator.py"
        self.process = sp.Popen(shlex.split(cmd), stdout=sp.PIPE, stderr=sp.PIPE)

    def move(self, data: FrameData):
        stream_socket.send_json(data.json())
        time.sleep(0.04)

    def destroy(self):
        self.process.terminate()
