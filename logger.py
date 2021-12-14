import sys
import os
from datetime import datetime

# log file
logfile = 'sneky.log'

def log(text):
	f = open(os.getenv('LOCALAPPDATA') + '\\Sneky\\' + logfile, 'a', encoding = 'utf8')
	print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + text)
	f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + text)
	f.write('\n')
	f.close()

def startuplog(gamestatus, gameversion):
	f = open(os.getenv('LOCALAPPDATA') + '\\Sneky\\' + logfile, 'a', encoding = 'utf8')
	if gamestatus != None and gamestatus != 'release':
		print('\n[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (' + gamestatus + ' ' + gameversion + ')\nBegin logging for this session.')
		f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (' + gamestatus + ' ' + gameversion + ')\nBegin logging for this session.')
	else:
		print('\n[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (v.' + gameversion + ')\nBegin logging for this session.')
		f.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Sneky logger initialized. (v.' + gameversion + ')\nBegin logging for this session.')
	print('Player: ' + os.getenv('USERNAME'))
	f.write('\nPlayer: ' + os.getenv('USERNAME'))
	print('Log file: ' + os.getenv('LOCALAPPDATA') + '\\Sneky\\' + logfile)
	f.write('\n')
	f.close()

if __name__ == '__main__':
	print('This logger is designed for Sneky.')