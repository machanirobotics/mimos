import os

stream_port = 6666
stream_url = f"tcp://localhost:{stream_port}"


class executors:
    num_parallel = 10
    animation_dir = os.path.join(os.getcwd(), "db")
