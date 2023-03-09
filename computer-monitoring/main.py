import json
import re
import threading
from time import sleep
import pythoncom
from CRUD import create_manage_db
from commons.Exceptions.DBException import DBException
from commons.Exceptions.LibreException import LibreException
from data_fetching import get_data_hw
from initialization import run_libre


def get_data_from_monitor(result):
    '''
        Result variable will store the result from the thread, then the next thread
        reads the value and then stores in db
    '''
    pythoncom.CoInitialize()
    libre_data = get_data_hw.GetDataHw()
    libre_data.get_monitoring_data()
    json_data = json.loads(libre_data.data_json)

    # Put Data in Table
    for parameter in json_data:
        for identifier in json_data[parameter]:
            table_name = parameter + identifier.replace("/", "_") + "_" + \
                         json_data[parameter][identifier]["Name"].replace(" ", "")
            table_name = re.sub("[^a-zA-Z0-9 \n]", "_", table_name).strip("_")
            result.append(
                [
                    table_name,
                    [
                        json_data[parameter][identifier]["Timestamp"],
                        json_data[parameter][identifier]["Value"]
                    ]
                ]
            )


def database_operations_with_result(result):
    '''
        Function gets result from previous func and puts it in db
    '''
    database_connection = create_manage_db.ManageDB()
    run_libre.run_libre_if_not_running()
    for table in result:
        table_name, timestamp, value = table[0], table[1][0], table[1][1]
        database_connection.create_table_if_not_exists(table_name)
        database_connection.insert_data(table_name, timestamp, value)


while True:
    try:
        result_get_data_hw = []
        get_data_thread = threading.Thread(target=get_data_from_monitor, args=(result_get_data_hw,))
        get_data_thread.start()
        get_data_thread.join()
        put_data_db_thread = threading.Thread(target=database_operations_with_result, args=(result_get_data_hw,))
        put_data_db_thread.start()
        sleep(5)
    except DBException as db_exception:
        print(db_exception)
    except LibreException as libre_exception:
        print(libre_exception)
    except Exception as exception:
        print(exception)
