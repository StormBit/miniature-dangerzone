#!/usr/bin/env python3
import sys

sys.path.append('..')

from src import dangerzone
if __name__ == '__main__':
    dangerzone.main('../etc/dangerzone.conf')

