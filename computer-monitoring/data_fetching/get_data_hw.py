import json
from datetime import datetime
import wmi


class GetDataHw:
    def __init__(self):
        self.hwmon = wmi.WMI(namespace=r"root\LibreHardwareMonitor")
        self.data_json = dict()
        self.set_of_data_collected = {
            "Power",
            "Temperature",
            "Clock",
            "Load",
            "Fan",
            "Voltage"
        }

    def get_specific_monitoring_fields(self, timestamp, parameter, sensor_data):
        for data in sensor_data:
            if data.Identifier[1:].split("/")[0] in {"nvme", "hdd", "gpu-nvidia", "amdcpu"}:
                if parameter not in self.data_json:
                    self.data_json[parameter] = dict()
                self.data_json[parameter][data.Identifier] = {
                    "Timestamp": timestamp,
                    "Name": data.Name,
                    "Value": data.Value
                }

    def get_monitoring_data(self):
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for parameter in self.set_of_data_collected:
            self.get_specific_monitoring_fields(time_now, parameter, self.hwmon.Sensor(SensorType=parameter))
        self.data_json = json.dumps(self.data_json)
