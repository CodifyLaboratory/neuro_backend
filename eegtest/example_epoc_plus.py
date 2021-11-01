import os
import sys

# sys.path.insert(0, '..//py3//cyPyUSB//')
# sys.path.insert(0, '..//py3')

from .Py3 import cyPyWinUSB as hid
from .Py3.cyCrypto.Cipher import AES
from .Py3.cyCrypto import Random

# import cyPyWinUSB as hid
import queue

# from cyCrypto.Cipher import AES
# from cyCrypto import Random

tasks = queue.Queue()


class EEG(object):

    def init(self):
        self.hid = None
        self.delimiter = ", "
        self.serial_number = " "
        self.vendor_name = " "

    def get_headset(self):
        devicesUsed = 0
        for device in hid.find_all_hid_devices():
            if device.product_name == 'EEG Signals':
                devicesUsed += 1
                self.hid = device
                self.hid.open()
                self.serial_number = device.serial_number
                self.vendor_name = device.vendor_name
                device.set_raw_data_handler(self.dataHandler)
                print(device.set_raw_data_handler(self.dataHandler))
                sn = self.serial_number
                print(sn)

                # EPOC+ in 16-bit Mode.
                # k = ['\0'] * 16
                k = [sn[-1], sn[-2], sn[-2], sn[-3], sn[-3], sn[-3], sn[-2], sn[-4], sn[-1], sn[-4], sn[-2], sn[-2],
                     sn[-4], sn[-4], sn[-2], sn[-1]]
                print(k)

                self.key = str(''.join(k))
                print(self.key)
                self.cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)
                print(self.cipher)
                return devicesUsed
        if devicesUsed == 0:
            return devicesUsed

        # EPOC+ in 14-bit Mode.
        # k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]

    def dataHandler(self, data):
        join_data = ''.join(map(chr, data[1:]))
        data = self.cipher.decrypt(bytes(join_data, 'latin-1')[0:32])
        if str(data[1]) == "32":  # No Gyro Data.
            return data
        tasks.put(data)

    # def convertEPOC_PLUS(self, value_1, value_2):
    #     edk_value = "%.8f" % (
    #                 ((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) - 128) * 32.82051289))
    #     return edk_value

    # def get_data(self):
    #
    #     data = tasks.get()
    #     # print(str(data[0])) COUNTER
    #
    #     try:
    #         packet_data = ""
    #         for i in range(2, 16, 2):
    #             packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i + 1]))) + self.delimiter
    #
    #         for i in range(18, len(data), 2):
    #             packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i + 1]))) + self.delimiter
    #
    #         packet_data = packet_data[:-len(self.delimiter)]
    #         return str(packet_data)
    #
    #     except Exception as exception2:
    #         print(str(exception2))

# cyHeadset = EEG()
# while True:
#     while tasks.empty():
#         pass
#     # print(cyHeadset.get_data())