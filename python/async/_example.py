import asyncio

import websockets.exceptions

from lib.cortex import Cortex
from decouple import config

async def do_stuff(websocket, path):
    cortex = Cortex('./cortex_creds')
    print("** USER LOGIN **")
    await cortex.get_user_login()
    print("** GET CORTEX INFO **")
    await cortex.get_cortex_info()
    print("** HAS ACCESS RIGHT **")
    await cortex.has_access_right()
    print("** REQUEST ACCESS **")
    await cortex.request_access()
    print("** AUTHORIZE **")
    await cortex.authorize()
    print("** GET LICENSE INFO **")
    await cortex.get_license_info()
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()
    if len(cortex.headsets) > 0:
        print("** CREATE SESSION **")
        await cortex.create_session(activate=True,
                                    headset_id=cortex.headsets[0])
        print("** CREATE RECORD **")
        await cortex.create_record(title="test record 1")
        await cortex.subscribe(['pow', 'met'])
        print("** SUBSCRIBE POW & MET **")
        while True:
            try:
                await cortex.get_data()
            except websockets.exceptions.ConnectionClosed:
                print('EXIT!!!!!!!!!!')
                await cortex.close_session()


# user = {
#     "license": "",
#     "client_id": config('CLIENT_ID'),
#     "client_secret": config('CLIENT_SECRET'),
#     "debit": 100
# }
#
#
# def test():
#     cortex = Cortex('./cortex_creds')
#     asyncio.run(do_stuff(cortex))
#     cortex.close()






if __name__ == '__main__':
    start_server = websockets.serve(do_stuff, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
