import psycopg2
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor, DictCursor

import amazon_ups_pb2
import world_ups_pb2
import communication_utils


# DB_HOST = "db"
DB_HOST = "localhost"
DB_PORT = 5432



def reset_tables():
    db_connection, db_cursor = get_db_cursor()
    db_cursor.execute("delete from deliveries_package")
    db_cursor.execute("delete from deliveries_truck")
    db_connection.commit()
    db_cursor.close()


def establish_db_connection():
   return psycopg2.connect(host=DB_HOST, database="postgres", user="postgres", password="passw0rd", port="5432", cursor_factory=DictCursor)


def get_db_cursor():
    db_connection = establish_db_connection()
    return db_connection, db_connection.cursor()


def finish_using_db(db_cursor, db_connection):
    # db_cursor.commit()
    db_connection.commit()
    db_cursor.close()


def get_truck_info_for_package(package_id):
    print("Looking for the truck info for package_id {}".format(package_id))
    db_connection, db_cursor = get_db_cursor()
    db_cursor.execute(f"select truck_id, destination_pos_x, destination_pos_y from deliveries_package where package_id={package_id}")
    package_truck_info = db_cursor.fetchone()
    finish_using_db(db_cursor, db_connection)
    print("package_truck_info.keys -- {}".format(list(package_truck_info.keys())))
    return package_truck_info


def get_package_with_truck_and_warehouse_location(truck_id, world_id, warehouse_x, warehouse_y):
    db_connection, db_cursor = get_db_cursor()
    db_cursor.execute(f"select package_id "
                      f"from deliveries_package "
                      f"where truck_id={truck_id} "
                      f"and warehouse_pos_x={warehouse_x} "
                      f"and warehouse_pos_y={warehouse_y} "
                      f"and world_id={world_id} "
                      f"and status='waiting to be picked up'")
    package_info = db_cursor.fetchone()
    finish_using_db(db_cursor, db_connection)
    return package_info['package_id']



def add_new_truck(world_id, truck_id, pos_x, pos_y):
    db_connection, db_cursor = get_db_cursor()
    try:
        db_cursor.execute(f"insert into deliveries_truck (truck_id, world_id, status, pos_x, pos_y)  values "
                      f"({truck_id},"
                      f"{world_id}, "
                      f"'idle', "
                      f"{pos_x}, "
                      f"{pos_y}) ")
    except IntegrityError:
        pass
    finish_using_db(db_cursor, db_connection)

def get_available_truck(world_id):
    db_connection, db_cursor = get_db_cursor()
    db_cursor.execute(f"select truck_id from deliveries_truck where status='idle' and world_id={world_id} limit 1")
    db_cursor.execute(f"select truck_id from deliveries_truck where status='idle' and world_id={world_id} limit 1")
    available_truck_entry = db_cursor.fetchone()
    for key in list(available_truck_entry.keys()):
        print("key in entry: {}".format(key))
    print("This is what was found: {}".format(available_truck_entry))
    print("available_truck_entry type = {}".format(type(available_truck_entry)))
    available_truck_id = None if not available_truck_entry else available_truck_entry['truck_id']
    print("available_truck_id -- {}".format(available_truck_id))
    finish_using_db(db_cursor, db_connection)
    return available_truck_id


def update_truck_status(truck_id, world_id, new_status):
    db_connection, db_cursor = get_db_cursor()
    print(f"updating truck {truck_id} to be {new_status}")
    db_cursor.execute(f"update deliveries_truck set status='{new_status}' where truck_id={truck_id} and world_id={world_id}")
    finish_using_db(db_cursor, db_connection)


def update_truck_location(truck_id, world_id, new_location_x, new_location_y):
    db_connection, db_cursor = get_db_cursor()
    db_cursor.execute(f"update deliveries_truck set pos_x={new_location_x}, pos_y={new_location_y} where truck_id={truck_id} and world_id={world_id}")
    finish_using_db(db_cursor, db_connection)


def update_package_status(world_id, package_id, new_status):
    db_connection, db_cursor = get_db_cursor()
    print(f"updating package {package_id} to be {new_status}")
    db_cursor.execute(f"update deliveries_package set status='{new_status}' where package_id={package_id} and world_id={world_id}")
    finish_using_db(db_cursor, db_connection)



# def update_truck_location(truck_id, world_id, new_location_x, new_location_y):

# def get_or_create_ups_account(ups_account_id, world_id, db_cursor):
#     db_cursor.execute(f"select acct_number from deliveries_upsaccount where acct_number={ups_account_id} and world_id={world_id} limit 1")
#     existing_account = db_cursor.fetchone()
#     if not existing_account:
#         db_cursor.execute(f"insert into deliveries_upsaccount (world_id, user_id, acct_number) "
#                           f"values ({world_id}, 0, {ups_account_id})")



def initialize_package(world_id, ups_account, truck_id, package_id, warehouse_id, warehouse_pos_x, warehouse_pos_y, destination_pos_x, destination_pos_y):
    db_connection, db_cursor = get_db_cursor()

    # check if ups account exists
    try:
        if ups_account:
            db_cursor.execute(f"insert into deliveries_package "
                              f"(package_id, "
                              f"world_id, "
                              f"destination_pos_x, "
                              f"destination_pos_y, "
                              f"warehouse_id, "
                              f"warehouse_pos_x, "
                              f"warehouse_pos_y, "
                              f"status, "
                              f"truck_id, "
                              f"ups_account_id) values"
                              f"({package_id}, "
                              f"{world_id}, "
                              f"{destination_pos_x}, "
                              f"{destination_pos_y}, "
                              f"{warehouse_id}, "
                              f"{warehouse_pos_x}, "
                              f"{warehouse_pos_y}, "
                              f"'waiting to be picked up', "
                              f"{truck_id}, "
                              f"{ups_account})")
        else:
            db_cursor.execute(f"insert into deliveries_package "
                              f"(package_id, "
                              f"world_id, "
                              f"destination_pos_x, "
                              f"destination_pos_y, "
                              f"warehouse_id, "
                              f"warehouse_pos_x, "
                              f"warehouse_pos_y, "
                              f"status, "
                              f"truck_id,"
                              f"ups_account_id) values"
                              f"({package_id}, "
                              f"{world_id}, "
                              f"{destination_pos_x}, "
                              f"{destination_pos_y}, "
                              f"{warehouse_id}, "
                              f"{warehouse_pos_x}, "
                              f"{warehouse_pos_y}, "
                              f"'waiting to be picked up', "
                              f"{truck_id},"
                              f"NULL )")
    except IntegrityError:
        pass

    finish_using_db(db_cursor, db_connection)


