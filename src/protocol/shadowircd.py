class protocol:
    def __init__(self):
        self.umodes = {
            'IRC_OPERATOR': 'o',

        }
        self.cmodes = {
            'INVITE': 'i',
            'SECRET': 's',
            'SSL': 'S',
            'STRIP': 'c',
            'PRIVATE': 'p',
            'KICKNOREJOIN': 'J',
            'NOREPEAT': 'K',
            'NOEXT': 'n',
            'TOPIC': 't',
            'MODERATED': 'm',
            'REGONLY': 'r',
            'NONICK': 'd',
            'FREE': 'g',
            'OPMOD': 'z',
            'BANLIST': 'L',
        }

    def burst(self):          pass
    def parse(self, data):    pass
