import os

stream_url = "tcp://localhost:6666"


class executors:
    num_parallel = 10
    animation_dir = os.path.join(os.getcwd(), "db")
