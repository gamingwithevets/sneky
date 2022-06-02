if __name__ == '__main__':
	print('Please run main.py to start Sneky.')
	sys.exit()

import sys
import os
import platform as platforn
from datetime import datetime

logfile = 'sneky.log'
startuplogged = False

if os.name == 'nt':
	appdata_path = os.getenv('LOCALAPPDATA') + '\\Sneky'
	appdata_path1 = os.getenv('LOCALAPPDATA') + '\\Sneky\\'
else:
	if platforn.system() == 'Darwin':
		appdata_path = os.path.expanduser('~/Library/Application Support/Sneky')
		appdata_path1 = os.path.expanduser('~/Library/Application Support/Sneky/')
	else:
		appdata_path = os.path.expanduser('~/.config/Sneky')
		appdata_path1 = os.path.expanduser('~/.config/Sneky/')

platform = platforn.system()
if platform == 'Darwin':
	platform = 'macOS'

if os.name == 'nt':
	playername = os.getenv('USERNAME')
else:
	playername = os.getenv('USER').upper()

if not os.path.exists(appdata_path):
	os.makedirs(appdata_path)
f = open(appdata_path1 + logfile, 'a', encoding = 'utf8')
print('\n[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] [LOGGER] Sneky logger initialized. Begin logging for this session.')
f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] [LOGGER] Sneky logger initialized. Begin logging for this session.')
print('Player: ' + playername)
f.write('\nPlayer: ' + playername)
print('Log file: ' + appdata_path1 + logfile)
f.write('\n')
f.close()

def log(text, allowprint = True, allowlog = True, tag = 'MAIN'):
	if not os.path.exists(appdata_path):
		os.makedirs(appdata_path)
	if allowprint:
		print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] [' + tag + '] ' + text)
	if allowlog:
		f = open(appdata_path1 + logfile, 'a', encoding = 'utf8')
		f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] [' + tag + '] ' + text)
		f.write('\n')
		f.close()

