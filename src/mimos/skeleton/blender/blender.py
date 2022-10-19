from typing import Dict
from mimos.skeleton.base import FrameData, Skeleton
from mimos.network import stream_socket
import mimos.config as config
import time
import subprocess as sp
import shlex
from pathlib import Path
import tempfile
import os
import site
import shutil


class Blender(Skeleton):
    def __init__(
        self,
        blend_file_path: str,
        debug: bool = False,
        skeleton_object: str = "BODY_Bones",
        modal_timer: float = 0.04,
    ):
        self.skeleton_object = skeleton_object
        self.modal_timer = modal_timer
        if not shutil.which("blender"):
            raise RuntimeError("Blender not found on path")

        if not os.path.exists(blend_file_path):
            raise FileNotFoundError(blend_file_path)

        operator_tpl_path = Path(__file__).parent / "operator.py.tpl"
        self.operator_path = self.create_operator_file(
            operator_tpl_path,
            {
                "${SITE_PACKAGES}": str(site.getsitepackages()),
                "${SKELETON_OBJECT}": skeleton_object,
                "${MODAL_TIMER}": str(modal_timer),
                "${STREAM_PORT}": str(config.stream_port),
            },
        )
        cmd = f"blender -y {blend_file_path} -P {self.operator_path}"
        if debug:
            self.process = sp.Popen(shlex.split(cmd))
        else:
            self.process = sp.Popen(shlex.split(cmd), stdout=sp.PIPE, stderr=sp.PIPE)

    def move(self, data: FrameData):
        stream_socket.send_json(data.json())
        time.sleep(self.modal_timer)

    def destroy(self):
        self.process.terminate()
        os.remove(self.operator_path)

    def create_operator_file(
        self, template_path: str, substitutions: Dict[str, str]
    ) -> str:
        with open(template_path, "r") as f:
            operator_contents = f.readlines()

        for idx, line in enumerate(operator_contents):
            for key, value in substitutions.items():
                if key in line:
                    operator_contents[idx] = line.replace(key, value)

        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "w") as tmp:
            tmp.writelines(operator_contents)

        return path