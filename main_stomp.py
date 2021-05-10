from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import stomp
import telegram_send
import re
import xml.etree.ElementTree as ET

test_str = """{cmd=MESSAGE,headers=[{'content-length': '1198', 'expires': '0', 'destination': '/topic/presto', 'subscription': '1', 'priority': '4', 'message-id': 'ID:seiscomp-presto-caiag-42301-1619687563310-3:2:-1:1:79', 'timestamp': '1619689164778'}],body=<?xml version="1.0" ?>
<q:quakeml xmlns='http://quakeml.org/xmlns/bed-rt/1.2' xmlns:q='http://quakeml.org/xmlns/quakeml-rt/1.2'>
<eventParameters publicID='smi:org.presto/ew/realtime_2021-04-29_1400'>
<event publicID='smi:org.presto/ev/realtime_2021-04-29_1400'><type>earthquake</type>
<preferredOriginID>smi:org.presto/or/realtime_2021-04-29_1400</preferredOriginID>
<preferredMagnitudeID>smi:org.presto/ma/realtime_2021-04-29_1400</preferredMagnitudeID>
</event>
<origin publicID='smi:org.presto/or/realtime_2021-04-29_1400'>
	<time><value>2021-04-29T09:39:11.00Z</value></time>
	<longitude><value>71.3928</value><uncertainty>2.63335</uncertainty></longitude>
	<latitude><value>40.0938</value><uncertainty>1.31667</uncertainty></latitude>
	<depth><value>12375</value><uncertainty>28866.1</uncertainty></depth>
</origin>
<magnitude publicID='smi:org.presto/ma/realtime_2021-04-29_1400'><mag><value>4.7</value><lowerUncertainty>1.7</lowerUncertainty><upperUncertainty>2</upperUncertainty></mag></magnitude>
<pick publicID='smi:org.presto/pi/1619689177.MLSU'><time><value>2021-04-29T09:39:37.36Z</value></time><waveformID networkCode='AD' stationCode='MLSU' /></pick>
</eventParameters>
</q:quakeml>}"""


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers):
        print(headers)
        # print('received an error "%s"' % message)
    def on_message(self, headers):
        # message = str(headers)
        text = str(headers)
        if '<eventParameters' in text:
            parser(text)
   

def parser(str):
        
        message = str
        start = message.find('<eventParameters')
        end = message.find('</eventParameters>')
        text = '<?xml version="1.0" encoding="UTF-8"?>' + message[start:end] + '</eventParameters>'
        print('text', text)
        if text != '</q:quakeml>':
            myroot = ET.fromstring(text)
            for x in myroot:
                if x.tag == 'event':
                    event = x[0].text
                    print(event)
                elif x.tag == 'origin':
                    time = x[0][0].text
                    print(time)
                    longitude = x[1][0].text
                    longitude_uncert = x[1][1].text
                    latitude = x[2][0].text
                    latitude_uncert = x[2][1].text
                    depth = x[3][0].text
                    depth_uncert = x[3][1].text
                elif x.tag == 'magnitude':
                    magnitude = x[0][0].text
                    magnitude_lower_uncert = x[0][1].text
                    magnitude_upper_uncert = x[0][2].text
                    print(magnitude, magnitude_lower_uncert, magnitude_upper_uncert)
                elif x.tag == 'pick':
                    attribs = json.dumps(x.attrib)
                    print(attribs)
                    # station_code = x[1][0].tag
                    # print(station_code)
            message_text = "time: " + time + "\nlongitude: " + longitude + "\nlatitude: " + latitude + "\ndepth: " + depth + "\nmagnitude: " + magnitude + '\nattributes: ' + attribs
            print('tags', myroot.tag)
        telegram_send.send(messages=[message_text])

def make_connection(app_event):
        event_name = app_event.get('name', None)
        queue_name = app_event.get('queue_name', None)

        connection = stomp.Connection()
        connection.set_listener(name=event_name, lstnr=EventManager())
        connection.connect('',  '', wait=True)
        connection.subscribe(destination=queue_name, id=event_name, ack='auto')
        return

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def connect():
    conn = stomp.Connection([('192.168.20.118', 61613)])
    lst = MyListener()
    conn.set_listener('', lst)
    conn.connect('presto', 'presto', wait=True)
    conn.subscribe(destination='/topic/presto', id=1, ack='auto')
    return 'success'






# conn = stomp.Connection()
# lst = MyListener()
# conn.set_listener('', lst)
# conn.start()
# conn.connect()
# conn.subscribe(destination='/queue/test', id=1, ack='auto')
# time.sleep(2)
# messages = lst.msg_list
# conn.disconnect()
# return render(request, 'template.html', {'messages': messages})