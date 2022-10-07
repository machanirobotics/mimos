from abc import ABC, abstractmethod
import queue
import threading
from typing import List, Optional

from mimos.utils.channel import Tx


class Input(ABC, threading.Thread):
    def __init__(self, queue_size: Optional[int] = None):
        super().__init__()
        self.txs: List[Tx] = []
        self.should_stop = False
        self.queue_size = queue_size

    def register(self, tx: Tx):
        self.txs.append(tx)

    def unregister_tx(self, tx: Tx):
        tx.terminate()
        self.txs.remove(tx)

    def run(self):
        while True and not self.should_stop:
            data = self.get_data()
            if data is None:
                continue
            for tx in self.txs:
                tx.put(data)

    def stop(self):
        if self.should_stop:
            return
        self.should_stop = True
        self.join()

        for tx in self.txs:
            self.unregister_tx(tx)

    def __del__(self):
        self.stop()

    @abstractmethod
    def get_data(self):
        raise NotImplementedError()
