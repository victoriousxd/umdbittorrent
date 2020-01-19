
piecesDict = {}
numPieces = 5
pieceLen = 4
totalLen = 18
lastPieceSize = totalLen % ((numPieces -1) * pieceLen)
offset = 2

def addPiece(index,offset,data):
	if index not in piecesDict:
		piecesDict[index] = {offset:data}
	elif offset not in piecesDict[index]:
		piecesDict[index][offset] = data
	print piecesDict[index]

def returnPiece(index,offset):
	if index in piecesDict and offset in piecesDict[index]:
		return piecesDict[index][offset]

def fullDictionary():
	if len(piecesDict) != numPieces:
		return False
	
	for i in range(0,numPieces-1):
		data = ''
		for j in range(0,pieceLen,offset):
			if j not in piecesDict[i]:
				return False
			data += piecesDict[i][j]
		if len(data) != pieceLen:
			return False
	
	lastdata = ''
	for k in piecesDict[numPieces-1]:
		lastdata += piecesDict[numPieces-1][k]
	if len(lastdata) != lastPieceSize:
		return False
	return True

def printDict():
	for x in piecesDict:
		print x, piecesDict[x]

fullDictionary()

def test():

	for i in range(0,numPieces-1):
		for j in range(0,pieceLen,offset):
			print i,j
			addPiece(i,j,'00')
	
		addPiece(numPieces-1,0,'00')
	printDict()
	print fullDictionary()

test()