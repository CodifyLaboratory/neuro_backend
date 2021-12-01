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
import certifi

# ssl_context = ssl.create_default_context()
# ssl_context.load_verify_locations(certifi.where())

websocket.enableTrace(True)
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
ws.connect("wss://127.0.0.1:6868", ssl=ssl.CERT_NONE, http_proxy_host="143.198.221.88", http_proxy_port="80", proxy_type="http")
get_cortex_info_request = {
            "jsonrpc": "2.0",
            "method": "getCortexInfo",
            "id": 100
        }
ws.send(json.dumps(get_cortex_info_request))
print(ws.recv())
ws.close()
