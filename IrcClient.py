import socket
import time
import threading

"""

a faire:

géré quand il n'y a plus de message (l'erreur ou on ce fait spam la prendre comme un déconnection)

"""


def id_to_nick(id):
    return id.split("!")[0].strip(":")



class IrcClient():
    def __init__(self, nick, hostname, chan, port=6667):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((hostname, port))
        self.nickname = nick
        self.chan = chan
        print("connected")

        self.IRCConnect(nick)       #on ce connecte avec le protocole irc
        time.sleep(2)
        self.startMainLoop()     #on start la mainloop qui vas analysé les messages pour voir si c'est: un ping, un msg public, privée

    def send_msg(self, msg):
        self.socket.send(str(msg +"\r\n").encode())
        #toujours terminés par une paire CR-LF (retour chariot - saut de ligne)
    
    def recv_msg(self):
        msg = str(self.socket.recv(4096).decode())
        if msg.find('PING') != -1:
            print("ping")                    
            self.send_msg('PONG ' + msg.split() [1]) 
        return msg
        #510 caractères autorisés
    
    def nick(self, nick):
        self.nickname = nick
        self.send_msg("NICK :" + self.nickname)

    def user(self, nick):
        self.send_msg("USER "+ nick +" * * :"+ nick)
    
    def join(self, chan):
        self.send_msg("JOIN :#harem")

    def IRCConnect(self, nick):
        """
        1. Message PASS -   x
        2. Message NICK
        3. Message USER
        """
        #on fait pas de PASS parceque pas de pass
        self.nick(nick)
        print(self.recv_msg())      # il y a un ping ici il faut le traiter sinon on ce fait rejeter
        self.user(nick)
        
    #def on_nickname_alredy_in_use():

    def on_public_msg(self, envoyeur, channelName, message):
        print(envoyeur +" on "+ channelName + ": "+ message)


    def on_private_msg(self, envoyeur, message):
        print(envoyeur+": "+ message)


    #methode qui analyse le message et appel public_msg ou privat_msg 
    def startMainLoop(self):
        print("mainloop started")
        
        self.join(self.chan)
        while(True):
            msg = self.recv_msg()
            split_msg = msg.split(" ")
            if len(split_msg) >= 4:
                envoyeur = id_to_nick(split_msg[0])
                methode = split_msg[1]
                destinataire = split_msg[2]   
                message = "".join(split_msg[3:])[1:]




            if 
            # si le message est pour moi(ex: 
            # :Kysan!Kysan@hzv-v9a.poj.93u6l5.IP PRIVMSG azerty12 :exemple
            if destinataire == self.nickname:
                threading.Thread(target=self.on_private_msg, args=(envoyeur, message)).start()
                

            # idem qu'avant 
            # :Kysan!Kysan@hzv-v9a.poj.93u6l5.IP PRIVMSG #harem :exemple
            elif destinataire == self.chan:
                #self.on_public_msg(envoyeur, destinataire, message)
                threading.Thread(target=self.on_public_msg, args=(envoyeur, destinataire, message)).start()