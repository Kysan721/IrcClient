import IrcClient


class Bot(IrcClient.IrcClient):
    def __init__(self, nick, hostname, chan, port=6667, senpai)):
        IrcClient.IrcClient(nick, hostname, chan)