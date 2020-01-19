import binascii


class InnerFile:
    def __init__(self, innerFile):
        self.length = innerFile['length']
        self.splitpath = innerFile['path']
        self.path = '/' + '/'.join(innerFile['path'])

    def printer(self):
        print "\t\t", self.length, self.path
        

class BitTorrentFileInfo:
    def __init__(self,fileInfo):
        self.name = fileInfo['name']
        self.piece_length = fileInfo['piece length']
        self.pieces = fileInfo['pieces']
        self.mult = False
        if 'files' in fileInfo:
            files = []
            self.mult = True
            self.private = fileInfo['private']
            for x in fileInfo['files']:
                files.append(InnerFile(x))
            self.files = files
        else:
            self.length = fileInfo['length']


    def printer(self):
        if self.mult:
            print "\t", self.name, " - files"
            print "\tfiles"
            for file in self.files:
                file.printer()
            print "\t\t", self.private
        else: 
            print "\t", self.name, self.length
        
        print "piece length: ", self.piece_length
        s = ''
        print binascii.b2a_hex(self.pieces)


class BitTorrentFile:
    def __init__(self, torrent_data):
        self.announce = torrent_data['announce']
        self.announce_list = torrent_data['announce-list']
        #self.created_by = torrent_data['created by']
        #self.creation_date = torrent_data['creation date']
        self.info = BitTorrentFileInfo(torrent_data['info'])
        

    def printer(self):
        print self.announce, "\n", self.announce_list, 
        self.info.printer()

class BitTorrentPacket:
    def __init__(self):
        self.protocolname = 'BitTorrent protocol'
        self.peer_id = ''
        self.reserved
        self.info_hash
        self.protocolnamelength



