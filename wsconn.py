
import base64
from collections import deque
import websockets
import json
import asyncio
import sys
from util import *
from config import appconf

class WsConn:
    front_msgq = deque()

    def send_to_front(self, msg):
        self.front_msgq.appendleft(msg)
        pass
    
    def queue_reset(self):
        try:
            while True:
                msg = self.front_msgq.pop()
                cdebug(f'Drop q len {len(msg)}')
        except IndexError:
            # Done
            pass
        

        
# ======================================================
#                  CALLBACK Dict
# ======================================================

    callbacks = {}

# ======================================================
#                   CALLBACK Connector
# ======================================================

    ws_sendjob_count = 0

    async def ws_send_from_queue(self, websocket):
        while True:    
            if websocket.open == False:
                ccritical('Websocket closed... Cannot Send')
                self.queue_reset()
                
                await asyncio.sleep(1)
                if self.ws_sendjob_count > 1:
                    ccritical('Send from Queue TASK OUT')
                    self.ws_sendjob_count -= 1
                    break
            else :
                try:
                    while True:
                        msg = self.front_msgq.pop()
                        await websocket.send(msg)
                        cdebug(f'Send to Front.. len {len(msg)}')
                except IndexError:
                    # No left msg at queue
                    pass
                except :
                    ccritical('Unknown exception at send_msg_form_q' + sys.exc_info())
                await asyncio.sleep(0.01)
        pass

    async def ws_recv(self, websocket):
        try:                    
            asyncio.create_task(self.ws_send_from_queue(websocket))    
            self.ws_sendjob_count += 1
            cinfo(f'Send to Front Task Created. Task Count:{self.ws_sendjob_count}')
                
            async for message in websocket:
                msg = json.loads(message)
                
                # if len(msg) < 200:
                #     cdebug(f'Recv from client : {msg}')
                    
                if msg['request_type'] in self.callbacks:
                    await self.callbacks[msg['request_type']](self, websocket, msg)
                else:
                    cdebug(f"No request_type named : {msg['request_type']}")
        except websockets.ConnectionClosed as e:
            cdebug(f'Should restart websocket...{websocket.open} {websocket.closed}')
            
    async def websocket_loop(self):
        async with websockets.serve(self.ws_recv, 
                                        appconf['DEFAULT']['ip'], 
                                        int(appconf['DEFAULT']['websocketport'])):
            cdebug('in loop')
            await asyncio.Future()  # run forever
            

# Singleton
singleton = WsConn()