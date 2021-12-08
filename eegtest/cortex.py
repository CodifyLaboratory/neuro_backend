import json
import ssl
import time
import websocket
from decouple import config
from pydispatch import Dispatcher

# define request id
from eegtest.models import CortexSessionModel

QUERY_HEADSET_ID = 1
CONNECT_HEADSET_ID = 2
REQUEST_ACCESS_ID = 3
AUTHORIZE_ID = 4
CREATE_SESSION_ID = 5
SUB_REQUEST_ID = 6
SETUP_PROFILE_ID = 7
QUERY_PROFILE_ID = 8
TRAINING_ID = 9
DISCONNECT_HEADSET_ID = 10
CREATE_RECORD_REQUEST_ID = 11
STOP_RECORD_REQUEST_ID = 12
EXPORT_RECORD_ID = 13
INJECT_MARKER_REQUEST_ID = 14
GET_USER_INFO = 15
UNSUB_REQUEST_ID = 16



class ConnectionStore:
    def __init__(self):
        self.__connections= {}


class Cortex(Dispatcher):
    def __init__(self, user, debug_mode=False):
        self.url = "wss://2.tcp.ngrok.io:18638"
        ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
        ws.connect(url=self.url)
        self.ws = ws
        self.user = user
        self.debug = debug_mode

    def ws_connect(self, url):
        ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
        ws.connect(url=url)
        self.ws = ws
        print(ws.sock)
        print(ws.connected)
        return ws

    def get_cortex_info(self):
        get_cortex_info_request = {
            "jsonrpc": "2.0",
            "method": "getCortexInfo",
            "id": 100
        }
        self.ws.send(json.dumps(get_cortex_info_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def query_headset(self):
        query_headset_request = {
            "jsonrpc": "2.0",
            "id": QUERY_HEADSET_ID,
            "method": "queryHeadsets",
            "params": {}
        }
        self.ws.send(json.dumps(query_headset_request, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def connect_headset(self, headset_id):
        connect_headset_request = {
            "jsonrpc": "2.0",
            "id": CONNECT_HEADSET_ID,
            "method": "controlDevice",
            "params": {
                "command": "connect",
                "headset": headset_id
            }
        }
        self.ws.send(json.dumps(connect_headset_request, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def disconnect_headset(self, headset_id):
        connect_headset_request = {
            "jsonrpc": "2.0",
            "id": DISCONNECT_HEADSET_ID,
            "method": "controlDevice",
            "params": {
                "command": "disconnect",
                "headset": headset_id
            }
        }
        self.ws.send(json.dumps(connect_headset_request, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def request_access(self):
        request_access_request = {
            "jsonrpc": "2.0",
            "method": "requestAccess",
            "params": {
                "clientId": self.user['client_id'],
                "clientSecret": self.user['client_secret']
            },
            "id": REQUEST_ACCESS_ID
        }
        self.ws.send(json.dumps(request_access_request, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def authorize(self):
        authorize_request = {
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {
                "clientId": self.user['client_id'],
                "clientSecret": self.user['client_secret'],
                "license": self.user['license'],
                "debit": self.user['debit']
            },
            "id": AUTHORIZE_ID
        }
        self.ws.send(json.dumps(authorize_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def get_user_info(self, cortex_token):
        get_user_info_request = {
            "jsonrpc": "2.0",
            "method": "getUserInformation",
            "params": {
                "cortexToken": cortex_token,
            },
            "id": GET_USER_INFO
        }
        self.ws.send(json.dumps(get_user_info_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def create_session(self, cortex_token, headset):
        create_session_request = {
            "jsonrpc": "2.0",
            "id": CREATE_SESSION_ID,
            "method": "createSession",
            "params": {
                "cortexToken": cortex_token,
                "headset": headset,
                "status": "active"
            }
        }
        self.ws.send(json.dumps(create_session_request))
        time.sleep(1)
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

        # self.session_id = result_dic['result']['id']

    def close_session(self, cortex_token, session_id):
        close_session_request = {
            "jsonrpc": "2.0",
            "id": CREATE_SESSION_ID,
            "method": "updateSession",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "status": "close"
            }
        }
        self.ws.send(json.dumps(close_session_request))
        time.sleep(1)
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def get_session(self, cortex_token):
        query_session_request = {
            "jsonrpc": "2.0",
            "id": CREATE_SESSION_ID,
            "method": "querySessions",
            "params": {
                "cortexToken": cortex_token,
            }
        }
        self.ws.send(json.dumps(query_session_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def subscribe_request(self, cortex_token, session_id):
        sub_request_json = {
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "streams": ['pow']
            },
            "id": SUB_REQUEST_ID
        }
        self.ws.send(json.dumps(sub_request_json))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def unsubscribe_request(self, cortex_token, session_id):
        unsub_request_json = {
            "jsonrpc": "2.0",
            "method": "unsubscribe",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "streams": ['pow']
            },
            "id": UNSUB_REQUEST_ID
        }
        self.ws.send(json.dumps(unsub_request_json))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def create_record(self, cortex_token, session_id, record_name):
        create_record_request = {
            "jsonrpc": "2.0",
            "method": "createRecord",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
                "title": record_name,
            },

            "id": CREATE_RECORD_REQUEST_ID
        }

        self.ws.send(json.dumps(create_record_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def stop_record(self, cortex_token, session_id):
        stop_record_request = {
            "jsonrpc": "2.0",
            "method": "stopRecord",
            "params": {
                "cortexToken": cortex_token,
                "session": session_id,
            },

            "id": STOP_RECORD_REQUEST_ID
        }

        self.ws.send(json.dumps(stop_record_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

    def export_record(self, cortex_token, record_ids, folder):
        export_record_request = {
            "jsonrpc": "2.0",
            "id": EXPORT_RECORD_ID,
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

        self.ws.send(json.dumps(export_record_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        return result_dic

        # if result_dic.get('error') != None:
        #     print("subscribe get error: " + result_dic['error']['message'])
        #     return
        # else:
        #     # handle data lable
        #     for stream in result_dic['result']['success']:
        #         stream_name = stream['streamName']
        #         stream_labels = stream['cols']
        #         # ignore com and fac data label because they are handled in on_new_data
        #         if stream_name != 'com' and stream_name != 'fac':
        #             self.extract_data_labels(stream_name, stream_labels)

        # while True:
        #     new_data = self.ws.recv()
        #     # Then emit the change with optional positional and keyword arguments
        #     result_dic = json.loads(new_data)
        #     if result_dic.get('com') != None:
        #         com_data = {}
        #         com_data['action'] = result_dic['com'][0]
        #         com_data['power'] = result_dic['com'][1]
        #         com_data['time'] = result_dic['time']
        #         self.emit('new_com_data', data=com_data)

        #     elif result_dic.get('dev') != None:
        #         dev_data = {}
        #         dev_data['signal'] = result_dic['dev'][1]
        #         dev_data['dev'] = result_dic['dev'][2]
        #         dev_data['batteryPercent'] = result_dic['dev'][3]
        #         dev_data['time'] = result_dic['time']
        #         self.emit('new_dev_data', data=dev_data)

        #     elif result_dic.get('pow') != None:
        #         pow_data = {}
        #         pow_data['pow'] = result_dic['pow']
        #         pow_data['time'] = result_dic['time']
        #         self.emit('new_pow_data', data=pow_data)
        #     else:
        #         print(new_data)

    def query_profile(self):
        print('query profile --------------------------------')
        query_profile_json = {
            "jsonrpc": "2.0",
            "method": "queryProfile",
            "params": {
                "cortexToken": self.auth,
            },
            "id": QUERY_PROFILE_ID
        }

        if self.debug:
            print('query profile request \n', json.dumps(query_profile_json, indent=4))
            print('\n')

        self.ws.send(json.dumps(query_profile_json))

        result = self.ws.recv()
        result_dic = json.loads(result)

        print('query profile result\n', result_dic)
        print('\n')

        profiles = []
        for p in result_dic['result']:
            profiles.append(p['name'])

        print('extract profiles name only')
        print(profiles)
        print('\n')

        return profiles

    def setup_profile(self, profile_name, status):
        print('setup profile: ' + status + ' -------------------------------- ')
        setup_profile_json = {
            "jsonrpc": "2.0",
            "method": "setupProfile",
            "params": {
                "cortexToken": self.auth,
                "headset": self.headset_id,
                "profile": profile_name,
                "status": status
            },
            "id": SETUP_PROFILE_ID
        }

        if self.debug:
            print('setup profile json:\n', json.dumps(setup_profile_json, indent=4))
            print('\n')

        self.ws.send(json.dumps(setup_profile_json))

        result = self.ws.recv()
        result_dic = json.loads(result)

    def inject_marker_request(self, marker):
        print('inject marker --------------------------------')
        inject_marker_request = {
            "jsonrpc": "2.0",
            "id": INJECT_MARKER_REQUEST_ID,
            "method": "injectMarker",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "label": marker['label'],
                "value": marker['value'],
                "port": marker['port'],
                "time": marker['time']
            }
        }

        self.ws.send(json.dumps(inject_marker_request))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('inject marker request \n', json.dumps(inject_marker_request, indent=4))
            print('inject marker result \n',
                  json.dumps(result_dic, indent=4))

c = Cortex
