# structure.py
# builds classes for every class and sub class, starting
# from the top down
#
# Copyright (c) 2012 Samuel Hoffman <sam@minicruzer.com>
import socket
import asyncore
import asynchat
import logging
import time
import string
import random
import configparser
import os
from src import module
from inspect import stack

class dangerzone(asynchat.async_chat):
    def __init__(self, conffile):
        self.protocol = None
        # ===================================================
        # configparser
        # ===================================================
        self.conf = configparser.ConfigParser(
                { 'Joah': 'faggot' },
                inline_comment_prefixes=(';','//',),
                interpolation=configparser.ExtendedInterpolation(),
                allow_no_value=True
        )
        self.conf.BOOLEAN_STATES = {
                'sure': True,

                'nope': False,
        }
        if len(self.conf.read(conffile)) != 1:
            print('Could not open conffile', conffile)

        # load all modules, load protocol first
        proto = self.conf.get('modules', 'protocol')
        mods = eval(self.conf.get('modules', 'load'))

        module.load(self, proto)

        for i in mods:
            try:
                module.load(self, i)
            except Exception:
                print('could not load module', i)

        # ===================================================
        # configparser
        # ===================================================

        self.connections = {}
        self.services = {}
        self.channels = {}
        self.users = {}
        self.servers = {}
        self.hooks = {}

    # ===================================================
    # asyncore
    # ===================================================
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recvq = []
        self.set_terminator(b'\r\n')
        self.connect((self.conf.get('uplink', 'host'), self.conf.getint('uplink', 'port')))

    def handle_connect(self):
        self.protocol.login(self)
        self.hook_run('on_connect')

    def collect_incoming_data(self, data):
        data = data.decode('utf-8') # this is so dumb
        print('R:', data)
        self.recvq.append(data)

    def found_terminator(self):
         line = ''.join(self.recvq)
         parv = line.split(' ')

         if parv[0] in self.protocol.dispatch_t:
             self.protocol.dispatch_t[parv[0]](self, parv)

         self.recvq = []

    def sts(self, data):
        print('S:', data)
        data = data + '\n'
        data = data.encode('utf-8') # back to bytes before sending
        self.push(data)
    # ===================================================
    # asyncore
    # ===================================================

    def modload(self, path):
        module = __import__('src.%s' % path, fromlist=['src'])
        module._modinit()

    def time(self):
        return int(time.time())

    def service_add(self):      pass
    def service_del(self):      pass

    def channel_add(self):      pass
    def channel_del(self):      pass

    def user_add(self):         pass
    def user_del(self):         pass

    def service_add(self):      pass
    def service_del(self):      pass

    def hook_add(self, hook):
        self.hooks[hook.events] = hook

    def hook_del(self):         pass
    def hook_run(self, event, *args):
        for events, hook in self.hooks:
            for _event in events:
                if _event == event:
                    hook.dispatch[event](hook, args)

class service(dangerzone):
    def __init__(self, nick, user, host, gecos):
        self.nick, self.user, self.host, self.gecos = nick, user, host, gecos
        self.commands = {}
        self.hooks = {}
        self.channels = {}
        self.modes = {}

        self.uid = self.sid + (''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6)))
        self.time = int(time())

    # command interface. if there aren't any commands, we're just going to ignore everything
    def command_add(self):      pass
    def command_del(self):      pass
    def command_exec(self):     pass

    def hook_add(self):         pass
    def hook_del(self):         pass
    def hook_run(self):         pass

    ## commands a service can potentially do. goal: be able to almost everything
    # message types: priority should be user, then channel
    def msg(self):              pass
    def notice(self):           pass
    def ctcp(self):             pass
    def me(self):               pass

    # actions against other users
    def kill(self):             pass
    def kick(self):             pass

    # channel actions
    def topic(self):            pass
    def join(self):
        self.channel_add()
    def part(self):
        self.channel_del()
    def channel_add(self):      pass
    def channel_del(self):      pass

    # misc
    def mode(self):             pass # should this be broken down to cmode and umode?
    def quit(self):             pass
    def oper(self):             pass

    # checking for things
    def has_mode(self, type):   pass
    def is_in(self, chan):      pass
    def is_oper(self):
        return self.has_mode('IRC_OPERATOR')

class channel(dangerzone):
    def __init__(self, name, users, time, topic, topic_time, topic_setter):
        self.name, self.users, self.modes, self.time, self.topic, self.topic_time, self.topic_setter = name, {}, modes, time, topic, topic_time, topic_setter

    def user_add(self):         pass
    def user_part(self):        pass

    # channel actions from server
    def mode(self):             pass
    def topic(self):            pass
    def kick(self):             pass
    def notice(self):           pass
    def msg(self):              pass # experimental

class user(dangerzone):
    def __init__(self, numeric, nick, time, modes, user, host, uid, gecos):
        self.numeric, self.nick, self.time, self.modes, self.user, self.host, self.uid = numeric, nick, time, modes, user, host, uiid

        self.channels = {}

    # when user joins/parts a channel
    def channel_add(self):      pass
    def channel_del(sefl):      pass

    # actions server can take against user
    def kill(self):             pass
    def ban(self):              pass

    # message types
    def sno(self):              pass
    def notice(self):           pass
    def msg(self):              pass # experimental

class protocol(dangerzone):
    def __init__(self,
            name,               # str
            tld,
            oper_only_cmode,
            cflag_owner,
            cflag_protect,
            cflag_halfop,
            permanent_cmode,
            cmode_list,
            umode_list,
            status_list,
            prefix_list,
            dispatch_t):

        self.name = name
        self.tld = tld
        self.oper_only_cmode = oper_only_cmode
        self.cflag_owner = cflag_owner
        self.cflag_protect = clfag_protect
        self.permant_cmode = permanent_cmode
        self.cmode_list = cmode_list
        self.umode_list = umode_list

    def parse(self, line):
        # split line into an array
        parv = line.split(' ')

        if parv[0] in self.dispatch_t:
            self.dispatch_t[parv[0]](self, parv)

def main(conffile):
    global me

    me = dangerzone(conffile)

    asyncore.loop()
