# import json
# import ssl
#
# from django.test import TestCase
# import websocket
# from websocket import create_connection
#
# ws = create_connection("wss://localhost:6868", sslopt={"cert_reqs": ssl.CERT_NONE})
# get_cortex_info_request = {
#     "jsonrpc": "2.0",
#     "method": "getCortexInfo",
#     "id": 100
# }
# ws.send(json.dumps(get_cortex_info_request))
# result = ws.recv()
# print(json.dumps(json.loads(result), indent=4))
# # print(result)
# # ws.close()
#
# # import websocket
# #
# #
# # def on_message(wsapp, message):
# #     print(message)
# #
# #
# # wsapp = websocket.WebSocketApp("wss://localhost:6868", on_message=on_message)
# # wsapp.run_forever()
import json

import websocket
import ssl

websocket.enableTrace(True)
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://localhost:6868")
get_cortex_info_request = {
            "jsonrpc": "2.0",
            "method": "getCortexInfo",
            "id": 100
        }
ws.send(json.dumps(get_cortex_info_request))
print(ws.recv())
ws.close()
