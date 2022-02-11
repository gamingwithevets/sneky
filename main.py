import pygame
import os
import sys
import traceback
import logger



if os.name == 'nt':
	appdata_path = os.getenv('LOCALAPPDATA') + '\\Sneky'
else:
	if os.geteuid() != 0:
		print('The application data path in Linux (/opt/) is protected by root,\nso you need to use sudo to run this port!')
		sys.exit()
	else:
		print('Since you\'re probably running as root, the player name will\nalways be root, no matter what account you\'re logged into.\nAnyway, enjoy the game!')
		appdata_path = '/opt/Sneky'

if not os.path.exists(appdata_path):
	os.mkdir(appdata_path)
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