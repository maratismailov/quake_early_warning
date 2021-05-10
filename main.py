#! ./env/bin/python3
import socket
import re
from datetime import datetime, timedelta
import telegram_send
import os

qids = []
print('start')
def parse_message(data):
    message_data = data.decode("utf-8")
    if message_data == 'testpacket':
        os.system("telegram-send --config ./telegram-send.conf '{}'".format(message_data))
    if 'ALARM DEST:T_BISH' in message_data:
        qid_pattern = r'.*?QID:(.*) SEQ:.*'
        qid_match = re.findall(qid_pattern, message_data)
        qid = qid_match[0]
        if qid not in qids:
            pga_pattern = r'.*?PGA:(.*) PGAmin:.*'
            pga_match = re.findall(pga_pattern, message_data)
            pga = pga_match[0]
            print('pga', pga)

            pga_min_pattern = r'.*?PGAmin:(.*) PGAmax:.*'
            pga_min_match = re.findall(pga_min_pattern, message_data)
            pga_min = pga_min_match[0]
            print('pga_min', pga_min)

            pga_max_pattern = r'.*?PGAmax:(.*) PGV:.*'
            pga_max_match = re.findall(pga_max_pattern, message_data)
            pga_max = pga_max_match[0]
            print('pga_max', pga_max)

            pgv_pattern = r'.*?PGV:(.*) PGVmin:.*'
            pgv_match = re.findall(pgv_pattern, message_data)
            pgv = pgv_match[0]
            print('pgv', pgv)

            pgv_min_pattern = r'.*?PGVmin:(.*) PGVmax:.*'
            pgv_min_match = re.findall(pgv_min_pattern, message_data)
            pgv_min = pgv_min_match[0]
            print('pgv_min', pgv_min)

            pgv_max_pattern = r'.*?PGVmax:(.*) SECS:.*'
            pgv_max_match = re.findall(pgv_max_pattern, message_data)
            pgv_max = pgv_max_match[0]
            print('pgv_max', pgv_max)

            remaining_pattern = r'.*?SECS:(.*) M:.*'
            remaining_match = re.findall(remaining_pattern, message_data)
            remaining = remaining_match[0]
            print('remaining', remaining)

            mag_pattern = r'.*?M:(.*) Mmin:.*'
            mag_match = re.findall(mag_pattern, message_data)
            mag = mag_match[0]
            print('mag', mag)

            lon_pattern = r'.*?LON:(.*) Xer:.*'
            lon_match = re.findall(lon_pattern, message_data)
            lon = lon_match[0]
            print('lon', lon)

            lat_pattern = r'.*?LAT:(.*) Yer:.*'
            lat_match = re.findall(lat_pattern, message_data)
            lat = lat_match[0]
            print('lat', lat)

            dep_pattern = r'.*?DEP:(.*) Zer:.*'
            dep_match = re.findall(dep_pattern, message_data)
            dep = dep_match[0]
            print('dep', dep)

            e_time_pattern = r'.*?Ot0:(.*) *.*'
            e_time_match = re.findall(e_time_pattern, message_data)
            e_time = e_time_match[0]
            print('e_time', e_time)

            reg_time_pattern = r'.*?(.*): ALARM DEST:.*'
            reg_time_match = re.findall(reg_time_pattern, message_data)
            reg_time = reg_time_match[0]
            print('reg_time', reg_time)

            remaining_int = float(remaining)
            arrival_time = datetime.strptime(reg_time, '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=remaining_int)
            print('ftime', arrival_time)
            arrival_time_str = arrival_time.strftime('%Y-%m-%d %H:%M:%S.%f')

            message = 'event_time:' + e_time + '\n' + 'reg_time:' + reg_time + '\n' + 'arrival time:' + arrival_time_str + '\n' + 'mag:' + mag + '\n' + 'pgv:' + pgv + '\n' + 'pga:' + pga + '\n' + 'lon:' + lon + '\n' + 'lat:' + lat + '\n' + 'dep:' + dep + '\n'
            print(message)
            qids.append(qid)
            current_time = str(datetime.now())
            text_file = open("logs/" + current_time + '.log', "w+")
            text_file.write(message_data)
            text_file.close()
            os.system("telegram-send --config ./telegram-send.conf '{}'".format(message))

UDP_IP = "0.0.0.0"
UDP_PORT = 33556

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    parse_message(data)

