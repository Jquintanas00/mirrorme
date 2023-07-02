import threading as t
import time as tt
import socket as s
import sys
import os
import status
import json
from hashlib import sha256


HOST = ("0.0.0.0",80)
dictt = {}
PID = os.getpid()

#ip to where people will connect
external_ip = b"127.0.0.1"

A = s.socket()
A.bind(HOST)
A.listen(0)

B = ""

def parse(stream):
	data = stream.split(b"\r\n")
	dir = data[0].split(b" ")[1]
	count = dir.count(b"/")
	if count > 1:
		dir = dir[:dir[1:].index(b"/") + 1]
	db = json.load(open("wl.json"))
	if dir.decode() in db.keys():
		host = db[dir.decode()]['url']
		path = db[dir.decode()]['path']
	else:
		host = db["/404"]['url']
		path = db["/404"]['path']
	stream = stream.replace(external_ip, host.encode())
	stream = stream.replace(dir, path.encode())
	return host, path, stream

def part1():
	global client,B,status
	count = 0
	try:
	    client.settimeout(999)
	    B.settimeout(999)
	except:
	    exit()
	while status.value == True:
		try:
			asd = client.recv(32568)
		except:
			print ("ERROR,t1",flush=True)
			break
		if asd in [b''] or status.value == False:
			break
		print (asd,flush=True)
		B.send(asd)
		count +=1
	status.value=False
def part2():
	global client,B
	count = 0
	try:
	    client.settimeout(999)
	    B.settimeout(999)
	except:
	    exit()
	while status.value==True:
		try:
			asd = B.recv(32568)
		except:
			print ("ERROR,t1",flush=True)
			break
		if asd in [b''] or status.value == False:
			break
		client.send(asd)
		count +=1
	status.value=False


def the_thing(client,B):
	t1 = t.Thread(target=part1, daemon=True)
	t2 = t.Thread(target=part2, daemon=True)
	t1.start()
	t2.start()
	while status.value==True:
		tt.sleep(1)
		pass

def winbug(*value):
    global client, B
    client = dictt["".join(value)]
    sys.stdin.close()
    host, path, stream = parse(client.recv(3333))
    print("ZZZ: ", host, path)
    B=s.socket()
    B.settimeout(30)
    print (host)
    if "127.0.0.1" in host:
	    B.connect(("127.0.0.1", 8089))
    else:
	    B.connect((host, 80))
    B.send(stream)
    the_thing(client,B)
    client.close()
#B.close()
    A.close()
    tt.sleep(1)
    exit(0)


while True:
	try:
		client,addr = A.accept()
	except :
		A.close()
		tt.sleep(1)
		exit(0)
	value = sha256(str(tt.time()).encode()).hexdigest()
	dictt[value] = client
	t.Thread(target=winbug, args=(value)).start()
A.close()
