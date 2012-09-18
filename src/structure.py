# structure.py
# builds classes for every class and sub class, starting
# from the top down
#
# Copyright (c) 2012 Samuel Hoffman <sam@minicruzer.com>
import socket, asyncore, asynchat, logging, time, string, random
from inspect import stack

class dangerzone(asynchat.async_chat):
    def __init__(self, host, port):
        self.connections = {}
        self.services = {}
        self.channels = {}
        self.users = {}
        self.servers = {}
        self.hooks = {} # specific event.file caller
        self.sid = '3D0' # TODO

    ########################################
    ####            asyncore            ####
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_terminator('\n')
        self.recvq = []
        self.connect((host, port))

    def handle_connect(self):
        self.run_hook('on_connect')

    def collect_incoming_data(self, data):
        self.recvq.append(data)

    def found_terminator(self):
        self.parse(''.join(self.recvq))
        self.recvq = []
    ####            asyncore            ####
    ########################################

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

        self.uid = self.sid + (''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
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

class channel(dangerzone):
    def __init__(self, name, users, time, topic, topic_time, topic_setter):
        self.name, self.users, self.modes, self.time, self.topic, self.topic_time, self.topic_setter
            = name, {}, modes, time, topic, topic_time, topic_setter

    def user_add(self):         pass
    def user_part(self):        pass

    # channel actions from server
    def mode(self):             pass
    def topic(self):            pass
    def kick(self):             pass
