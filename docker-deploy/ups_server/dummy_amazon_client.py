import socket
import communication_utils
import world_amazon_pb2

if __name__ == "__main__":
    HOST = socket.gethostname()
    AMAZON_PORT = 8888
    WORLD_HOST = "vcm-25947.vm.duke.edu"
    WORLD_PORT = 23456

    # UPS_HOST = socket.gethostname()
    UPS_HOST = "vcm-25947.vm.duke.edu"
    UPS_PORT = 8888

    # 1. Establish connection to the world
    print("Establishing connection to the world....")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as world_connection:
        world_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # this socket option avoids the error 'Address already in use'
        world_connection.connect((WORLD_HOST, WORLD_PORT))
        WORLD_ID = 1
        amazon_connect = world_amazon_pb2.AConnect()
        amazon_connect.worldid = 1
        init = amazon_connect.initwh.add()
        init.id = 1
        init.x = 0
        init.y = 0
        amazon_connect.isAmazon = True

        # init_world_connection_message(amazon_connect)

        print(f"AConnect Message:\n{amazon_connect}")
        communication_utils.send_protobuf_msg_to_socket(world_connection, amazon_connect)
        ups_connected = communication_utils.receive_incoming_connection(world_connection)
        print(f"Here is the newly created world ID: {ups_connected.worldid}\n   result: {ups_connected.result}")

        # 2. Establish connection to ups
        print("Attempting to establish connection to ups....")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ups_sock:
            ups_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ups_sock.connect((UPS_HOST, 8888))
            print("ups connect")


            # # start to handle requests...
            # t1 = Thread(target=process_amazon_requests, args=(amazon_connection, world_connection, WORLD_ID))
            # t1.start()
            #
            # t2 = Thread(target=process_world_requests, args=(amazon_connection, world_connection, WORLD_ID))
            # t2.start()











