from .cortex import Cortex
from django.db import models
from user.models import User
from .models import Test


class Subcribe(models.Model):
    """
    A class to subscribe data stream.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User',
                             blank=True, null=True, related_name='data')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test',
                             blank=True, null=True, related_name='data')


    def __init__(self):
        """
        Constructs cortex client and bind a function to handle subscribed data streams
        If you do not want to log request and response message , set debug_mode = False. The default is True
        """
        self.c = Cortex(user, debug_mode=True)
        self.c.bind(new_data_labels=self.on_new_data_labels)
        self.c.bind(new_eeg_data=self.on_new_eeg_data)
        self.c.bind(new_mot_data=self.on_new_mot_data)
        self.c.bind(new_dev_data=self.on_new_dev_data)
        self.c.bind(new_met_data=self.on_new_met_data)
        self.c.bind(new_pow_data=self.on_new_pow_data)

    def do_prepare_steps(self):
        """
        Do prepare steps before training.
        Step 1: Connect a headset. For simplicity, the first headset in the list will be connected in the example.
                If you use EPOC Flex headset, you should connect the headset with a proper mappings via EMOTIV App first 
        Step 2: requestAccess: Request user approval for the current application for first time.
                       You need to open EMOTIV App to approve the access
        Step 3: authorize: to generate a Cortex access token which is required parameter of many APIs
        Step 4: Create a working session with the connected headset
        Returns
        -------
        None
        """
        self.c.do_prepare_steps()

    def sub(self, streams):
        """
        To subscribe to eeg data streams
        """
        self.c.sub_request(streams)

    def on_new_data_labels(self, *args, **kwargs):
        """
        To handle data labels of subscribed data 
        Returns
        -------
        data: list  
              array of data labels
        name: stream name
        For example:
            eeg: ["COUNTER","INTERPOLATED", "AF3", "T7", "Pz", "T8", "AF4", "RAW_CQ", "MARKER_HARDWARE"]
            motion: ['COUNTER_MEMS', 'INTERPOLATED_MEMS', 'Q0', 'Q1', 'Q2', 'Q3', 'ACCX', 'ACCY', 'ACCZ', 'MAGX', 'MAGY', 'MAGZ']
            dev: ['AF3', 'T7', 'Pz', 'T8', 'AF4', 'OVERALL']
            met : ['eng.isActive', 'eng', 'exc.isActive', 'exc', 'lex', 'str.isActive', 'str', 'rel.isActive', 'rel', 'int.isActive', 'int', 'foc.isActive', 'foc']
            pow: ['AF3/theta', 'AF3/alpha', 'AF3/betaL', 'AF3/betaH', 'AF3/gamma', 'T7/theta', 'T7/alpha', 'T7/betaL', 'T7/betaH', 'T7/gamma', 'Pz/theta', 'Pz/alpha', 'Pz/betaL', 'Pz/betaH', 'Pz/gamma', 'T8/theta', 'T8/alpha', 'T8/betaL', 'T8/betaH', 'T8/gamma', 'AF4/theta', 'AF4/alpha', 'AF4/betaL', 'AF4/betaH', 'AF4/gamma']
        """
        data = kwargs.get('data')
        stream_name = data['streamName']
        stream_labels = data['labels']
        print('{} labels are : {}'.format(stream_name, stream_labels))


    def on_new_dev_data(self, *args, **kwargs):
        """
        To handle dev data emitted from Cortex

        Returns
        -------
        data: dictionary
             The values in the array dev match the labels in the array labels return at on_new_data_labels
        For example:  {'signal': 1.0, 'dev': [4, 4, 4, 4, 4, 100], 'batteryPercent': 80, 'time': 1627459265.4463}
        """
        data = kwargs.get('data')
        print('dev data: {}'.format(data))

    def on_new_pow_data(self, *args, **kwargs):
        """
        To handle band power data emitted from Cortex

        Returns
        -------
        data: dictionary
             The values in the array pow match the labels in the array labels return at on_new_data_labels
        For example: {'pow': [5.251, 4.691, 3.195, 1.193, 0.282, 0.636, 0.929, 0.833, 0.347, 0.337, 7.863, 3.122, 2.243, 0.787, 0.496, 5.723, 2.87, 3.099, 0.91, 0.516, 5.783, 4.818, 2.393, 1.278, 0.213], 'time': 1627459390.1729}
        """
        data = kwargs.get('data')
        print('pow data: {}'.format(data))


# -----------------------------------------------------------
# 
# SETTING
#   - replace your license, client_id, client_secret to user dic
#   - specify infor for record and export
#   - connect your headset with dongle or bluetooth, you should saw headset on EmotivApp
# SUBSCRIBE
#     you need to folow steps:
#         1) do_prepare_steps: for authorization, connect headset and create working session.
#         2) sub(): to subscribe data, you can subscribe one stream or multiple streams
# RESULT
#   - the data labels will be retrieved at on_new_data_labels
#   - the data will be retreived at on_new_[dataStream]_data
# 
# -----------------------------------------------------------

"""
    client_id, client_secret:
    To get a client id and a client secret, you must connect to your Emotiv account on emotiv.com and create a Cortex app
    To subscribe eeg you need to put a valid licese (PRO license)
"""
# user = {
#     "license": "26f60052-0070-4b35-9ed8-fec4363edfc6",
#     "client_id": "ZsMXJvVqaOR4Pq5QUY46Djw4wXNjni3MK4NBihh3",
#     "client_secret": "7OwHHGELxD9tQLoo2J5g1kswqKcjkoD51XoX8qGcjBSytuqt3gtg9Yuq0f1KX6fRNzJIn3DVGZ3FNQ7WflfHSMvWr4YKhldprljskJBAFdHuo8xYpIgoEdlzZlMQzLS8",
#     "debit": 100
# }

user = {
    "license": "26f60052-0070-4b35-9ed8-fec4363edfc6",
    "client_id": "N0mvmXCzhTLbYNVYDkAMmrUf5WK1YlvPA7D0ujZm",
    "client_secret": "3KVc00v5obtcBzo96moG0wjdEjJ8bNjsgeLl3VzGPbTMnp0woJPmB3dBbxOZ00V66XJTKHcWAeldMSbcvmVTQGGHLcPOSJZPWHweWnVvGUTu1b6a8NxlyWqLWrHf8WgA",
    "debit": 100
}

# s = Subcribe()
#
# # Do prepare steps
# s.do_prepare_steps()
#
# # sub multiple streams
# # streams = ['eeg','mot','met','pow']
#
# # or only sub for eeg
# streams = ['eeg']
#
# s.sub(streams)
# -----------------------------------------------------------

# def start():
#     s = Subcribe()
#     s.do_prepare_steps()
#     streams = ['eeg']
#     s.sub(streams)