import sys
if __name__ == '__main__':
	print('Please run main.py to start Sneky.')
	sys.exit()

logfile = 'sneky.log'

import os
from datetime import datetime

def log(text, allowprint = True, allowlog = True, tag = 'MAIN', print_blank = False):
	if not os.path.exists(appdata_path): os.makedirs(appdata_path)
	lines = text.split('\n')
	blank_string = '                         '
	for j in range(len(tag)): blank_string += ' '
	for i in range(len(lines)):
		if i == 0:
			if allowprint:
				if print_blank: print(f'{blank_string}{lines[i]}')
				else: print(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] [{tag}] {lines[0]}')
			if allowlog:
				with open(appdata_path1 + logfile, 'a', encoding = 'utf8') as f:
					if print_blank: f.write(f'{blank_string}{lines[i]}')
					else: f.write(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] [{tag}] {lines[0]}')
					f.write('\n')
					f.close()
		elif i > 0:
			if allowprint: print(f'{blank_string}{lines[i]}')
			if allowlog:
				with open(appdata_path1 + logfile, 'a', encoding = 'utf8') as f:
					f.write(f'{blank_string}{lines[i]}')
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

log(f'Sneky logger initialized. Begin logging for this session.\nLog file: {appdata_path1}{logfile}', allowlog = False, tag = 'LOGGER')
log('Sneky logger initialized. Begin logging for this session.', allowprint = False, tag = 'LOGGER')


