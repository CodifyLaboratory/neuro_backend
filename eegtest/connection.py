ws_connections = {
}
from pyngrok import ngrok, conf


class Ngrok:
    @staticmethod
    def generate_tcp_url():
        ngrok.kill(pyngrok_config=conf.get_default())
        conf.get_default().auth_token = '21uxf517CHEduSGSkO9MJczRJs5_3DHeSFoT7JutuvqR9JaC3'
        tcp_tunnel = ngrok.connect(port=6868, proto='tcp')
        ngrok_url = tcp_tunnel.public_url[6:]
        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()
        return ngrok_url


# pyngrok_config = conf.get_default()
#
# if not os.path.exists(pyngrok_config.ngrok_path):
#     context = ssl.create_default_context()
#     context.check_hostname = False
#     context.verify_mode = ssl.CERT_NONE
#     installer.install_ngrok(pyngrok_config.ngrok_path, context=context)


# tunnels = ngrok.get_tunnels()
# print(tunnels)

connection = {}


# def _ws_connection():
#     url = 'wss://2.tcp.ngrok.io:18194/'
#     print(url)
#     ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
#     ws.connect(url=url)
#     connection[1] = ws
#     return ws
#
# print(ngrok_url)
# print(_ws_connection())
