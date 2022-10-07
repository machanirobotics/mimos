from queue import Queue
from typing import Any, Optional, Tuple


class Tx:
    def __init__(self, queue: Queue):
        self.queue = queue
        self.has_terminated = False

    def put(self, data: Any):
        self.queue.put(data, block=True)

    def terminate(self):
        if not self.has_terminated:
            self.queue.put(StopIteration(), block=True)
            self.has_terminated = True

    def __del__(self):
        self.terminate()


class Rx:
    def __init__(self, queue: Queue):
        self.queue = queue

    def __iter__(self):
        return self

    def __next__(self):
        data = self.queue.get(block=True)
        if type(data) == StopIteration:
            raise StopIteration()

        return data


def channel(maxsize: Optional[int] = None) -> Tuple[Tx, Rx]:
    queue = Queue(maxsize=-1 if maxsize is None else maxsize)
    return Tx(queue), Rx(queue)
