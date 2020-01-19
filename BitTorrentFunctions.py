import sys
import bencode
import urllib3
import hashlib
import urllib
import socket
import select


def symetricHandshake(sock, peerIP, peerPort, torrentinfo, peerID):
	try:
		sock.connect((peerIP, peerPort))
		
		bytesToSend = bytearray()

		bytesToSend.append(0x13)
		toSend = "BitTorrent protocol00000000"
		bytesToSend.extend(bytearray(toSend, 'utf-8'))

		toSend = toSend + torrentinfo

		bytesToSend.extend(bytearray(torrentinfo))

		toSend = toSend + str(peerID)
		digits = [int(d) for d in str(peerID)]
		bytesToSend.extend(bytearray(digits))

		toSend = "0019" + toSend
		#print(arr)
		sock.sendall(bytesToSend)
		data = sock.recv(68)
		print('Received', repr(data))
		#parse the response
		
	except socket.error:
		pass

def getClients(dictionary):
	clientsData = dictionary['peers']
	#print(type(clientsData))

	if str(type(clientsData)) == "<type 'list'>":
		return clientsData
	else:
		data = list(clientsData)
		toReturn = []
		for i in xrange(0,len(data)/6):
			newClient = {
				"peer id" : "",
				"ip" : "",
				"port" : 0,
				"choked" : 0,
				"interested" : 0,
				"owned pieces" : []
			}
			#newClient["ip"] += data[0+(i*6)]
			#newClient["ip"] += data[1+(i*6)]
			#newClient["ip"] += data[2+(i*6)]
			#newClient["ip"] += data[3+(i*6)]
			newClient["ip"] = socket.inet_ntoa(data[0+(i*6)] + data[1+(i*6)] + data[2+(i*6)] + data[3+(i*6)])
#['\xb9', '\x15', '\xd9', '\x08', '\xd0', '\x06', '\xb9', '\x15', '\xd9', '\x12', '\xdf', 'L', '\xb9', '\xcb', ...]
			#print(data[4+(i*6)])
			
			newClient["port"]+= (int(data[4+(i*6)].encode('hex'), 16)) << 8
			#newClient["port"]+= (int(data[4+(i*6)]) << 8)
			newClient["port"]+= (int(data[5+(i*6)].encode('hex'), 16))
			#newClient["port"]+= (int(data[5+(i*6)]))
			toReturn.append(newClient)
		return toReturn

def getPeerFromSocket(socket, peerList):
	for x in xrange(0,len(peerList)):
		if peerList[x]["socket"] == socket:
			return peerList[x]