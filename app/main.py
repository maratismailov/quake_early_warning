from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import asyncio
from starlette.endpoints import WebSocket, WebSocketEndpoint
from typing import Dict, Tuple
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import telegram_send
import time
import re


UDP_PORT = 8001
message_data = 'te'
qids = []



app = FastAPI()
ws_clients: Dict[str, WebSocket] = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # return render_template('report.html', hists = hists)
    return templates.TemplateResponse("index.html", {"request": request})

class MyUDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        # telegram_send.send(messages=[data.decode("utf-8")])
        message_data = data.decode("utf-8")
        if 'ALARM DEST:T_BISH' in message_data:
            pattern = r'.*?QID:(.*) SEQ.*'  
            match = re.search(pattern, message_data)
            qid = match.group(1)
            print('qid', qid, 'end')
            for id in qids:
                if qid == id:
                    print('d')

            current_time = str(datetime.now())
            text_file = open("logs/" + current_time + '.log', "w+")
            text_file.write(message_data)
            text_file.close()
            # telegram_send.send(messages=[data.decode("utf-8")])
            print(message_data)
            # time.sleep(60)
        # telegram_send.send(messages=[message_data])
   

        
        return 's'
        ws_client = ws_clients[addr[0]]
        print(data)
        asyncio.create_task(send_info_to_client(ws_client, data))


@app.on_event("startup")
async def on_startup() -> None:
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: MyUDPProtocol(), local_addr=("0.0.0.0", UDP_PORT)
    )
    app.state.udp_transport = transport
    app.state.udp_protocol = protocol
    print('start')
    qids_file = open('qids.json', 'r')
    qids = json.load(qids_file)
    for qid in qids:
        print(qid)

def make_alarm(message):
    print('dd')


# @bot.message_handler(content_types=['text'])
# @bot.message_handler(commands=['start'])
# def send(message):
#     bot.send_message(message.chat.id, 'dd')


