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

def log(text, allowprint = True, allowlog = True):
	if not os.path.exists(appdata_path):
		os.makedirs(appdata_path)
	if allowprint:
		print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + text)
	if allowlog:
		f = open(appdata_path1 + logfile, 'a', encoding = 'utf8')
		f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + text)
		f.write('\n')
		f.close()

def startuplog(gamestatus, gameversion):
	global startuplogged
	if not startuplogged:
		if not os.path.exists(appdata_path):
			os.makedirs(appdata_path)
		f = open(appdata_path1 + logfile, 'a', encoding = 'utf8')
		print('\n[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized.', end = '')
		f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized.')
		if platform != 'Windows':
			print(' (' + platform + ' port)\nBegin logging for this session.')
			f.write(' (' + platform + ' port)\nBegin logging for this session.')
		else:
			print(' Begin logging for this session.')
			f.write(' Begin logging for this session.')
		print('Player: ' + playername, end = '')
		f.write('\nPlayer: ' + playername)
		print(' - Log file: ' + appdata_path1 + logfile)
		f.write('\n')
		f.close()
		startuplogged = True

if __name__ == '__main__':
	print('This logger is designed for Sneky.')