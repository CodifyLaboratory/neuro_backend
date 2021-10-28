from django.db import models
import os
import sys
from Py3 import cyPyWinUSB as hid
import queue
from Py3.cyCrypto.Cipher import AES
from Py3.cyCrypto import Random

# sys.path.insert(0, '..//py3//cyUSB//')
# sys.path.insert(0, '..//py3')

tasks = queue.Queue()

class Headset(models.Model):
    hid = models.CharField(max_length=250, verbose_name='Device', blank=True, null=True)
    serial_number = models.CharField(max_length=250, verbose_name='Serial Number', blank=True, null=True)
    product_name = models.CharField(max_length=250, verbose_name='Name', blank=True, null=True)

    class Meta:
        verbose_name = 'Headset'
        verbose_name_plural = 'Headsets'

    def __str__(self):
        return self.hid

    def get_headset(self):
        devicesUsed = 0
        for device in hid.find_all_hid_devices():
            if device.product_name == 'EEG Signals':
                devicesUsed += 1
                self.hid = device
                self.hid.open()
                self.serial_number = device.serial_number
                device.set_raw_data_handler(self.dataHandler)
        if devicesUsed == 0:
            print('No headsets.')
            os._exit(0)