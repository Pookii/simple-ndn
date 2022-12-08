# Author: Bingqi Xia
# Id: 22300549

from datetime import datetime
import os
import random
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class Sensor:
    def __init__(self, device_name, sensor_name, save_dir):
        # /area43/device1
        self.device_name = device_name
        self.sensor_name = sensor_name
        self.base_dir = save_dir + device_name + '/' + sensor_name + '/'
        self.base_name = device_name + '/' + sensor_name + '/'

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def create_file(self):
        # /device1/sensorA/1.txt
        time_nonce = datetime.now().strftime('%d%H%M%S')
        # file_name = "%s.txt" % time_nonce
        file_name = "1.txt"
        save_path = self.base_dir + file_name

        name_prefix = self.base_name + file_name
        # print("file_name: %s, save_path: %s" % (file_name, save_path))

        with open(save_path, "w") as f:
            content = str(random.randint(50, 60)) + ' km/h'
            f.write(content)

        return name_prefix


if __name__ == '__main__':
    time_nonce = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = "%s.txt" % time_nonce
    sensor = Sensor("", "./data/device1", 'sensorA')
    sensor.create_file()
