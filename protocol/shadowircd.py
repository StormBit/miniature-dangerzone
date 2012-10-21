# protocol module for shadowircd
# Copyright (c) 2012 Samuel Hoffman
import platform

_shadowircd_cmode_list = {
        'i': 'CMODE_INVITE',
        'm': 'CMODE_MOD',
        'n': 'CMODE_NOEXT',
        'p': 'CMODE_PRIV',
        's': 'CMODE_SEC',
        't': 'CMODE_TOPIC',
        'c': 'CMODE_NOCOLOR',
        'r': 'CMODE_REGONLY',
        'z': 'CMODE_OPMOD',
        'g': 'CMODE_FINVITE',
        'L': 'CMODE_EXLIMIT',
        'P': 'CMODE_PERM',
        'F': 'CMODE_FTARGET',
        'Q': 'CMODE_DISFWD',
        'M': 'CMODE_IMMUNE',
        'C': 'CMODE_NOCTCP',
        'A': 'CMODE_ADMINONLY',
        'O': 'CMODE_OPERONLY',
        'Z': 'CMODE_SSLONLY',
        'D': 'CMODE_NOACTIONS',
        'T': 'CMODE_NONOTICE',
        'G': 'CMODE_NOCAPS',
        'E': 'CMODE_NOKICKS',
        'd': 'CMODE_NONICKS',
        'K': 'CMODE_NOREPEAT',
        'J': 'CMODE_KICKNOREJOIN'
}

_shadowircd_cstatus_list = {
        'a': 'CSTATUS_PROTECT',
        'o': 'CSTATUS_OP',
        'h': 'CSTATUS_HALFOP',
        'v': 'CSTATUS_VOICE'
}

_shadowircd_prefix_list = {
        '!': 'CSTATUS_PROTECT',
        '@': 'CSTATUS_OP',
        '%': 'CSTATUS_HALFOP',
        '+': 'CSTATUS_VOICE'
}

_shadowircd_umode_list = {
        'a': 'UF_ADMIN',
        'i': 'UF_INVIS',
        'o': 'UF_IRCOP',
        'D': 'UF_DEAF',
        'p': 'UF_IMMUNE'
}
def get_platform_info():
	info = 'Implementation: ' + platform.python_compiler() + platform.python_implementation() + platform.python_version() \
		+ ' | Platform: ' + platform.platform() + ' ' + platform.processor()
	return info
	
def _shadowircd_login(me):
    me.sts('PASS %s TS 6 :%s' % (me.conf.get('uplink', 'password'), me.conf.get('serverinfo', 'numeric')))
    me.sts('CAPAB :QS EX IE KLN UNKLN ENCAP TB SERVICES EUID EOPMOD MLOCK')
    me.sts('SERVER %s 1 :%s' % (me.conf.get('serverinfo', 'name'), me.conf.get('serverinfo', 'desc') + ' ' + get_platform_info()))
    me.sts('SVINFO 6 6 0 :%d' % me.time())

def _shadowircd_pass(me, *stream):
    pass

_shadowircd_dispatch_t = {
        'PASS': _shadowircd_pass
}

class ShadowIRCd:
    def __init__(self):
        self.name = 'ShadowIRCd 6+'
        self.tld = '$$'
        self.owner = None
        self.protect = '+a'
        self.halfop = '+h'
        self.oper_only_cmode = ['CMODE_EXLIMIT', 'CMODE_PERM', 'CMODE_IMMUNE']
        self.perm_cmode = ['CMODE_PERM']
        self.umode_list = _shadowircd_umode_list
        self.cmode_list = _shadowircd_cmode_list
        self.cstatus_list = _shadowircd_cstatus_list
        self.prefix_list = _shadowircd_prefix_list
        self.login = _shadowircd_login
        self.dispatch_t = _shadowircd_dispatch_t

def _modinit(me):
    print('using shadowircd as protocol module')
    me.protocol = ShadowIRCd()

