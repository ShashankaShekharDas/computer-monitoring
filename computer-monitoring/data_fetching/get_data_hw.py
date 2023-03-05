import wmi

hwmon = wmi.WMI(namespace="root\LibreHardwareMonitor")
sensors = hwmon.Sensor(SensorType="Voltage")

set_of_data_collected = {
    "Power",
    "Temperature",
    "Clock",
    "Load",
    "Fan",
    "Voltage"
}

'''
    Data to be collected
    Identifier : Name, Min, Max, Value, Time (upto exact milisecond)
    
    Data collect every second
    
    Store in 2 places
    -> Local DB 
    -> Cloud
    
    
    Confirm if sensor name will change, i dont think so, but confirm
    If SQL DB 
    Normalize tables based on 
    Sensor Type, then identifier name, then based on name
'''

sensorData = {i: {} for i in set_of_data_collected}

print(sensorData)
for s in sensors:
    if s.Identifier[1:].split("/")[0] in {"nvme", "hdd", "gpu-nvidia", "amdcpu"}:
        print(s.Identifier, s.Max, s.Min, s.Name, s.Value)
#     # sensorTypes.add(s.SensorType)
#
# print(sensorTypes)
