import os, sys, socket, threading

from time import *

VERSION = 0.1

class Bot():

    def __init__(self):
        self.socket = self.make_socket()

        self.conf = {
            'nick': 'Becky',
            'anick': 'Becky2',

            'real': 'BeckyBot %s' %(VERSION),
            'user': 'BeckyBot',

            'host': 'irc.rizon.net',
            'port': 6667,
            'channels': ['#thefission', '#zanacross', '#thefusion']
        }

        self.porn = Porn()
        self.channels = {}
        self.starttime = time()
        self.lasttime = time()

        self.porntime = 0
        self.pornrun = True

    def make_socket(self):
        return socket.socket(socket.AF_INET, socket.TCP_NODELAY)

    def connect(self):
        self.socket.connect((self.conf['host'], int(self.conf['port'])))
        self.recv()
    def register(self):
        data = "NICK %s" %(self.conf['nick'])
        self.send(data)
        data = "USER %s * 0 :%s" %(self.conf['user'], self.conf['real'])
        self.send(data)

    def send(self, data):
        print '('+asctime(localtime(self.lasttime))+') ->', data
        self.socket.send(data + "\r\n")

    def join(self, chan):
        d = "JOIN %s" %(chan)
        self.send(d)

    def part(self, chan):
        d = "PART %s" %(chan)
        self.send(d)

    def msg(self, dest, message):
        d = "PRIVMSG %s :%s" %(dest, message)
        self.send(d)

    def users(self):
        d = self.channels
        self.socket.send("PRIVMSG #thefission :%s \r\n" %(d))

    def porntimer(self):
        while self.pornrun:
            if time() - self.porntime >= 1800:
                self.porn()

    def recv(self):
        while time() - self.lasttime <= 300:
            data = self.socket.recv(4096)
            data = data.split('\r\n')
            if not data[0] == '':
                print '('+asctime(localtime(self.lasttime))+') <-', data[0]
                parsed = data[0].split(' ')
                if is_num(parsed[1]):
                    self.parse_raw(int(parsed[1]), parsed[2:])
                if ' '.join(parsed[1:len(parsed)]) == "NOTICE AUTH :*** Checking Ident":
                    self.register()
                if parsed[0] == 'ERROR':
                    print "Error Connecting: %s" %(parsed[1:])
                if parsed[0] == 'PING':
                    d = "PONG %s" %(parsed[1])
                    self.send(d)
                if parsed[1] == 'JOIN':
                    self.parse_join(parsed[0], parsed[2])
                if parsed[1] == 'PRIVMSG':
                    user = get_user(parsed[0])
                    self.parse_msg(user, parsed[2], parsed[3:])
                self.lasttime = time()

        print "Disconnected - Reconnecting"
        self.connect()

    def parse_raw(self, raw, message):
        if raw == 439:
            #Connect Raw
            self.register()
            pass
        if raw == 001:
            #welcome
            self.mynick = message[0]
            for i in self.conf['channels']:
                self.join(i)
        if raw == 002:
            pass
        if raw == 352:
            self.channels[message[1]]['nicks'].append(message[5])
        if raw == 315:
            print self.channels

    def parse_msg(self, user, dest, message):
        cmd = message[0].replace(':', '')
        if is_chan(dest):
            #channel
            if cmd == '!porn':
                d = self.porn.porn()
                if d:
                    self.msg(dest, d)
            pass
        else:
            #private
            if user[0] == 'Lord-Harlot':
                if cmd == '!join':
                    self.join(message[1])
                if cmd == '!part':
                    self.part(message[1])
                if cmd == '!porn':
                    self.msg(message[1], self.porn.porn())
                if cmd == '!users':
                    self.users()

    def parse_join(self, user, dest):
        user = get_user(user)
        if user[0] == self.mynick:
            print dest
            self.channels.update({dest.replace(':',''): {'nicks': [], 'porntime': time()}})
            d = "WHO %s" %(dest)
            self.send(d)
    def parse_error(self, error):
        pass

class Porn():
    def __init__(self):
        import sqlite3 as sql
        self.con = sql.connect('porn.db')
        self.cur = self.con.cursor()

        self.url = "http://porn.zananet.info/"

        self.lastused = {}
    def porn(self):
        if time() - self.lastused >= 5:
            self.cur.execute("SELECT * FROM PornLinks ORDER BY RANDOM() LIMIT 1")
            i = self.cur.fetchall()
            image = i[0][1]
            url = self.url + image
            self.lastused = time()
            return '[NSFW] ' + url



def is_num(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

def get_user(user):
    string = user.replace(':', '').split('!')
    nick = string[0]
    string = string[1].split('@')
    user = string[0]
    host = string[1]
    return nick, user, host

def is_chan(chan):
    if chan[:1] == '#':
        return True
    else:
        return False

if __name__ == '__main__':
    bot = Bot()
    bot.connect()
