import sys
import os
import platform
from datetime import datetime

logfile = 'sneky.log'
startuplogged = False

if os.name == 'nt':
	appdata_path = os.getenv('LOCALAPPDATA') + '\\Sneky'
	appdata_path1 = os.getenv('LOCALAPPDATA') + '\\Sneky\\'
else:
	appdata_path = '/opt/Sneky'
	appdata_path1 = '/opt/Sneky/'

platform = platform.system()
if platform == 'Darwin':
	platform = 'macOS'

if os.name == 'nt':
	playername = os.getenv('USERNAME')
else:
	playername = os.getenv('USER').upper()

def log(text, allowprint = None):
	if not os.path.exists(appdata_path):
		os.mkdir(appdata_path)
	f = open(appdata_path1 + logfile, 'a', encoding = 'utf8')
	if allowprint != False:
		print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + text)
	f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + text)
	f.write('\n')
	f.close()

def startuplog(gamestatus, gameversion):
	global startuplogged
	if not startuplogged:
		if not os.path.exists(appdata_path):
			os.mkdir(appdata_path)
		f = open(appdata_path1 + logfile, 'a', encoding = 'utf8')
		if (gamestatus or gamestatus != None) and gamestatus != 'release':
			print('\n[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (' + gamestatus + ' ' + gameversion, end = '')
			f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (' + gamestatus + ' ' + gameversion)
		else:
			print('\n[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (v.' + gameversion, end = '')
			f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (v.' + gameversion)
		if platform != 'Windows':
			print(' [' + platform + ' port])')
			f.write(' [' + platform + ' port])')
		else:
			print(')')
			f.write(')')
		print('Begin logging for this session.')
		f.write('\nBegin logging for this session.')
		print('Player: ' + playername)
		f.write('\nPlayer: ' + playername)
		print('Log file: ' + appdata_path1 + logfile)
		f.write('\n')
		f.close()
		startuplogged = True

if __name__ == '__main__':
	print('This logger is designed for Sneky.')