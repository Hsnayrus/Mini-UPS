import threading
import time
from concurrent.futures import ThreadPoolExecutor

import amazon_ups_pb2
import world_ups_pb2
import communication_utils
import ups_database

DB_HOST = "localhost"
DB_PORT = 5432

RESP_WAIT_TIME = 8


AMAZON_SEQ_NUM = 1
WORLD_SEQ_NUM = 1
world_lock = threading.Lock()
amazon_lock = threading.Lock()
AMAZON_ACK_NUMS = set()
WORLD_ACK_NUMS = set()


def world_sequence_number():
    try:
        print("Generating sequence number for world ack")
        world_lock.acquire()
        global WORLD_SEQ_NUM
        temp = WORLD_SEQ_NUM
        WORLD_SEQ_NUM += 1
        world_lock.release()
        return temp
    except Exception as e:
        print("WORLD SEQUENCE GENERATION FAILED WITH THE FOLLWOWING EXCEPTION!")


def amazon_sequence_number():
    try:
        print("Generating sequence number for ack")
        amazon_lock.acquire()
        global AMAZON_SEQ_NUM
        temp = AMAZON_SEQ_NUM
        AMAZON_SEQ_NUM += 1
        amazon_lock.release()
        return temp
    except Exception as e:
        print("AMAZON SEQUENCE GENERATION FAILED WITH THE FOLLOWING EXCEPTION!")


def verify_world_ack_num(world_seq_num):
    global WORLD_ACK_NUMS
    return True if world_seq_num in WORLD_ACK_NUMS else False


def verify_amazon_ack_num(amazon_seq_num):
    global AMAZON_ACK_NUMS
    return True if amazon_seq_num in AMAZON_ACK_NUMS else False


def add_amazon_ack(amazon_ack_num):
    global AMAZON_ACK_NUMS
    AMAZON_ACK_NUMS.add(amazon_ack_num)


def add_world_ack(world_ack_num):
    global WORLD_ACK_NUMS
    WORLD_ACK_NUMS.add(world_ack_num)


def wait_for_response():
    time.sleep(RESP_WAIT_TIME)


def get_truck_or_wait(world_id):
    while True:
        available_truck_id = ups_database.get_available_truck(world_id)
        if available_truck_id != None:
            break
    return available_truck_id

def add_godeliver_to_world_command(world_command, seq_num, truck_id):
    print("Adding godeliver to world command...")
    go_deliver_command = world_command.deliveries.add()
    go_deliver_command.seqnum = seq_num
    go_deliver_command.truckid = truck_id
    print("finished adding godeliver to world command....")
    # return go_deliver_command


def add_gopickup_to_world_command(world_command, seq_num, warehouse_id, truck_id):
    print("Adding gopickup to world command....")
    go_pickup_command = world_command.pickups.add()
    go_pickup_command.whid = warehouse_id
    go_pickup_command.truckid = truck_id
    go_pickup_command.seqnum = seq_num
    print("Finished adding gopickup to world command....")


def add_package_to_delivery_message(delivery_message, delivery_pos_x, delivery_pos_y, package_id):
    print("adding package to delivery message")
    new_package_message = delivery_message.packages.add()
    new_package_message.x = delivery_pos_x
    new_package_message.y = delivery_pos_y
    new_package_message.packageid = package_id


def send_world_msg_and_wait_for_reply(socket, msg, seq_num):
    print(f"sending {msg} to world and waiting for ack....")
    while True:
        print("waiting...for....ack")
        communication_utils.send_protobuf_msg_to_socket(socket, msg)
        wait_for_response()
        if verify_world_ack_num(seq_num):
            print("received ack from world!!")
            return


def send_amazon_msg_and_wait_for_reply(socket, msg, seq_num):
    print(f"sending {msg} to amazon and waiting for ack....")
    while True:
        print("waiting...for....ack")
        communication_utils.send_protobuf_msg_to_socket(socket, msg)
        wait_for_response()
        if verify_amazon_ack_num(seq_num):
            print("received ack from amazon!!")
            return


def send_amazon_ack(amazon_socket, ack_num):
    amazon_update_message = amazon_ups_pb2.UACommand()
    amazon_update_message.acks.append(ack_num)
    print("Sending the following ack to AMAZON: {}\n".format(amazon_update_message))
    communication_utils.send_protobuf_msg_to_socket(amazon_socket, amazon_update_message)


def send_world_ack(world_socket, ack_num):
    world_update_message = world_ups_pb2.UCommands()
    world_update_message.acks.append(ack_num)
    print("Sending the following ack to WORLD: {}\n".format(world_update_message))
    communication_utils.send_protobuf_msg_to_socket(world_socket, world_update_message)

#### WORLD HANDLERS ####

def handle_world_completion(world_finished_message, world_socket, amazon_socket, world_id):
    '''
    message UFinished{
      required int32 truckid = 1;
      required int32 x = 2;
      required int32 y = 3;
      required string status = 4;
      required int64 seqnum = 5;
    }
    '''
    status = world_finished_message.status
    truck_id = world_finished_message.truckid
    x = world_finished_message.x
    y = world_finished_message.y
    seq_num = world_finished_message.seqnum
    print(f"Received a UFinished message with status {status}")
    # if status == "IDLE":
    if status == "idle":
        # means delivery finished
        print("UFinished message referred to ")
        ups_database.update_truck_status(truck_id, world_id, "idle")
        ups_database.update_truck_location(truck_id, world_id, x, y)
        send_world_ack(world_socket, seq_num)
    else:
        send_world_ack(world_socket, seq_num)
        ups_database.update_truck_status(truck_id, world_id, "loading")
        ups_database.update_truck_location(truck_id, world_id, x, y)
        amazon_update_message = amazon_ups_pb2.UACommand()
        # message UACommand{
        # 	repeated UTruckArrive arrive = 1;
        # 	repeated UDelivered delivered = 2;
        # 	repeated int64 acks = 3;
        # 	repeated Err error = 4;
        # }
        package_id = ups_database.get_package_with_truck_and_warehouse_location(truck_id, world_id, x, y)
        amazon_arrive_message = amazon_update_message.arrive.add()
        # message UTruckArrive{
        # 	required int64 packageid  = 1;
        # 	required int32 truckid  = 2;
        # 	repeated int64 seqnum = 3;
        # }
        amazon_arrive_message.packageid = package_id
        amazon_arrive_message.truckid = truck_id
        amazon_arrive_message.seqnum = amazon_sequence_number()
        # communication_utils.send_protobuf_msg_to_socket(amazon_socket, amazon_update_message)
        send_amazon_msg_and_wait_for_reply(amazon_socket, amazon_update_message, amazon_arrive_message.seqnum)
        print("Sent UTruckArrive message to amazon")


def handle_world_delivered(world_delivered_message, world_socket, amazon_socket, world_id):
    '''
    message UDeliveryMade{
      required int32 truckid = 1;
      required int64 packageid = 2;
      required int64 seqnum = 3;
    }
    '''
    package_id = world_delivered_message.packageid
    seq_num = world_delivered_message.seqnum
    send_world_ack(world_socket, seq_num)
    ups_database.update_package_status(world_id, package_id, 'delivered')
    print(f"Updating package({package_id}) status to delivered!")
    amazon_update_message = amazon_ups_pb2.UACommand()
    # message UACommand{
    # 	repeated UTruckArrive arrive = 1;
    # 	repeated UDelivered delivered = 2;
    # 	repeated int64 acks = 3;
    # 	repeated Err error = 4;
    # }
    amazon_delivered_message = amazon_update_message.delivered.add()
    # message UDelivered{
    # 	required int64 packageid  = 1;
    # 	required int64 seqnum = 2;
    # }
    amazon_delivered_message.packageid = package_id
    amazon_delivered_message.seqnum = amazon_sequence_number()
    # communication_utils.send_protobuf_msg_to_socket(amazon_socket, amazon_update_message)
    send_amazon_msg_and_wait_for_reply(amazon_socket, amazon_update_message, amazon_delivered_message.seqnum)


def handle_world_acks(ack_nums):
    global WORLD_ACK_NUMS
    for ack_num in ack_nums:
        WORLD_ACK_NUMS.add(ack_num)


def handle_world_errors(world_error):
    '''
    message Err{
	    required string err = 1;
  	    required int64 originseqnum = 2;
  	    required int64 seqnum = 3;
    }
    '''
    print(f"WORLD ERROR: {world_error.err}")


def handle_world_truck_query(world_truck_status):
    '''
    message UTruck{
      required int32 truckid =1;
      required string status = 2;
      required int32 x = 3;
      required int32 y = 4;
      required int64 seqnum = 5;
    }
    '''
    # NOTE: This handler is only called if our ups_server sends the world a
    # query; Our expected work flow doesn't presently require the use of
    # queries, so I wouldn't expect this function to get used much if at all
    print(f"WORLD TRUCK STATUS: {world_truck_status}")



def handle_world_finished(world_socket):
    '''
    message UCommands{
      repeated UGoPickup pickups = 1;
      repeated UGoDeliver deliveries = 2;
      optional uint32 simspeed = 3;
      optional bool disconnect = 4;
      repeated UQuery queries = 5;
      repeated int64 acks = 6;
    }
    '''
    world_update_command = world_ups_pb2.UCommands()
    world_update_command.disconnect = True
    seq_num = world_sequence_number()
    send_world_msg_and_wait_for_reply(world_socket, world_update_command, seq_num)
    exit(0)


#### AMAZON HANDLERS ####

def handle_amazon_acks(ack_nums):
    global AMAZON_ACK_NUMS
    for ack_num in ack_nums:
        AMAZON_ACK_NUMS.add(ack_num)


def handle_amazon_errors(amazon_error):
    '''
    message Err{
	    required string err = 1;
  	    required int64 originseqnum = 2;
  	    required int64 seqnum = 3;
    }
    '''
    print(f"AMAZON ERROR: {amazon_error.err}")



def handle_init_deliveries(world_socket, amazon_socket, amazon_delivery_command, world_id):
    '''amazon_delivery_command is the following message:
        message AStartDeliver{
            required int64 packageid  = 1;
            required int64 seqnum = 2;
        }
    '''
    # send a GoDeliver message to the World
    # wait for an ack and then update the truck and package status to out for delivery
    print(f"This is what the delivery command looks like: {amazon_delivery_command}")
    amazon_seq_num = amazon_delivery_command.seqnum
    delivery_package_id = amazon_delivery_command.packageid
    send_amazon_ack(amazon_socket=amazon_socket, ack_num=amazon_seq_num)
    new_world_command = world_ups_pb2.UCommands()
    seq_num = world_sequence_number()
    truck_info = ups_database.get_truck_info_for_package(delivery_package_id)
    print("Found the relevant truck info!")
    print(f"truck_id of required truck is {truck_info['truck_id']}")
    add_godeliver_to_world_command(new_world_command, seq_num, truck_info['truck_id'])
    print("made it beyond the godeliver")
    add_package_to_delivery_message(new_world_command.deliveries[0], truck_info['destination_pos_x'], truck_info['destination_pos_y'], delivery_package_id)
    ups_database.update_truck_status(truck_info['truck_id'], world_id, 'delivering')
    ups_database.update_package_status(world_id, delivery_package_id, 'out for delivery')
    print(f"Truck {truck_info['truck_id']} is now out for delivery!")
    print("Sending UGoDeliver to message to the world!")
    send_world_msg_and_wait_for_reply(world_socket, new_world_command, seq_num)



def handle_init_orders(world_socket, amazon_socket, amazon_order_command, world_id):
    '''amazon_order_command is the following message:
        AOrderATruck{
            required int64 packageid = 1;
            required int32 warehouselocationx = 2;
            required int32 warehouselocationy = 3;
            required int32 warehouseid = 4;
            required int32 destinationx = 5;
            required int32 destinationy = 6;
            optional string upsid = 7;
            required int64 seqnum = 8;
        }
    '''
    print(f"This is what the incoming AOrderATruck looks like: {amazon_order_command}")
    # add new package with packageid into database with the given fields in message
    # (associate the order with a ups account if one is provided?)
    # get a new truck to make the pickup and send a GoPickup message over to the world server
    # wait for a response and then after receiving an ack, change the truck status to en route
    package_id = amazon_order_command.packageid

    # TODO: we should consider sending a user acccount not found error to amazon if they give us a upsid that doesn't exist in our DB
    ups_account = None if not amazon_order_command.HasField('upsid') else amazon_order_command.upsid
    delivery_truck_id = get_truck_or_wait(world_id)
    warehouse_id = amazon_order_command.warehouseid
    warehouse_location_x = amazon_order_command.warehouselocationx
    warehouse_location_y = amazon_order_command.warehouselocationy
    destination_location_x = amazon_order_command.destinationx
    destination_location_y = amazon_order_command.destinationy
    amazon_seq_num = amazon_order_command.seqnum
    send_amazon_ack(amazon_socket=amazon_socket, ack_num=amazon_seq_num)
    ups_database.initialize_package(world_id,
                                    ups_account,
                                    delivery_truck_id,
                                    package_id,
                                    warehouse_id,
                                    warehouse_location_x,
                                    warehouse_location_y,
                                    destination_location_x,
                                    destination_location_y)
    seq_num = world_sequence_number()
    new_world_command = world_ups_pb2.UCommands()
    add_gopickup_to_world_command(new_world_command, seq_num, warehouse_id, delivery_truck_id)
    ups_database.update_truck_status(delivery_truck_id, world_id, 'travelling')
    print(f"Truck {delivery_truck_id} is travelling")
    print("Sending world GoPickUp Message!")
    send_world_msg_and_wait_for_reply(world_socket, new_world_command, seq_num)

#### THREAD CONTROL FUNCTIONS ####

def process_world_requests(amazon_socket, world_socket, world_id):
    '''world_command is the following message:
        UResponses{
          repeated UFinished completions = 1;
          repeated UDeliveryMade delivered = 2;
          optional bool finished = 3;
          repeated int64 acks = 4;
          repeated UTruck truckstatus = 5;
          repeated UErr error = 6;
        }
    '''
    # previously tried this using multiprocessing to avoid python GIL penalties, but
    # shared memory was needed to support the ack-seq messaging logic
    with ThreadPoolExecutor(max_workers=4) as exe:
        while True:
            time.sleep(1)
            world_command = communication_utils.receive_world_msg(world_socket)
            print(f"*~*~*~*~*\nHere is the recently received AUCommand: {world_command}")
            for world_completion in world_command.completions:
                print("Handling a world completion message\n")
                exe.submit(handle_world_completion, world_completion, world_socket, amazon_socket, world_id)
            for world_delivered in world_command.delivered:
                print("Handling a world delivered message\n")
                exe.submit(handle_world_delivered, world_delivered, world_socket, amazon_socket, world_id)
            for world_truckstatus in world_command.truckstatus:
                print("Handling a world truck status message\n")
                exe.submit(handle_world_truck_query, world_truckstatus)
            for world_error in world_command.error:
                print("Handling a world error message\n")
                exe.submit(handle_world_errors, world_error)
            if len(world_command.acks):
                print("Handling a world ack message\n")
                exe.submit(handle_world_acks, world_command.acks)
            if world_command.HasField("finished"):
                print("Handling a world finished message\n")
                exe.submit(handle_world_finished, world_socket)



def process_amazon_requests(amazon_socket, world_socket, world_id):
    '''amazon_command is the following message:
        AUCommand{
            repeated AStartDeliver deliver = 1;
            repeated AOrderATruck order = 2;
            repeated int64 acks = 3;
            repeated Err error = 4;
        }'''

    with ThreadPoolExecutor(max_workers=4) as exe:
        while True:
            time.sleep(1)
            amazon_command = communication_utils.receive_amazon_msg(amazon_socket)
            print(f"*~*~*~*~*\nHere is the recently received AUCommand: {amazon_command}")
            for amazon_delivery_command in amazon_command.deliver:
                print("Handling amazon delivery command\n")
                exe.submit(handle_init_deliveries, world_socket, amazon_socket, amazon_delivery_command, world_id)
            for amazon_order_command in amazon_command.order:
                print("Handling amazon order command\n")
                exe.submit(handle_init_orders, world_socket, amazon_socket, amazon_order_command, world_id)
            if len(amazon_command.acks):
                print("Handling amazon acks\n")
                exe.submit(handle_amazon_acks, amazon_command.acks)
            for amazon_command_error in amazon_command.error:
                print("Handling amazon error\n")
                exe.submit(handle_amazon_errors, amazon_command_error)
