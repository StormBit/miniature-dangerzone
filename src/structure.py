# structure.py
# builds classes for every class and sub class, starting
# from the top down
#
# Copyright (c) 2012 Samuel Hoffman <sam@minicruzer.com>
import socket, asyncore, asynchat, logging
from inspect import stack

class dangerzone(asynchat.async_chat):
    def __init__(self, host, port):
        self.connections = {}
        self.services = {}
        self.channels = {}
        self.users = {}
        self.servers = {}
        self.hooks = {} # specific event.file caller

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


