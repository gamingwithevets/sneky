import pygame
import os
import sys
import traceback
import logger

try:

	from game import Game

	g = Game()

	while g.running:
		g.curr_menu.display_menu()
		g.game_loop()

except pygame.error:
	pygame.quit()
	logger.log('Sneky closed because Pygame got an error.\n' + traceback.format_exc() + '\nSneky session closed. (Pygame Error)\n')
	exit()
except KeyboardInterrupt:
	pygame.quit()
	logger.log('Sneky closed due to the user halting execution manually.\n' + traceback.format_exc() + '\nSneky session closed. (KeyboardInterrupt)\n')
	exit()
except Exception as e:
	pygame.quit()
	logger.log('An error has occurred!\n' + traceback.format_exc() + '\nSneky session closed. (' + type(e).__name__ + ')\n')
	exit()