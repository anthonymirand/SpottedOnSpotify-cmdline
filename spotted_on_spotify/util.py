import os
import sys
from clint.textui import puts, colored

import conf

def display_intro():
  print_message('''
  __  ____  ____   ___ _____  __    ___ _______   __
 / / / ___||  _ \\ / _ \\_   _| \\ \\  |_ _|  ___\\ \\ / /
| |  \\___ \\| |_) | | | || |    | |  | || |_   \\ V /
| |   ___) |  __/| |_| || |    | |  | ||  _|   | |
| |  |____/|_|    \\___/ |_|    | | |___|_|     |_|
 \\_\\                          /_/

          Welcome to Spotted on Spotify!\n''', color='green')

def print_message(message, color='white', exit=False):
  color_map = {
    'cyan'   : colored.cyan,
    'green'  : colored.green,
    'red'    : colored.red,
    'white'  : colored.white,
    'yellow' : colored.yellow
  }
  puts(color_map[color](message))
  if exit:
    if os.path.isfile(conf.YOUTUBE_DL_OPTS['outtmpl']):
      os.remove(conf.YOUTUBE_DL_OPTS['outtmpl'])
    sys.exit(1)
