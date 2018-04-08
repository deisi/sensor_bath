import os                                                  # import os module
import glob                                                # import glob module
import time                                                # import time module

class Ds18b20():
    def __init__(self, device_file=None):
        # Make sure kernel modules are loaded
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        if not device_file:
            self.device_file = self.get_device_file()
        else:
            self.device_file = device_file

    def get_device_file(self):
        base_dir = '/sys/bus/w1/devices/'                          # point to the address
        device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from 28*
        device_file = device_folder + '/w1_slave'                  # store the details
        return device_file

    def get_temp_raw(self):
       f = open(self.device_file, 'r')
       lines = f.readlines()                                   # read the device details
       f.close()
       return lines

    def get_temp(self):
       lines = self.get_temp_raw()
       while lines[0].strip()[-3:] != 'YES':                   # ignore first line
          time.sleep(0.2)
          lines = self.get_temp_raw()
       equals_pos = lines[1].find('t=')                        # find temperature in the details
       if equals_pos != -1:
          temp_string = lines[1][equals_pos+2:]
          temp_c = float(temp_string) / 1000.0                 # convert to Celsius
          temp_f = temp_c * 9.0 / 5.0 + 32.0                   # convert to Fahrenheit 
          return temp_c, temp_f
