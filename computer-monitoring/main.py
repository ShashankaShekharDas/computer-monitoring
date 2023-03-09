import json
from time import sleep

from commons.Exceptions import LibreException, DBException
from data_fetching import get_data_hw
from initialization import run_libre
from CRUD import create_manage_db
import re


def get_data_and_put_db(libre_data):
    # Get Data
    libre_data.get_monitoring_data()
    json_data = json.loads(libre_data.data_json)

    # Put Data in Table
    for parameter in json_data:
        for identifier in json_data[parameter]:
            table_name = parameter + identifier.replace("/", "_") + "_" + \
                         json_data[parameter][identifier]["Name"].replace(" ", "")
            table_name = re.sub("[^a-zA-Z0-9 \n]", "_", table_name).strip("_")
            database_connection.create_table_if_not_exists(table_name)
            database_connection.insert_data(table_name, json_data[parameter][identifier]["Timestamp"],
                                            json_data[parameter][identifier]["Value"])
    print("Inserted Data Successfully")


try:
    while True:
        # initialise objects
        data_hw = get_data_hw.GetDataHw()
        database_connection = create_manage_db.ManageDB()
        # Check pre initialisation environment
        run_libre.run_libre_if_not_running()
        get_data_and_put_db(data_hw)
        sleep(5)

except DBException.DBException as db_exception:
    print(db_exception)
except LibreException.LibreException as libre_exception:
    print(libre_exception)
except Exception as e:
    print(e)
