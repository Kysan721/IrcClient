import socket
from time import sleep
import threading

class QueueSystem:
    def __init__(self, ircClient):
        self.requests = []
        self.client = ircClient
        threading.Thread(target=self.handleRequests)
    
    def addRequestToQueue(self, request):
        requests.append(request)

    def handleRequests(self):
        while 1:
            try:
                self.client.irc.send(bytes(self.requests[0] + '\r\n', 'utf-8'))
                self.requests = self.requests[1:]   #on enleve la requette qui viend d'être executé        
                sleep(2)        # on attend 2 secondes pour pas ce faire restrict
            except:
                sleep(1)        # pour pas que ça prenne tout mon cpu
                
class BanchoIRCClient:
    def __init__(self, nick, password=''):
        self.server = 'irc.ppy.sh'
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((self.server, 6667))
        
        self.qs = QueueSystem(self)

        self.nick = nick
        self.password = password
        if password != '':
            self.sendRawMessageWithoutQueue('PASS ' + password)
        self.sendRawMessageWithoutQueue('NICK ' + nick)
        self.sendRawMessageWithoutQueue('USER ' + nick + ' ' + nick)
        threading.Thread(target=self.handleMessages).start()

    def sendRawMessageWithoutQueue(self, msg):
        self.irc.send(bytes(msg + '\r\n', 'utf-8'))

    def sendRawMessage(self, msg):
        self.qs.addRequestToQueue(msg)

    def getRawMessage(self):
        return self.irc.recv(2040).decode('utf-8')


    def joinChannel(self, channelName):
        self.sendRawMessage('JOIN ' + channelName)

    def handleMessages(self):
        while 1:
            msg = self.getRawMessage()
            print(msg)
            if msg.find('PING') != -1:
                self.sendRawMessage('PONG ' + msg.split()[1])
            #else if msg.split()[-2] == "QUIT" faut faire une event pour les quit
            else:
                threading.Thread(target=self.onRawMessage, args=(msg,)).start()
                
    def onRawMessage(self, rawMessage):
        print('new raw message : {}'.format(rawMessage))

    def sendMessage(self, target, message):
        pass
    
    def listUsersOnChannel(self, channelName):
        pass    # command NAME à uttilisé

    def onPrivateMessage(self):
        pass
    
    def onChannelMessage(self):
        pass


bot = BanchoIRCClient('Kysan721', '<pass>')
