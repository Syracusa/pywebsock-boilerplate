import asyncio
import threading
from config import appconf

from util import *
# from logging import debug, info, warn, error, critical

import wsconn

if __name__ == "__main__":
    print(appconf['DEFAULT']['ip'])

    # asyncio.run(wsconn.websocket_loop())
    wst = asyncio.run(wsconn.singleton.websocket_loop())
