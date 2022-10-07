import zmq
import mimos.config as config


context = zmq.Context()
stream_socket = context.socket(zmq.PUB)
stream_socket.connect(config.stream_url)
