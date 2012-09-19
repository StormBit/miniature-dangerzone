# protocol module for shadowircd
# Copyright (c) 2012 Samuel Hoffman
import dangerzone

class protocol(dangerzone.dangerzone):
    def __init__(self, me):
        self.me = me
        self.d_table = { 'PASS': self.password}

    def burst(self):
        numeric = self.me.conf.get('serverinfo', 'numeric',
                fallback='00B') # 00A is atheme's default, try 00B
        password = self.me.conf.get('uplink', 'password',
                fallback=None)

        if password is None:
            print('password required for connecting to uplink in dangerzone.conf (uplink/password)')
            return
        else:
            self.me.sts('PASS %s TS 6 :%s' % (password, numeric))

        self.bursting = True

        self.me.sts('CAPAB :QS EX IE KLN UNKLN ENCAP TB SERVICES EUID EOPMOD MLOCK')
        self.me.sts('SERVER ' + self.me.conf.get('serverinfo', 'name') + ' 1 :%s' % self.me.conf.get('serverinfo', 'desc'))
        self.me.sts('SVINFO 6 :%d' % self.me.time())

    def parse(self, data):
        pass

    def password(self, data):
        pass
