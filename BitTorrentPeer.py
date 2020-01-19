import socket
import sys
from threading import Thread 
from SocketServer import ThreadingMixIn 
import errno
import os
import random
import errno
import binascii
from struct import pack, unpack, error as unpack_exception


def printBuffer(data):
    if (len(data) < 1):
        return
    for byte in data:
        print(byte.encode('hex')),
    

class PeerManager:
	def __init__(self,peers):
		self.peers = peers

class Peer:
# all Peers in class
	peerList = []
# length of 1 piece
	pieceLen = 0
# length of whole file
	totalLen = 0
# list of current pieces 
	listOfTorrentPieces = {}
# piece index 
	listOfPieceOffsets = []
# list of pieces to request
	whatWeNeed = []
# list of pieces that were requested
	requested = []
	peers = []
	torrentinfo = ""
	d = {}
	peerID = ""
	@classmethod
	def retrieveSockets(cls):
		return [p.sock for p in Peer.peerList]
	
	def __init__(self, peerinfo ):
		self.peer_id = peerinfo['peer id']
		self.ip = peerinfo['ip']
		self.port = peerinfo['port']
		self.themchoked = False # did they choke us
		self.uschoked = False  # did we choke them 
		self.interested = 0
		self.owned_pieces = []
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(10)
		self.connected = False
		self.bad = False


# symmetric handshake 
	def handshake(self):
		try:
			self.sock.connect((self.ip, self.port))
			
			bytesToSend = bytearray()

			bytesToSend.append(0x13)
			toSend = "BitTorrent protocol00000000"
			bytesToSend.extend(bytearray(toSend, 'utf-8'))

			toSend = toSend + Peer.torrentinfo

			bytesToSend.extend(bytearray(Peer.torrentinfo))

			toSend = toSend + str(Peer.peerID)
			digits = [int(d) for d in str(Peer.peerID)]
			bytesToSend.extend(bytearray(digits))

			toSend = "0019" + toSend
			#print(arr) 
			# 19 - bittorrent protocol - reserved extension bytes
			ok = "\x13" + "\x42\x69\x74\x54\x6f\x72\x72\x65\x6e\x74\x20\x70\x72\x6f\x74\x6f\x63\x6f\x6c" + "\x00\x00\x00\x00\x00\x10\x00\x05"
			# torrent info - Victoria's peerid (taken from bittorrent)
			ok += bytearray(Peer.torrentinfo) + "\x4d\x37\x2d\x34\x2d\x33\x2d\x2d\x15\xab\x84\xf0\x4c\x3d\xed\xe5\x55\x4d\xe8\x6c"
			self.sock.sendall(ok)
			data = self.sock.recv(68)
			print(len(data))
			print('Received', repr(data))
			self.connected = True
			#parse the response
			# if handshake complete send interested message
			self.sock.send('\x00\x00\x00\x01\x02')
			# if successful interested message, append to peerList
			if not self.bad:
				Peer.peerList.append(self)
		# if error, close 
		except socket.error as e:
			self.bad = True
			print(e)

	# make peer request Payload of given piece & offset
	def requestPayload(self, piece, offset):
		payload = bytearray(bytes(pack('>IBIII', 13,6,piece,offset, Peer.pieceLen % 1200)))
		# pack constructs byte array
		# pack('>IBIII', 1,2,3) = '\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03'
		#printBuffer(payload)

		print(binascii.hexlify(payload))
		self.sock.send(payload)

		
	# generic send message 
	def sendMessage(self,length, value, payload):
		try: 
			message = bytearray()
			for i in range(4-(len(str(length)))):
				message.append(0x00)
			message.append(length)
			message.append(value)
			#append payload
			if payload != None:
				for i in range(length-len(payload)):
					message.append(0x00)
				message.extend(bytearray(payload))

			print(binascii.hexlify(message))
			self.sock.sendall(message)
		except socket.error as e:
			self.bad = True
			print(e)


# if piece not in dictionary:
# 	dictionary[piece] = piece[offset] = {}
# 	size(dcition.keys()) == piece 


