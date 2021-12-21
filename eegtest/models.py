import json
import ssl
import time
from datetime import date

import websocket
from decouple import config
from django.db import models

from .connection import ws_connections, Ngrok
from user.models import User
from pyngrok import ngrok, conf


class Test(models.Model):
    title = models.CharField(max_length=250, unique=True, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    status = models.BooleanField(verbose_name='Status', default=False)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.title


class StimuliCategory(models.Model):
    title = models.CharField(max_length=250, verbose_name='Stimulus category', blank=True, null=True)

    class Meta:
        verbose_name = 'Stimulus category'
        verbose_name_plural = 'Stimulus categories'

    def __str__(self):
        return self.title


class Stimulus(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test', related_name='stimulus')
    category = models.ForeignKey(StimuliCategory, on_delete=models.CASCADE, verbose_name='Category')
    title = models.CharField(max_length=250, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    duration = models.DurationField(verbose_name='Duration')
    file = models.FileField(verbose_name='File')

    class Meta:
        verbose_name = 'Stimuli'
        verbose_name_plural = 'Stimulus'

    def __str__(self):
        return self.title

    def get_str_id(self):
        return str(self.pk)


class Parameter(models.Model):
    title = models.CharField(max_length=250, verbose_name='Parameter', blank=True, null=True)

    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameters'

    def __str__(self):
        return self.title


# class Operation(models.Model):
#     title = models.CharField(max_length=250, verbose_name='Operation', blank=True, null=True)
#
#     class Meta:
#         verbose_name = 'Operation'
#         verbose_name_plural = 'Operations'
#
#     def __str__(self):
#         return self.title


class Calculation(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test',
                             related_name='calculations')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Parameter',
                                  related_name='calculations', blank=True, null=True)

    class Meta:
        verbose_name = 'Calculation'
        verbose_name_plural = 'Calculations'

    def __str__(self):
        return '{}'.format(self.test)


class StimuliGroup(models.Model):
    calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE, verbose_name='Calculation',
                                    related_name='stimuli_groups')
    stimuli = models.ManyToManyField(Stimulus, verbose_name='Stimulus', related_name='stimuli_groups')

    class Meta:
        verbose_name = 'Stimuli Groups'
        verbose_name_plural = 'Stimuli Groups'

    def __str__(self):
        return '{}'.format(self.calculation)


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User',
                             blank=True, null=True, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test',
                             blank=True, null=True, related_name='results')
    title = models.CharField(max_length=250, verbose_name='Title', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    file = models.FileField(verbose_name='File', blank=True, null=True)
    date = models.DateField(verbose_name='Date of creation', default=date.today)
    status = models.BooleanField(verbose_name='Status', default=False)
    parameter = models.BooleanField(verbose_name='Status', default=False)

    class Meta:
        verbose_name = 'Test result'
        verbose_name_plural = 'Test results'

    def __str__(self):
        return self.title


class CortexSessionModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    url = models.CharField(max_length=250, verbose_name='url')


class CortexObjectModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    url = models.CharField(max_length=250, verbose_name='Websocket URL', blank=True, null=True)
    client_id = models.CharField(max_length=250, verbose_name='Cortex Client ID', default=config('CLIENT_ID'))
    client_secret = models.CharField(max_length=250, verbose_name='Cortex Client Secret',
                                     default=config('CLIENT_SECRET'))
    ngrok_token = models.CharField(max_length=250, verbose_name='Ngrok Access Token', default=config('NGROK_TOKEN'))

    class Meta:
        verbose_name = 'Cortex Object'
        verbose_name_plural = 'Cortex Object'

    def __str__(self):
        return '{}'.format(self.user)

    def generate_tcp_url(self):
        ngrok.kill(pyngrok_config=conf.get_default())
        conf.get_default().auth_token = self.ngrok_token
        tcp_tunnel = ngrok.connect(port=6868, proto='tcp')
        self.url = tcp_tunnel.public_url[6:]
        # ngrok_process = ngrok.get_ngrok_process()
        # ngrok_process.proc.wait()
        return self.url

    def _ws_connection(self):
        ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
        ws.connect(url=self.url)
        print(self.url)
        user = self.user
        ws_connections[user.id] = ws
        return ws.connected

    # CORTEX AUTH
    def authorize(self, ws):
        authorize_request = {
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {
                "clientId": self.client_id,
                "clientSecret": self.client_secret,
                "license": '',
                "debit": 100
            },
            "id": 1
        }
        ws.send(json.dumps(authorize_request))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def request_access(self, ws):
        request_access_request = {
            "jsonrpc": "2.0",
            "method": "requestAccess",
            "params": {
                "clientId": self.client_id,
                "clientSecret": self.client_secret
            },
            "id": 2
        }
        ws.send(json.dumps(request_access_request, indent=4))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    # HEADSETS
    def query_headset(self, ws):
        query_headset_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "queryHeadsets",
            "params": {}
        }
        ws.send(json.dumps(query_headset_request, indent=4))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def connect_headset(self, ws, headset_id):
        connect_headset_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "controlDevice",
            "params": {
                "command": "connect",
                "headset": headset_id
            }
        }
        ws.send(json.dumps(connect_headset_request, indent=4))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def disconnect_headset(self, ws, headset_id):
        connect_headset_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "controlDevice",
            "params": {
                "command": "disconnect",
                "headset": headset_id
            }
        }
        ws.send(json.dumps(connect_headset_request, indent=4))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    # SESSIONS
    def create_session(self, ws, cortex_token, headset):
        create_session_request = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "createSession",
            "params": {
                "cortexToken": cortex_token,
                "headset": headset,
                "status": "active"
            }
        }
        ws.send(json.dumps(create_session_request))
        time.sleep(1)
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def close_session(self, ws, cortex_token, session_id):
        close_session_request = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "updateSession",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "status": "close"
            }
        }
        ws.send(json.dumps(close_session_request))
        time.sleep(1)
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def get_query_session(self, ws, cortex_token):
        query_session_request = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "querySessions",
            "params": {
                "cortexToken": cortex_token,
            }
        }
        ws.send(json.dumps(query_session_request))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    # STREAMS
    def subscribe_request(self, ws, cortex_token, session_id):
        sub_request_json = {
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "streams": ['pow']
            },
            "id": 9
        }
        ws.send(json.dumps(sub_request_json))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def unsubscribe_request(self, ws, cortex_token, session_id):
        unsub_request_json = {
            "jsonrpc": "2.0",
            "method": "unsubscribe",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "streams": ['pow']
            },
            "id": 10
        }
        ws.send(json.dumps(unsub_request_json))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    # RECORDS
    def create_record(self, ws, cortex_token, session_id, record_name):
        create_record_request = {
            "jsonrpc": "2.0",
            "method": "createRecord",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "title": record_name,
            },

            "id": 11
        }

        ws.send(json.dumps(create_record_request))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def stop_record(self, ws, cortex_token, session_id):
        stop_record_request = {
            "jsonrpc": "2.0",
            "method": "stopRecord",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
            },

            "id": 12
        }

        ws.send(json.dumps(stop_record_request))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def export_record(self, ws, cortex_token, record_ids, folder):
        export_record_request = {
            "jsonrpc": "2.0",
            "id": 13,
            "method": "exportRecord",
            "params": {
                "cortexToken": cortex_token,
                "folder": folder,
                "format": 'CSV',
                "streamTypes": ['BP'],
                "recordIds": record_ids,
                "version": 'V2',
            }
        }

        # if export_format == 'CSV':
        #     export_record_request['params']['version'] = export_version

        ws.send(json.dumps(export_record_request))
        result = ws.recv()
        result_dic = json.loads(result)
        return result_dic
