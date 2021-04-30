from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import asyncio
from starlette.endpoints import WebSocket, WebSocketEndpoint
from typing import Dict, Tuple
import telegram_send
import telebot;

bot = telebot.TeleBot('1797763054:AAENh337dik1__AEKvv9Ad6ty4O8M437-ak');
bot.polling()


UDP_PORT = 8001
message_data = 'te'



app = FastAPI()
ws_clients: Dict[str, WebSocket] = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MyUDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        print('received', data)
        # telegram_send.send(messages=[data.decode("utf-8")])
        message_data = data.decode("utf-8")
        print('sent')
        send()
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

@bot.message_handler(content_types=["text"])
def send(message):
    print('dfsdfsd')
    bot.send_message(message.chat.id, message_data)




# @bot.message_handler(content_types=['text'])
# @bot.message_handler(commands=['start'])
# def send(message):
#     bot.send_message(message.chat.id, 'dd')


