# Copyright (c) 2012 Samuel Hoffman

def load(me, path):
     module = __import__(path, fromlist=['src'])
     if module == None:
          print('Could not import', module,':(')
          return
     module._modinit(me)
     return module
