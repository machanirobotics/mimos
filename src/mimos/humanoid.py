from typing import Callable
from mimos.body import Body


class Humanoid:
    def __init__(self, body: Body, controller: Callable):
        self.body = body
        self.controller = controller

    def run(self):
        self.controller(self.body)
