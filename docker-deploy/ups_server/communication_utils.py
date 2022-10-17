import world_ups_pb2
import amazon_ups_pb2
from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.decoder import _DecodeVarint32



def encode_varint(varint):
    data_buffer = []
    _VarintEncoder()(data_buffer.append, varint, None)
    return b''.join(data_buffer)


def decode_varint(encoded_varint):
    return _DecodeVarint32(encoded_varint, 0)[0]




def send_msg_to_socket(socket, message):
    # print("message_str = {}".format(message_data))
    message_data = str(message).encode('utf-8')
    socket.sendall(message_data)


def send_protobuf_msg_to_socket(socket, message):
    message_data = message.SerializeToString()
    # print("message_str = {}".format(message_data))
    message_size = encode_varint(len(message_data))
    socket.sendall(message_size + message_data)



def _receive_msg(socket):
    raw_data_size = b''
    while True:
        try:
            raw_data_size += socket.recv(1)
            data_size = decode_varint(raw_data_size)
            break
        except IndexError as e:
            continue
    raw_data_msg = socket.recv(data_size)
    return raw_data_msg

def receive_amazon_msg(socket):
    raw_data_msg = _receive_msg(socket)
    ups_response = amazon_ups_pb2.AUCommand()
    ups_response.ParseFromString(raw_data_msg)
    return ups_response


def receive_ups_msg(socket):
    raw_data_size = b''
    while True:
        try:
            raw_data_size += socket.recv(1)
            data_size = decode_varint(raw_data_size)
            break
        except IndexError as e:
            continue
    raw_data_msg = socket.recv(data_size)
    amazon_response = amazon_ups_pb2.UACommand()
    amazon_response.ParseFromString(raw_data_msg)
    return amazon_response


def receive_world_msg(socket):
    raw_data_msg = _receive_msg(socket)
    world_response = world_ups_pb2.UResponses()
    world_response.ParseFromString(raw_data_msg)
    return world_response

def receive_incoming_connection(socket):
    received_bytes = b''
    while True:
        try:
            received_bytes += socket.recv(1)
            msg_size = decode_varint(received_bytes)
            break
        except IndexError as e:
            # print("Caught an index out of bounds error.... continuing to find message size")
            continue

    msg_received = socket.recv(msg_size)
    response = world_ups_pb2.UConnected()
    response.ParseFromString(msg_received)
    return response
