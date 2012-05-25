from . import *

import sys
from argparse import ArgumentParser

if version[0] == 0:
  #dev version: 0, major, minor, year, tag
  verfmt = '%d.%d.%d:%d-%s'
else:
  #release version: year, major, minor
  verfmt = '%d.%d.%d'

cmdparser = ArgumentParser(description='Convert text to Braille')

cmdparser.add_argument('-d', '--debug', action='store_true',
    help='turn on warnings and debug messages')
cmdparser.add_argument('--version', action='version',
    version=verfmt % version,
    help='display the current version of the software.')

guiopt = cmdparser.add_mutually_exclusive_group()
guiopt.add_argument('-gui', '--gui', action='store_true',
    default=True, help='use the gui interface')
guiopt.add_argument('-cmd', '--cmdline', action='store_false',
    dest='gui', help='use the command line interface')
guiopt.add_argument('--tests', action='store_true',
    help='run package tests, then exit')

args = cmdparser.parse_args()

options.override(vars(args))

if opt('tests'):
  import unittest
  import unittest.runner

  tests = unittest.defaultTestLoader.discover('braille.tests', pattern='test*.py')
  runner = unittest.runner.TextTestRunner()
  runner.run(tests)

elif opt('gui'):
  from . import gui
  gui.__main__()
else:
  oline = ""
  while (True):
    line = sys.stdin.readline()

    oline = convert(line)

    #Helps readability on monospace outputs--like a terminal
    oline = oline.replace('', ' ')

    print oline.strip()
    oline = ''