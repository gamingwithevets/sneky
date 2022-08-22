import sys
if __name__ == '__main__':
	print('Please run main.py to start Sneky.')
	sys.exit()

logfile = 'sneky.log'

import os
import platform as platforn
from datetime import datetime

def log(text, allowprint = True, allowlog = True, tag = 'MAIN'):
	if not os.path.exists(appdata_path):
		os.makedirs(appdata_path)
	if allowprint:
		print(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] [{tag}] {text}')
	if allowlog:
		with open(appdata_path1 + logfile, 'a', encoding = 'utf8') as f:
			f.write(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] [{tag}] {text}')
			f.write('\n')
			f.close()

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

log(f'Sneky logger initialized. Begin logging for this session.\nLog file: {appdata_path1}{logfile}', allowlog = False, tag = 'LOGGER')
log('Sneky logger initialized. Begin logging for this session.', allowprint = False, tag = 'LOGGER')


