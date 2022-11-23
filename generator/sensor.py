from datetime import datetime
import os

class Sensor:
    def __init__(self, name):
        self.name = name
        self.base_dir = os.getcwd() +'/Data'

    def create_file(self, file_name):
        (path, filename) = os.path.split(file_name)
        # print(path)
        if path[0] != '/':
            self.base_dir += '/'

        path = self.base_dir + path + '/'
        # print(path)

        if not os.path.exists(path):
            os.makedirs(path)

        save_path = path + filename
        print("path: %s, save_path: %s" % (path, save_path))
        with open(save_path, "w") as f:
            content = "hello, I am file %s from device %s" % (file_name, self.name)
            f.write(content)


if __name__ == '__main__':
    time_nonce = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = "/seed/test/sc/1_%s.txt" % time_nonce
    sensor = Sensor("PiA/nodeB")
    sensor.create_file(file_name)
