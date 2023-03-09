import os.path
import subprocess

import psutil

from commons import variables
from commons.Exceptions.LibreException import LibreException


def check_if_libre_running():
    processes = (p.name() for p in psutil.process_iter())
    return variables.LIBRE_HW_EXECUTABLE in processes


def run_libre_executable():
    # NEEDS ADMIN PERMISSION OR POPUP
    full_executable_path = os.path.join(variables.PATH_TO_LIBRE_HW, variables.LIBRE_HW_EXECUTABLE)
    subprocess.call(full_executable_path, shell=True)


def run_libre_if_not_running():
    try:
        if not check_if_libre_running():
            run_libre_executable()
    except Exception as e:
        raise LibreException("Could not run Libre HW Monitor " + e)
