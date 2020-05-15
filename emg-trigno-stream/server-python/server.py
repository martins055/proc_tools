# -*- coding: utf-8 -*-

"""

Delsys station is connected to a Windows computer (169.254.1.2)
This script connects to it and streams the info to a webpage via websockets on port 7766

"""

import random
import logging
from aiohttp import web
import socketio
import time
import sys
sys.path.append("./pytrigno/")
# Trigno
try:
    import pytrigno
except ImportError:
    import sys
    sys.path.insert(0, '..')
    import pytrigno

# Server
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

############################ Trigno ####################################

# Start the EMG
dev = pytrigno.TrignoEMG(channel_range=(0, 7), samples_per_read=270,host='169.254.1.2')
# test multi-channels
dev.set_channel_range((0, 7)) # connect to the 8 channels of the emg
dev.start()
print("Started Trigno")

############################# Websockets ###############################

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect', namespace='/emg')
async def connect(sid, environ):
    print("connection de sid: ", sid, "on namespace /emg")
    await sio.emit('confirmation_connection', "emg", namespace='/emg')

@sio.on('disconnect', namespace='/emg')
def disconnect(sid):
    print('disconnect', sid)

@sio.on('emg message', namespace='/emg')
async def message(sid, data):
    print("server received message!", data)
    await sio.emit('reply', data, namespace='/emg')
    await sio.send(data)

######################### Asynchrone ###################################

async def start_background_task_trigno():
    while True:
        data = dev.read() # get data from trigno
        # we get a numpy.darray (8, 270) # print(type(data), data.shape)
        datalist = data.tolist() # instead of serialize/json
        await sio.emit('message', datalist, namespace='/emg')
        await sio.sleep(0.1)

    dev.stop() # stop the trigno
    print("stopped trigno")

########################## Start server ################################

app.router.add_get('/', index)

if __name__ == '__main__':
    sio.start_background_task(start_background_task_trigno)
    web.run_app(app, port=7766)
