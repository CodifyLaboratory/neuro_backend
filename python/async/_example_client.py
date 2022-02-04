import asyncio
import websockets
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def hello():
    async with websockets.connect("wss://2.tcp.ngrok.io:18638", ssl=ssl_context) as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()
        await websocket.close()

if __name__ == '__main__':
    asyncio.run(hello())