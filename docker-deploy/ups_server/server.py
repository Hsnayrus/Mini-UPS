import socket
from threading import Thread
import communication_utils
import ups_database
import world_ups_pb2
from handle_requests import process_amazon_requests, process_world_requests



def init_world_connection_message(world_connect_message, num_trucks=25, starting_pos_x=0, starting_pos_y=0):
    curr_truck_id = 0  # we will increment this value to sequentially specify truckids as needed
    for _ in range(num_trucks):
        new_truck = world_connect_message.trucks.add()
        new_truck.x = starting_pos_x
        new_truck.y = starting_pos_y
        new_truck.id = curr_truck_id
        curr_truck_id += 1
    world_connect_message.isAmazon = False
    # world_connect_message.worldid = WORLD_ID



def adjust_sim_speed(simspeed, world_connection):
    print("adjusting sim speed....")
    adjust_sim_speed = world_ups_pb2.UCommands()
    adjust_sim_speed.simspeed = simspeed
    communication_utils.send_protobuf_msg_to_socket(world_connection, adjust_sim_speed)
    # communication_utils.receive_incoming_connection(world_connection)

if __name__ == "__main__":
    HOST = socket.gethostname()
    AMAZON_PORT = 8888
    WORLD_HOST = "vcm-25947.vm.duke.edu"
    # WORLD_HOST = "localhost"
    WORLD_PORT = 12345 # connect to the world server on its UPS exposed port

    SIM_SPEED = 100

    # 1. Establish connection to the world
    print("Establishing connection to the world....")

    ups_database.reset_tables() # clear out any of the previous package and truck information in preparation for this new session

    open_connections = []
    try:
        world_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        open_connections.append(world_connection)
        world_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # this socket option avoids the error 'Address already in use'
        world_connection.connect((WORLD_HOST, WORLD_PORT))
        # WORLD_ID = 1
        ups_connect = world_ups_pb2.UConnect()
        init_world_connection_message(ups_connect)

        print(f"UConnect Message:\n{ups_connect}")
        communication_utils.send_protobuf_msg_to_socket(world_connection, ups_connect)
        ups_connected = communication_utils.receive_incoming_connection(world_connection)
        print(f"Here is the newly created world ID: {ups_connected.worldid}\n   result: {ups_connected.result}")
        WORLD_ID = ups_connected.worldid

        # adjust sim speed from the default 100 to the specified speed for testing
        # adjust_sim_speed(SIM_SPEED, world_connection)


        for truck in ups_connect.trucks:
            ups_database.add_new_truck(world_id=WORLD_ID, truck_id=truck.id, pos_x=truck.x, pos_y=truck.y)

        # 2. Establish connection to amazon
        print("Attempting to establish connection to amazon....")
        amazon_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        open_connections.append(amazon_connection)
        amazon_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # this socket option avoids the error 'Address already in use'
        amazon_connection.bind(('', AMAZON_PORT))
        amazon_connection.listen()
        amazon_connection, amazon_client_addr = amazon_connection.accept()
        print(f"Received Amazon connection from {amazon_client_addr}")

        # send world_id to amazon
        communication_utils.send_msg_to_socket(amazon_connection, WORLD_ID)


        # start to handle requests...
        t1 = Thread(target=process_amazon_requests, args=(amazon_connection, world_connection, WORLD_ID))
        t1.start()

        t2 = Thread(target=process_world_requests, args=(amazon_connection, world_connection, WORLD_ID))
        t2.start()


        # while True:
        #     pass


    except KeyboardInterrupt as e:
        for connection in open_connections:
            connection.close()












