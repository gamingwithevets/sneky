import pygame
import os
import sys
import traceback
import logger

if not os.path.exists(os.getenv('LOCALAPPDATA') + '\\Sneky'):
	os.mkdir(os.getenv('LOCALAPPDATA') + '\\Sneky')
sys.path.insert(0, os.getenv('LOCALAPPDATA') + '\\Sneky')

try:

	from game import Game

	g = Game()

	while g.running:
		g.curr_menu.display_menu()
		g.game_loop()

except pygame.error:
	pygame.quit()
	logger.log('Sneky closed because Pygame thrown an error.\n' + traceback.format_exc() + '\nSneky session closed. (pygame.error)\n')
	exit()
except KeyboardInterrupt:
	pygame.quit()
	logger.log('Sneky closed due to the user halting execution manually.\n' + traceback.format_exc() + '\nSneky session closed. (KeyboardInterrupt)\n')
	exit()
except Exception as e:
	pygame.quit()
	logger.log('An error has occurred!\n' + traceback.format_exc() + '\nSneky session closed. (' + type(e).__name__ + ')\n')
	exit()