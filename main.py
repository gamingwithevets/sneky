import sys

# python + pygame version requirements
python_requirement = '3.8.0'
pygame_requirement = '2.0.0'

import platform
if platform.python_version() < python_requirement:
	if platform.python_version() < '3.10.0':
		print('Oops! Your Python version is too old.\n')
		print('Requirement: Python ' + python_requirement + '+\nYou have   : Python ' + platform.python_version())
		print('\nGet a newer version!')
		sys.exit()

try:
	import pygame
except:
	print('You don\'t have Pygame! How can you run Pygame games WITHOUT Pygame????')
	print('Did you forget to "pip install pygame"?')
	print('\nIf this happened on a binary YOU compiled, you probably didn\'t do it before\ncompiling. So do it and recompile! ;)')
	print('\nIf that didn\'t work, PLEASE report it here:\nhttps://github.com/gamingwithevets/sneky/issues')
	sys.exit()

if pygame.version.ver < pygame_requirement:
	print('Oops! Your Python version is too old.\n')
	print('Requirement: Pygame ' + pygame_requirement + '+\nYou have   : Pygame ' + pygame.version.ver)
	print('\nGet a newer version!')
	sys.exit()

import os
import traceback
import logger

if os.name == 'nt':
	appdata_path = os.getenv('LOCALAPPDATA') + '\\Sneky'
elif os.name == 'posix':
	if platform.system() != 'Darwin':
		appdata_path = os.path.expanduser('~/.config/Sneky')
	else:
		print('It appears you are running the game on a Mac! Keep in mind that\nthis macOS port may have problems!\nIf you found any, PLEASE report it here:\nhttps://github.com/gamingwithevets/sneky/issues')
		print('Using ~/Library/Application Support/Sneky as appdata path.\nIf it can\'t write there, please report it via the URL above.')
		appdata_path = os.path.expanduser('~/Library/Application Support/Sneky')
 
if not os.path.exists(appdata_path):
	os.makedirs(appdata_path)
sys.path.insert(0, appdata_path)

try: 
	from game import Game

	g = Game()

	while g.running:
		g.curr_menu.display_menu()
		g.game_loop()

except pygame.error:
	pygame.quit()
	logger.log('Sneky closed because Pygame thrown an error.\n' + traceback.format_exc() + '\nSneky session closed. (pygame.error)\n')
	sys.exit()
except KeyboardInterrupt:
	pygame.quit()
	logger.log('Sneky closed due to the user halting execution manually.\n' + traceback.format_exc() + '\nSneky session closed. (KeyboardInterrupt)\n')
	sys.exit()
except Exception as e:
	pygame.quit()
	logger.log('An error has occurred!\n' + traceback.format_exc() + '\nSneky session closed. (' + type(e).__name__ + ')\n')
	sys.exit()