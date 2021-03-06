if __name__ == '__main__':
	print('Please run main.py to start Sneky.')
	sys.exit()

import pygame
import sys
import os
import time
import logger, updater
import shutil
import random
from datetime import datetime
import webbrowser

class Menu():
	def __init__(self, game):
		self.game = game
		self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0,0, self.game.font_size, self.game.font_size)
		self.offset = -200

	def draw_cursor(self, size = 30):
		self.game.draw_text('→', size, self.cursor_rect.x, self.cursor_rect.y, font_name = self.game.arrow_font)

	def blit_screen(self):
		self.game.update_fps()
		self.game.window.blit(self.game.display, (0,0))
		pygame.display.update()
		self.game.reset_keys()

class MainMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = "LAUNCH GAME"
		self.startx, self.starty = self.mid_w, int(self.mid_h + self.game.font_size * 3/2)
		self.optionsx, self.optionsy = self.mid_w, int(self.mid_h + self.game.font_size * 5/2)
		self.creditsx, self.creditsy = self.mid_w, int(self.mid_h + self.game.font_size * 7/2)
		self.quitx, self.quity = self.mid_w, int(self.mid_h + self.game.font_size * 9/2)
		self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

		self.menumousex = (int(self.mid_w - 180), int(self.mid_w + 175))
		self.startmousey = (int(self.mid_h - 33), int(self.mid_h + 65))
		self.optionsmousey = (int(self.mid_h + 66), int(self.mid_h + 100))
		self.creditsmousey = (int(self.mid_h + 101), int(self.mid_h + 130))
		self.quitmousey = (int(self.mid_h + 131), int(self.mid_h + 160))

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('MAIN MENU', self.game.font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - self.game.font_size)
			self.game.draw_text('LAUNCH GAME', self.game.font_size, self.startx, self.starty)
			self.game.draw_text('SETTINGS', self.game.font_size, self.optionsx, self.optionsy)
			self.game.draw_text('CREDITS', self.game.font_size, self.creditsx, self.creditsy)
			self.game.draw_text('QUIT', self.game.font_size, self.quitx, self.quity)
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'LAUNCH GAME':
				self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
				self.state = 'OPTIONS'

			elif self.state == 'OPTIONS':
				self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
				self.state = 'CREDITS'

			elif self.state == 'CREDITS':
				self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
				self.state = 'QUIT'

			elif self.state == 'QUIT':
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = 'LAUNCH GAME'
			self.game.DRsnd_menumove.play()

		if self.game.UP_KEY:
			if self.state == 'LAUNCH GAME':
				self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
				self.state = 'QUIT'

			elif self.state == 'OPTIONS':
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = 'LAUNCH GAME'

			elif self.state == 'CREDITS':
				self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
				self.state = 'OPTIONS'

			elif self.state == 'QUIT':
				self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
				self.state = 'CREDITS'
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.startmousey) and self.state != 'LAUNCH GAME':
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = 'LAUNCH GAME'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.optionsmousey) and self.state != 'OPTIONS':
				self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
				self.state = 'OPTIONS'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.creditsmousey) and self.state != 'CREDITS':
				self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
				self.state = 'CREDITS'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.quitmousey) and self.state != 'QUIT':
				self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
				self.state = 'QUIT'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.START_KEY:
			if self.state == 'LAUNCH GAME':
				self.game.curr_menu = self.game.mode_menu
			elif self.state == 'OPTIONS':
				self.game.curr_menu = self.game.options
			elif self.state == 'CREDITS':
				self.game.curr_menu = self.game.credits
			elif self.state == 'QUIT':
				self.game.running = False
				self.run_display = False
				self.game.DRsnd_select.play()
				logger.log('Sneky session closed.\n')
				pygame.quit()
				sys.exit()
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.BACK_KEY:
			self.run_display = False
			self.game.DRsnd_select.play()
			self.game.curr_menu = self.game.press_start
		elif self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.startmousey):
				self.game.curr_menu = self.game.mode_menu
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.optionsmousey):
				self.game.curr_menu = self.game.options
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.creditsmousey):
				self.game.curr_menu = self.game.credits
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.quitmousey):
				self.game.running = False
				self.run_display = False
				self.game.DRsnd_select.play()
				logger.log('Sneky session closed.\n')
				pygame.quit()
				sys.exit()
			self.run_display = False

class OptionsMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self,game)
		self.state = 'VIDEO'
		self.videox, self.videoy = self.mid_w, self.mid_h + self.game.font_size
		self.volx, self.voly = self.mid_w, self.mid_h + self.game.font_size *2
		self.controlsx, self.controlsy = self.mid_w, self.mid_h + self.game.font_size *3
		self.updatex, self.updatey = self.mid_w, self.mid_h + self.game.font_size *4
		self.clearx, self.cleary = self.mid_w, self.mid_h + self.game.font_size *5
		self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)

		self.menumousex = (int(self.mid_w - 100), int(self.mid_w + 95))
		self.videomousey = (int(self.mid_h + 20), int(self.mid_h + 50))
		self.volmousey = (int(self.mid_h + 50), int(self.mid_h + 80))
		self.controlsmousey = (int(self.mid_h + 80), int(self.mid_h + 110))
		self.updatemousey = (int(self.mid_h + 110), int(self.mid_h + 140))
		self.clearmousey = (int(self.mid_h + 140), int(self.mid_h + 170))

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('SETTINGS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size * 3/2) 
			self.game.draw_text('VIDEO', int(self.game.font_size * 3/4), self.videox, self.videoy)
			self.game.draw_text('VOLUME', int(self.game.font_size * 3/4), self.volx, self.voly) 
			self.game.draw_text('CONTROLS', int(self.game.font_size * 3/4), self.controlsx, self.controlsy)
			self.game.draw_text('UPDATES', int(self.game.font_size * 3/4), self.updatex, self.updatey)
			self.game.draw_text('CLEAR DATA', int(self.game.font_size * 3/4), self.clearx, self.cleary)
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'VIDEO':
				self.state = 'VOLUME'
				self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
			elif self.state == 'VOLUME':
				self.state = 'CONTROLS'
				self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
			elif self.state == 'CONTROLS':
				self.state = 'UPDATES'
				self.cursor_rect.midtop = (self.updatex + self.offset, self.updatey)
			elif self.state == 'UPDATES':
				self.state = 'CLEAR'
				self.cursor_rect.midtop = (self.clearx + self.offset, self.cleary)
			elif self.state == 'CLEAR':
				self.state = 'VIDEO'
				self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)
			self.game.DRsnd_menumove.play()
		if self.game.UP_KEY:
			if self.state == 'VIDEO':
				self.state = 'CLEAR'
				self.cursor_rect.midtop = (self.clearx + self.offset, self.cleary)
			elif self.state == 'CLEAR':
				self.state = 'UPDATES'
				self.cursor_rect.midtop = (self.updatex + self.offset, self.updatey)
			elif self.state == 'UPDATES':
				self.state = 'CONTROLS'
				self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
			elif self.state == 'CONTROLS':
				self.state = 'VOLUME'
				self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
			elif self.state == 'VOLUME':
				self.state = 'VIDEO'
				self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.videomousey) and self.state != 'VIDEO':
				self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)
				self.state = 'VIDEO'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.volmousey) and self.state != 'VOLUME':
				self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
				self.state = 'VOLUME'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.controlsmousey) and self.state != 'CONTROLS':
				self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
				self.state = 'CONTROLS'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.updatemousey) and self.state != 'UPDATES':
				self.cursor_rect.midtop = (self.updatex + self.offset, self.updatey)
				self.state = 'UPDATES'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.clearmousey) and self.state != 'CLEAR':
				self.cursor_rect.midtop = (self.clearx + self.offset, self.cleary)
				self.state = 'CLEAR'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'CONTROLS':
				self.game.curr_menu = self.game.controls
			elif self.state == 'VIDEO':
				self.game.curr_menu = self.game.videomenu
			elif self.state == 'VOLUME':
				self.game.curr_menu = self.game.volumemenu
			elif self.state == 'UPDATES':
				self.game.curr_menu = self.game.updatemenu
			elif self.state == 'CLEAR':
				self.game.curr_menu = self.game.clear_data
			self.run_display = False
		elif self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.videomousey):
				self.game.curr_menu = self.game.videomenu
				self.game.DRsnd_select.play()
			if self.game.mousey in range(*self.volmousey):
				self.game.curr_menu = self.game.volumemenu
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.controlsmousey):
				self.game.curr_menu = self.game.controls
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.updatemousey):
				self.game.curr_menu = self.game.updatemenu
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.clearmousey):
				self.game.DRsnd_select.play()
				self.game.curr_menu = self.game.clear_data
			self.run_display = False

class ClearData(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.state = 'saved'
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 10
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 40
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)

		self.menumousex = (int(self.mid_w - 165), int(self.mid_w + 160))
		self.opt1mousey = (int(self.mid_h), int(self.mid_h + 20))
		self.opt2mousey = (int(self.mid_h + 30), int(self.mid_h + 50))
		self.opt3mousey = (int(self.mid_h + 60), int(self.mid_h + 80))

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('CLEAR DATA', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('CLEAR SAVED SETTINGS', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text('CLEAR SESSION LOGS', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text('CLEAR EVERYTHING', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
			self.draw_cursor(int(self.game.font_size / 2))
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'saved':
				self.state = 'logs'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'logs':
				self.state = 'all'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'all':
				self.state = 'saved'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'saved':
				self.state = 'all'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'all':
				self.state = 'logs'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'logs':
				self.state = 'saved'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey) and self.state != 'saved':
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
				self.state = 'saved'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt2mousey) and self.state != 'logs':
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				self.state = 'logs'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt3mousey) and self.state != 'all':
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'all'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'saved':
				self.run_display = False
				self.clear_data2()
			elif self.state == 'logs':
				self.run_display = False
				self.clear_data2(False, True)
			elif self.state == 'all':
				self.run_display = False
				self.clear_data2(True, True)

		if self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey):
				self.game.DRsnd_select.play()
				self.run_display = False
				self.clear_data2()
			elif self.game.mousey in range(*self.opt2mousey):
				self.game.DRsnd_select.play()
				self.run_display = False
				self.clear_data2(False, True)
			elif self.game.mousey in range(*self.opt3mousey):
				self.game.DRsnd_select.play()
				self.run_display = False
				self.clear_data2(True, True)

	def clear_data2(self, cleardata = True, clearlogs = False):
		self.clear2_run_display = True
		while self.clear2_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY:
				self.clear2_run_display = False
				self.game.DRsnd_select.play()
				self.run_display = True
			elif self.game.START_KEY:
				self.clear2_run_display = False
				self.game.DRsnd_select.play()
				self.clear_data3(cleardata, clearlogs)
				break
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('CLEAR DATA', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			if cleardata:
				self.game.draw_text('WARNING! You are about to clear all saved data and settings.', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, color = self.game.red, font_name = self.game.menu2_font)
				if clearlogs:
					self.game.draw_text('You\'re also clearing all your session logs.', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text('This cannot be undone!', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CLEAR EVERYTHING'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CANCEL'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 110, font_name = self.game.menu2_font)
				else:
					self.game.draw_text('This cannot be undone!', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CLEAR ALL SAVED DATA'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 70, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CANCEL'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
			elif clearlogs:
				self.game.draw_text('WARNING! You are about to clear all your session logs.', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, color = self.game.red, font_name = self.game.menu2_font)
				self.game.draw_text('This cannot be undone!', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, color = self.game.red, font_name = self.game.menu2_font)
				self.game.draw_text('{0}: CLEAR ALL SESSION LOGS'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 70, font_name = self.game.menu2_font)
				self.game.draw_text('{0}: CANCEL'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
			self.blit_screen()

	def clear_data3(self, cleardata = True, clearlogs = False):
		self.clear3_run_display = True
		while self.clear3_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY:
				self.clear3_run_display = False
				self.game.DRsnd_select.play()
				self.run_display = True
			elif self.game.START_KEY:
				self.clear3_run_display = False
				self.game.DRsnd_select.play()
				self.clear_data(cleardata, clearlogs)
				break
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('CLEAR DATA', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			if cleardata:
				if clearlogs:
					self.game.draw_text('Are you REALLY sure you wanna clear EVERYTHING?', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CLEAR EVERYTHING'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CANCEL'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 110, font_name = self.game.menu2_font)
				else:
					self.game.draw_text('Are you REALLY sure you wanna clear your data?', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CLEAR ALL SAVED DATA'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 70, font_name = self.game.menu2_font)
					self.game.draw_text('{0}: CANCEL'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
			elif clearlogs:
				self.game.draw_text('Are you REALLY sure you wanna clear all session logs?', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, color = self.game.red, font_name = self.game.menu2_font)
				self.game.draw_text('{0}: CLEAR ALL SESSION LOGS'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 70, font_name = self.game.menu2_font)
				self.game.draw_text('{0}: CANCEL'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
			self.game.draw_text('THIS IS YOUR LAST WARNING!', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, color = self.game.red, font_name = self.game.menu2_font)
			self.blit_screen()

	def clear_data(self, cleardata = True, clearlogs = False):
		if os.path.exists(self.game.appdata_path):
			if os.path.exists(self.game.appdata_path + self.game.settings_fn):
				if cleardata: os.remove(self.game.appdata_path + self.game.settings_fn)
			if os.path.exists(self.game.appdata_path + logger.logfile):
				if clearlogs: os.remove(self.game.appdata_path + logger.logfile)
		print('The following has been cleared:')
		if cleardata: print('- Saved settings and data')
		if clearlogs: print('- Session logs')
		if cleardata:
			print('Sneky session closed.')
			pygame.quit()
			sys.exit()
		else:
			self.clear4_run_display = True
			while self.clear4_run_display:
				self.game.reset_keys()
				self.game.check_events()
				if self.game.BACK_KEY:
					self.clear4_run_display = False
					self.game.DRsnd_select.play()
					self.run_display = True
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('CLEAR DATA', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
				self.game.draw_text('All session logs have been cleared.', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, color = self.game.red, font_name = self.game.menu2_font)
				self.game.draw_text('{0}: BACK'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50, font_name = self.game.menu2_font)
				self.blit_screen()

class CreditsMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			if self.game.BACK_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
				self.game.DRsnd_select.play()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('CREDITS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('Menu & Music/SFX Injection: GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, font_name = self.game.menu2_font)
			self.game.draw_text('Menu Template: ChristianD37 - Mode Menu: SeverusFate', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, font_name = self.game.menu2_font)
			self.game.draw_text('Game & Image Injection: SeverusFate & GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50, font_name = self.game.menu2_font)
			self.game.draw_text('Crash Handler & Logger: GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 70, font_name = self.game.menu2_font)
			self.game.draw_text('Snake & Title Screen Images: GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 110, font_name = self.game.menu2_font)
			self.game.draw_text('Sounds from DELTARUNE, Google Snake Game, SMB2 USA, SMB3, Brain Age', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 130, font_name = self.game.menu2_font)
			self.game.draw_text('Music:', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 150, font_name = self.game.menu2_font)
			if self.game.holiday:
				if self.game.holiday == 'christmas_exclusive/':
					self.game.draw_text('Candy Cone Image: Kandi Patterns - Santa Hat: John3 from TopPNG', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
					self.game.draw_text('\"Jingle Bells\" - From YouTube/KON', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 170, font_name = self.game.menu2_font)
					self.game.draw_text('\"We Wish You A Merry Christmas\"', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 190, font_name = self.game.menu2_font)
					self.game.draw_text('From YouTube/Pudding TV - Nursery Rhymes', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 210, font_name = self.game.menu2_font)
					self.game.draw_text('Made with: Pygame', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 250, font_name = self.game.menu2_font)
			else:
				self.game.draw_text('Apple Image: Luna4s', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
				self.game.draw_text('Wii Menu Music - Nintendo', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 170, font_name = self.game.menu2_font)
				self.game.draw_text('\"Nothing to Say\" - Md Abdul Kader Zilani', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 190, font_name = self.game.menu2_font)
				self.game.draw_text('Made with: Pygame', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 230, font_name = self.game.menu2_font)
			self.blit_screen()

class VideoMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.state = 'fullscreen'
		self.set_values()
		self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)

	def set_values(self):
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 10
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 40
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.opt4x, self.opt4y = self.mid_w, self.mid_h + 100
		self.opt5x, self.opt5y = self.mid_w, self.mid_h + 130

		self.menumousex = (int(self.mid_w - 165), int(self.mid_w + 160))
		self.opt1mousey = (int(self.mid_h), int(self.mid_h + 20))
		self.opt2mousey = (int(self.mid_h + 30), int(self.mid_h + 50))
		self.opt3mousey = (int(self.mid_h + 60), int(self.mid_h + 80))
		self.opt4mousey = (int(self.mid_h + 90), int(self.mid_h + 110))
		self.opt5mousey = (int(self.mid_h + 120), int(self.mid_h + 140))

	def display_menu(self):
		self.run_display = True
		self.fullscreen = self.game.fullscreen
		self.scaled = self.game.scaled
		self.native_res = self.game.native_res

		while self.run_display:
			if self.fullscreen: self.fullscreen_str = 'ON'
			else: self.fullscreen_str = 'OFF'
			if self.scaled: self.scaled_str = 'ON'
			else: self.scaled_str = 'OFF'
			if self.native_res: self.native_res_str = 'ON'
			else: self.native_res_str = 'OFF'
			if self.game.fullscreen:
				if self.game.scaled: self.curr_setting = 'Fullscreen, Scaled'
				else:
					if self.game.native_res: self.curr_setting = 'Fullscreen, Native Resolution'
					else: self.curr_setting = 'Fullscreen'
			else: 
				if self.game.native_res: self.curr_setting = 'Windowed, Native Resolution'
				else: self.curr_setting = 'Windowed'
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('VIDEO', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('Fullscreen: {0}'.format(self.fullscreen_str), int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			if not self.fullscreen:
				self.game.draw_text('Scaled Mode: {0}'.format(self.scaled_str), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font, color = self.game.gray)
			else:
				self.game.draw_text('Scaled Mode: {0}'.format(self.scaled_str), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			if self.scaled and self.fullscreen:
				self.game.draw_text('Native Resolution ({0}x{1}): {2}'.format(self.game.current_w, self.game.current_h, self.native_res_str), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font, color = self.game.gray)
			else:
				self.game.draw_text('Native Resolution ({0}x{1}): {2}'.format(self.game.current_w, self.game.current_h, self.native_res_str), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
			self.game.draw_text('APPLY SETTINGS', int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
			self.game.draw_text('RESET TO DEFAULTS', int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
			self.game.draw_text('Current window setting: {0}'.format(self.curr_setting), int(self.game.font_size / 2), self.opt4x, self.opt4y + 70, font_name = self.game.menu2_font)
			self.game.save_settings()
			self.draw_cursor(int(self.game.font_size / 2))
			self.blit_screen()


	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'fullscreen':
				if not self.fullscreen:
					self.state = 'native'
					self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				else:
					self.state = 'scaled'
					self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'scaled':
				if self.scaled and self.fullscreen:
					self.state = 'apply'
					self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				else:
					self.state = 'native'
					self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'native':
				self.state = 'apply'
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'apply':
				self.state = 'reset'
				self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
			elif self.state == 'reset':
				self.state = 'fullscreen'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'fullscreen':
				self.state = 'reset'
				self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
			elif self.state == 'reset':
				self.state = 'apply'
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'apply':
				if self.scaled and self.fullscreen:
					self.state = 'scaled'
					self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				else:
					self.state = 'native'
					self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'native':
				if not self.fullscreen:
					self.state = 'fullscreen'
					self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
				else:
					self.state = 'scaled'
					self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'scaled':
				self.state = 'fullscreen'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey) and self.state != 'fullscreen':
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
				self.state = 'fullscreen'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt2mousey) and self.state != 'scaled' and self.fullscreen:
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				self.state = 'scaled'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt3mousey) and self.state != 'native' and (not self.scaled or not self.fullscreen):
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'native'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt4mousey) and self.state != 'apply':
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				self.state = 'apply'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt5mousey) and self.state != 'reset':
				self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				self.state = 'reset'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'fullscreen':
				self.fullscreen = not self.fullscreen
			elif self.state == 'scaled' and self.fullscreen:
				self.scaled = not self.scaled
			elif self.state == 'native' and (not self.scaled or (self.scaled and not self.fullscreen)):
				self.native_res = not self.native_res
			elif self.state == 'apply':
				if self.fullscreen == self.game.fullscreen and self.scaled == self.game.scaled and self.native_res == self.game.native_res:
					should_continue = False
				else: should_continue = True
				if self.fullscreen and not self.scaled and not self.native_res:
					should_continue = self.noscale_warning()
				elif (not self.fullscreen and self.game.fullscreen) or (self.native_res and not self.game.native_res):
					should_continue = self.native_warning()
				if should_continue:
					self.game.fullscreen = self.fullscreen
					self.game.scaled = self.scaled
					self.game.native_res = self.native_res
					self.game.window = self.game.set_window_mode()
					self.game.init_menus()
					self.game.mode()
					Menu.__init__(self, self.game)
					self.set_values()
					self.set_cursor_pos()
					self.game.change_volume()
			elif self.state == 'reset':
				if self.game.fullscreen == True and self.game.scaled == True and self.game.native_res == True:
					should_continue = False
				else: should_continue = True
				if should_continue:
					self.game.fullscreen = True
					self.game.scaled = True
					self.game.native_res = True
					self.fullscreen = self.game.fullscreen
					self.scaled = self.game.scaled
					self.native_res = self.game.native_res
					self.game.window = self.game.set_window_mode()
					self.game.init_menus()
					self.game.mode()
					Menu.__init__(self, self.game)
					self.set_values()
					self.set_cursor_pos()
					self.game.change_volume()

		if self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey):
				self.game.DRsnd_select.play()
				self.fullscreen = not self.fullscreen
			elif self.game.mousey in range(*self.opt2mousey) and self.fullscreen:
				self.game.DRsnd_select.play()
				self.scaled = not self.scaled
			elif self.game.mousey in range(*self.opt3mousey) and (not self.scaled or not self.fullscreen):
				self.game.DRsnd_select.play()
				self.native_res = not self.native_res
			elif self.game.mousey in range(*self.opt4mousey):
				self.game.DRsnd_select.play()
				if self.fullscreen == self.game.fullscreen and self.scaled == self.game.scaled and self.native_res == self.game.native_res:
					should_continue = False
				else: should_continue = True
				if self.fullscreen and not self.scaled and not self.native_res:
					should_continue = self.noscale_warning()
				elif (not self.fullscreen and self.game.fullscreen) or (self.native_res and not self.game.native_res):
					should_continue = self.native_warning()
				if should_continue:
					self.game.fullscreen = self.fullscreen
					self.game.scaled = self.scaled
					self.game.native_res = self.native_res
					self.game.window = self.game.set_window_mode()
					self.game.init_menus()
					self.game.mode()
					Menu.__init__(self, self.game)
					self.set_values()
					self.set_cursor_pos()
					self.game.change_volume()
			elif self.game.mousey in range(*self.opt5mousey):
				self.game.DRsnd_select.play()
				if self.game.fullscreen == True and self.game.scaled == True and self.game.native_res == True:
					should_continue = False
				else: should_continue = True
				if should_continue:
					self.game.DRsnd_select.play()
					self.game.fullscreen = True
					self.game.scaled = True
					self.game.native_res = True
					self.game.window = self.game.set_window_mode()
					self.game.init_menus()
					self.game.mode()
					Menu.__init__(self, self.game)
					self.set_values()
					self.set_cursor_pos()
					self.game.change_volume()

	def set_cursor_pos(self):
		if self.state == 'apply': self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
		elif self.state == 'reset': self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)

	def noscale_warning(self):
		self.noscale_run_display = True
		while self.noscale_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY:
				self.noscale_run_display = False
				self.game.DRsnd_select.play()
				return False
			elif self.game.START_KEY:
				self.noscale_run_display = False
				self.game.DRsnd_select.play()
				return True
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('VIDEO', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('WARNING! Fullscreen without scaled mode and native', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, font_name = self.game.menu2_font)
			self.game.draw_text('resolution may cause screen issues!', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, font_name = self.game.menu2_font)
			self.game.draw_text('Are you sure you want to continue?', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: YES'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: NO'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 110, font_name = self.game.menu2_font)
			self.blit_screen()

	def native_warning(self):
		self.native_run_display = True
		while self.native_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY:
				self.native_run_display = False
				self.game.DRsnd_select.play()
				return False
			elif self.game.START_KEY:
				self.native_run_display = False
				self.game.DRsnd_select.play()
				return True
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('VIDEO', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('NOTE: If you see that the text/screen is too small, you', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, font_name = self.game.menu2_font)
			self.game.draw_text('probably should switch to fullscreen with scaled mode.', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, font_name = self.game.menu2_font)
			self.game.draw_text('Do you want to apply this setting?', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: YES'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: NO'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 110, font_name = self.game.menu2_font)
			self.blit_screen()

class UpdateMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.state = 'check'
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 10
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 40
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)

		self.menumousex = (int(self.mid_w - 165), int(self.mid_w + 160))
		self.opt1mousey = (int(self.mid_h), int(self.mid_h + 20))
		self.opt2mousey = (int(self.mid_h + 30), int(self.mid_h + 50))
		self.opt3mousey = (int(self.mid_h + 60), int(self.mid_h + 80))

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			if self.game.auto_update: self.auto_str = 'ON'
			else: self.auto_str = 'OFF'
			if self.game.check_prerelease: self.prer_str = 'ON'
			else: self.prer_str = 'OFF'
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('UPDATES', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('CHECK FOR UPDATES'.format(round(self.game.musicvol * 100)), int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text('Automatically Check for Updates: {0}'.format(self.auto_str), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text('Check Prerelease Versions: {0}'.format(self.prer_str), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
			self.game.save_settings()
			self.draw_cursor(int(self.game.font_size / 2))
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'check':
				self.state = 'auto'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'auto':
				self.state = 'prer'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'prer':
				self.state = 'check'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'check':
				self.state = 'prer'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'prer':
				self.state = 'auto'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'auto':
				self.state = 'check'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey) and self.state != 'check':
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
				self.state = 'check'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt2mousey) and self.state != 'auto':
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				self.state = 'auto'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt3mousey) and self.state != 'prer':
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'prer'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'check':
				self.game.curr_menu = self.game.updater
				self.run_display = False
			elif self.state == 'auto':
				self.game.auto_update = not self.game.auto_update
			elif self.state == 'prer':
				self.game.check_prerelease = not self.game.check_prerelease

		if self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey):
				self.game.DRsnd_select.play()
				self.game.curr_menu = self.game.updater
				self.run_display = False
			elif self.game.mousey in range(*self.opt2mousey):
				self.game.DRsnd_select.play()
				self.game.auto_update = not self.game.auto_update
			elif self.game.mousey in range(*self.opt3mousey):
				self.game.DRsnd_select.play()
				self.game.check_prerelease = not self.game.check_prerelease


class Updater(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'install'
		self.opt0x, self.opt0y = self.mid_w, self.mid_h +  10
		self.opt1x, self.opt1y = self.mid_w, self.mid_h +  40 
		self.opt2x, self.opt2y = self.mid_w, self.mid_h +  70
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 100
		self.opt4x, self.opt4y = self.mid_w, self.mid_h + 130
		self.opt5x, self.opt5y = self.mid_w, self.mid_h + 160
		self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
		
	def display_menu(self, auto = False):
		self.run_display = True
		self.auto = auto
		if self.run_display:
			if self.auto and self.game.updatechecked:
				self.run_display = False
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('UPDATES', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2) 
			self.game.draw_text('Checking for updates. Please wait...', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
			if self.auto: self.game.draw_text('To disable automatic updates, please go to Settings -> Updates.', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.blit_screen()
			self.updstat = updater.check_updates(self.game.gameversion, self.game.check_prerelease)
			if self.updstat['newupdate']: self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)	
			while self.run_display:
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('UPDATES', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
				self.game.check_events()
				if self.updstat['error']:
					if not self.auto:
						if (self.game.START_KEY or self.game.BACK_KEY) or (self.game.CLICK and self.game.mousex in range(235, 560) and self.game.mousey in range(321, 340)):
							if not self.auto: self.game.curr_menu = self.game.updatemenu
							self.game.updatechecked = True
							self.run_display = False
							self.game.DRsnd_select.play()
						if self.updstat['exceeded']:
							self.game.draw_text('GitHub API rate limit exceeded! Please try again later.', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
						elif self.updstat['nomodule']:
							self.game.draw_text('Please install the "requests" module! Use "pip install requests".', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
						elif self.updstat['nowifi']:
							self.game.draw_text('Hmmm... can you check your Internet connection?', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
						else:
							self.game.draw_text('Can\'t check for updates! Please try again later.', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
						if self.auto: self.game.draw_text('MAIN MENU', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
						else: self.game.draw_text('BACK', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
					else:
						self.game.updatechecked = True
						rself.run_display = False
				elif self.updstat['newupdate']:
					self.check_input()
					self.game.draw_text('An update is available!', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
					self.game.draw_text('v.' + self.updstat['tag_name'] + ' - ' + self.updstat['title'], int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
					self.game.draw_text('VISIT DOWNLOAD PAGE', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
					self.game.draw_text('REMIND ME LATER', int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
				elif self.updstat['unofficial']:
					self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
					if (self.game.START_KEY or self.game.BACK_KEY) or (self.game.CLICK and self.game.mousex in range(235, 560) and self.game.mousey in range(421, 440)):
						if not self.auto: self.game.curr_menu = self.game.updatemenu
						self.game.updatechecked = True
						self.run_display = False
						self.game.DRsnd_select.play()
					self.game.draw_text('This is an unofficial or development version of Sneky.', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
					self.game.draw_text('If this is a Sneky mod and you\'re the developer, please', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
					self.game.draw_text('change the "username" and "reponame" variables in updater.py to', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
					self.game.draw_text('your GitHub username and the repository of your mod respectively.', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
					if self.auto: self.game.draw_text('MAIN MENU', int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
					else: self.game.draw_text('BACK', int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
				else:
					if not self.auto:
						if (self.game.START_KEY or self.game.BACK_KEY) or (self.game.CLICK and self.game.mousex in range(235, 560) and self.game.mousey in range(361, 380)):
							self.game.curr_menu = self.game.updatemenu
							self.game.updatechecked = True
							self.run_display = False
							self.game.DRsnd_select.play()
						self.game.draw_text('You are already running the latest version of Sneky!', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
						self.game.draw_text('BACK', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
					else:
						self.game.updatechecked = True
						self.run_display = False
				self.draw_cursor(int(self.game.font_size / 2))
				self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY or self.game.UP_KEY:
			if self.state == 'install':
				self.state = 'remind'
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'remind':
				self.state = 'install'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(235, 560):
			if self.game.mousey in range(381, 400) and self.state != 'install':
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'install'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(401, 420) and self.state != 'remind':
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				self.state = 'remind'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			if not self.auto:
				self.game.curr_menu = self.game.updatemenu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'install':
				self.download()
			elif self.state == 'remind':
				self.game.updatechecked = True
				if not self.auto:
					self.game.curr_menu = self.game.updatemenu
				self.run_display = False

		if self.game.CLICK and self.game.mousex in range(235, 560):
			if self.game.mousey in range(381, 400):
				self.game.DRsnd_select.play()
				self.download()
			elif self.game.mousey in range(401, 420):
				self.game.DRsnd_select.play()
				self.game.updatechecked = True
				if not self.auto:
					self.game.curr_menu = self.game.updatemenu
				self.run_display = False

	def download(self):
		webbrowser.open_new_tab('https://github.com/gamingwithevets/sneky/releases/tag/v' + self.updstat['tag_name'])

class VolumeMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.state = 'master'
		self.mastervolx, self.mastervoly = self.mid_w, self.mid_h + 10
		self.musicvolx, self.musicvoly = self.mid_w, self.mid_h + 40
		self.soundvolx, self.soundvoly = self.mid_w, self.mid_h + 70
		self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('VOLUME', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('MASTER VOLUME: {0}%'.format(round(self.game.volume * 100)), int(self.game.font_size * 3/4), self.mastervolx, self.mastervoly, font_name = self.game.menu2_font)
			self.game.draw_text('MUSIC: {0}%'.format(round(self.game.musicvol * 100)), int(self.game.font_size * 3/4), self.musicvolx, self.musicvoly, font_name = self.game.menu2_font)
			self.game.draw_text('SOUND: {0}%'.format(round(self.game.soundvol * 100)), int(self.game.font_size * 3/4), self.soundvolx, self.soundvoly, font_name = self.game.menu2_font)
			self.game.save_settings()
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'master':
				self.state = 'music'
				self.cursor_rect.midtop = (self.musicvolx + self.offset, self.musicvoly)
			elif self.state == 'music':
				self.state = 'sound'
				self.cursor_rect.midtop = (self.soundvolx + self.offset, self.soundvoly)
			elif self.state == 'sound':
				self.state = 'master'
				self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'master':
				self.state = 'sound'
				self.cursor_rect.midtop = (self.soundvolx + self.offset, self.soundvoly)
			elif self.state == 'sound':
				self.state = 'music'
				self.cursor_rect.midtop = (self.musicvolx + self.offset, self.musicvoly)
			elif self.state == 'music':
				self.state = 'master'
				self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(235, 560):
			if self.game.mousey in range(295, 325) and self.state != 'master':
				self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)
				self.state = 'master'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(326, 355) and self.state != 'music':
				self.cursor_rect.midtop = (self.musicvolx + self.offset, self.musicvoly)
				self.state = 'music'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(356, 385) and self.state != 'sound':
				self.cursor_rect.midtop = (self.soundvolx + self.offset, self.soundvoly)
				self.state = 'sound'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'master':
				self.mastervol()
			elif self.state == 'music':
				self.musicvol()
			elif self.state == 'sound':
				self.soundvol()

		if self.game.CLICK and self.game.mousex in range(235, 560):
			if self.game.mousey in range(295, 325):
				self.game.DRsnd_select.play()
				self.mastervol()
			elif self.game.mousey in range(326, 355):
				self.game.DRsnd_select.play()
				self.musicvol()
			elif self.game.mousey in range(356, 385):
				self.game.DRsnd_select.play()
				self.soundvol()

	def mastervol(self):
		self.mv_run_display = True
		while self.mv_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.mv_run_display = False
				self.game.DRsnd_select.play()
			elif self.game.DOWN_KEY or self.game.MOUSESLIDERDOWN:
				self.game.volume -= 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.UP_KEY or self.game.MOUSESLIDERUP:
				self.game.volume += 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.LEFT_KEY:
				self.game.volume -= 0.05
				self.game.DRsnd_menumove.play()
			elif self.game.RIGHT_KEY:
				self.game.volume += 0.05
				self.game.DRsnd_menumove.play()
			if self.game.volume > 1:
				self.game.volume = 1
			elif self.game.volume < 0:
				self.game.volume = 0
			self.game.change_volume()
			self.game.save_settings()

			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('VOLUME', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('MASTER VOLUME: {0}%'.format(round(self.game.volume * 100)), int(self.game.font_size * 3/4), self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: -1% - {1}: +1% - {2}: -5% - {3}: +5%'.format(pygame.key.name(self.game.UP_BIND).upper(), pygame.key.name(self.game.DOWN_BIND).upper(), pygame.key.name(self.game.LEFT_BIND).upper(), pygame.key.name(self.game.RIGHT_BIND).upper()), 15, self.game.DISPLAY_W / 2, self.mastervoly + 25, font_name = self.game.menu2_font)
			self.game.draw_text('Or, use your mouse slider', 15, self.game.DISPLAY_W / 2, self.mastervoly + 50, font_name = self.game.menu2_font)
			self.blit_screen()

	def musicvol(self):
		self.ms_run_display = True
		while self.ms_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.ms_run_display = False
				self.game.DRsnd_select.play()
			elif self.game.DOWN_KEY or self.game.MOUSESLIDERDOWN:
				self.game.musicvol -= 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.UP_KEY or self.game.MOUSESLIDERUP:
				self.game.musicvol += 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.LEFT_KEY:
				self.game.musicvol -= 0.05
				self.game.DRsnd_menumove.play()
			elif self.game.RIGHT_KEY:
				self.game.musicvol += 0.05
				self.game.DRsnd_menumove.play()
			if self.game.musicvol > 1:
				self.game.musicvol = 1
			elif self.game.musicvol < 0:
				self.game.musicvol = 0
			self.game.change_volume()
			self.game.save_settings()

			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('VOLUME', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('MUSIC: {0}%'.format(round(self.game.musicvol * 100)), int(self.game.font_size * 3/4), self.musicvolx, self.musicvoly, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: -1% - {1}: +1% - {2}: -5% - {3}: +5%'.format(pygame.key.name(self.game.UP_BIND).upper(), pygame.key.name(self.game.DOWN_BIND).upper(), pygame.key.name(self.game.LEFT_BIND).upper(), pygame.key.name(self.game.RIGHT_BIND).upper()), 15, self.game.DISPLAY_W / 2, self.musicvoly + 25, font_name = self.game.menu2_font)
			self.game.draw_text('Or, use your mouse slider', 15, self.game.DISPLAY_W / 2, self.musicvoly + 50, font_name = self.game.menu2_font)
			self.blit_screen()

	def soundvol(self):
		self.sound_run_display = True
		while self.sound_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.sound_run_display = False
				self.game.DRsnd_select.play()
			elif self.game.DOWN_KEY or self.game.MOUSESLIDERDOWN:
				self.game.soundvol -= 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.UP_KEY or self.game.MOUSESLIDERUP:
				self.game.soundvol += 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.LEFT_KEY:
				self.game.soundvol -= 0.05
				self.game.DRsnd_menumove.play()
			elif self.game.RIGHT_KEY:
				self.game.soundvol += 0.05
				self.game.DRsnd_menumove.play()
			if self.game.soundvol > 1:
				self.game.soundvol = 1
			elif self.game.soundvol < 0:
				self.game.soundvol = 0
			self.game.change_volume()
			self.game.save_settings()

			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('VOLUME', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('SOUND: {0}%'.format(round(self.game.soundvol * 100)), int(self.game.font_size * 3/4), self.soundvolx, self.soundvoly, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: -1% - {1}: +1% - {2}: -5% - {3}: +5%'.format(pygame.key.name(self.game.UP_BIND).upper(), pygame.key.name(self.game.DOWN_BIND).upper(), pygame.key.name(self.game.LEFT_BIND).upper(), pygame.key.name(self.game.RIGHT_BIND).upper()), 15, self.game.DISPLAY_W / 2, self.soundvoly + 25, font_name = self.game.menu2_font)
			self.game.draw_text('Or, use your mouse slider', 15, self.game.DISPLAY_W / 2, self.soundvoly + 50, font_name = self.game.menu2_font)
			self.blit_screen()

class ControlsMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.state = 'enter'
		self.opt0x, self.opt0y = self.mid_w, self.mid_h + 10
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 30
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 50
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.opt4x, self.opt4y = self.mid_w, self.mid_h + 90
		self.opt5x, self.opt5y = self.mid_w, self.mid_h + 110
		self.opt6x, self.opt6y = self.mid_w, self.mid_h + 130
		self.opt7x, self.opt7y = self.mid_w, self.mid_h + 150
		self.opt8x, self.opt8y = self.mid_w, self.mid_h + 170
		self.opt9x, self.opt9y = self.mid_w, self.mid_h + 190
		self.opt10x, self.opt10y = self.mid_w, self.mid_h + 210
		self.cursor_rect.midtop = (self.opt0x + self.offset, self.opt0y)
		self.checks = 0

	def display_menu(self):
		self.run_display = True
		self.game.save_settings()
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('REBIND CONTROLS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('{0} (menu) - Select Option'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Up'.format(pygame.key.name(self.game.UP_BIND).upper()), int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Down'.format(pygame.key.name(self.game.DOWN_BIND).upper()), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Left'.format(pygame.key.name(self.game.LEFT_BIND).upper()), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Right'.format(pygame.key.name(self.game.RIGHT_BIND).upper()), int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} (game) - Toggle AI Snake'.format(pygame.key.name(self.game.X_BIND).upper()), int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} (hold) - Turbo Mode'.format(pygame.key.name(self.game.CTRL_BIND).upper()), int(self.game.font_size / 2), self.opt6x, self.opt6y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Back/Pause'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.opt7x, self.opt7y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} (game over) - New Game'.format(pygame.key.name(self.game.SPACE_BIND).upper()), int(self.game.font_size / 2), self.opt8x, self.opt8y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} (game) - Quit'.format(pygame.key.name(self.game.MENU_BIND).upper()), int(self.game.font_size / 2), self.opt9x, self.opt9y, font_name = self.game.menu2_font)
			self.game.draw_text('RESET TO DEFAULTS', int(self.game.font_size / 2), self.opt10x, self.opt10y, font_name = self.game.menu2_font)
			self.game.save_settings()
			self.draw_cursor(size = int(self.game.font_size / 2))
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'enter':
				self.state = 'up'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			elif self.state == 'up':
				self.state = 'down'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'down':
				self.state = 'left'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'left':
				self.state = 'right'
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'right':
				self.state = 'x'
				self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
			elif self.state == 'x':
				self.state = 'ctrl'
				self.cursor_rect.midtop = (self.opt6x + self.offset, self.opt6y)
			elif self.state == 'ctrl':
				self.state = 'esc'
				self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
			elif self.state == 'esc':
				self.state = 'space'
				self.cursor_rect.midtop = (self.opt8x + self.offset, self.opt8y)
			elif self.state == 'space':
				self.state = 'backspace'
				self.cursor_rect.midtop = (self.opt9x + self.offset, self.opt9y)
			elif self.state == 'backspace':
				self.state = 'reset'
				self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
			elif self.state == 'reset':
				self.state = 'enter'
				self.cursor_rect.midtop = (self.opt0x + self.offset, self.opt0y)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'enter':
				self.state = 'reset'
				self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
			elif self.state == 'reset':
				self.state = 'backspace'
				self.cursor_rect.midtop = (self.opt9x + self.offset, self.opt9y)
			elif self.state == 'backspace':
				self.state = 'space'
				self.cursor_rect.midtop = (self.opt8x + self.offset, self.opt8y)
			elif self.state == 'space':
				self.state = 'esc'
				self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
			elif self.state == 'esc':
				self.state = 'ctrl'
				self.cursor_rect.midtop = (self.opt6x + self.offset, self.opt6y)
			elif self.state == 'ctrl':
				self.state = 'x'
				self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
			elif self.state == 'x':
				self.state = 'right'
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'right':
				self.state = 'left'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'left':
				self.state = 'down'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'down':
				self.state = 'up'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			elif self.state == 'up':
				self.state = 'enter'
				self.cursor_rect.midtop = (self.opt0x + self.offset, self.opt0y)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(190, 610):
			if self.game.mousey in range(300, 320) and self.state != 'enter':
				self.cursor_rect.midtop = (self.opt0x + self.offset, self.opt0y)
				self.state = 'enter'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(321, 340) and self.state != 'up':
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
				self.state = 'up'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(341, 360) and self.state != 'down':
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				self.state = 'down'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(361, 380) and self.state != 'left':
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'left'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(381, 400) and self.state != 'right':
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				self.state = 'right'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(401, 420) and self.state != 'x':
				self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				self.state = 'x'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(421, 440) and self.state != 'ctrl':
				self.cursor_rect.midtop = (self.opt6x + self.offset, self.opt6y)
				self.state = 'ctrl'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(441, 460) and self.state != 'esc':
				self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
				self.state = 'esc'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(461, 480) and self.state != 'space':
				self.cursor_rect.midtop = (self.opt8x + self.offset, self.opt8y)
				self.state = 'space'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(481, 500) and self.state != 'backspace':
				self.cursor_rect.midtop = (self.opt9x + self.offset, self.opt9y)
				self.state = 'backspace'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(501, 520) and self.state != 'reset':
				self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
				self.state = 'reset'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			
			if self.state == 'enter':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (menu) - Select Option'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
				self.game.START_BIND = self.assign_key()
			elif self.state == 'up':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Up'.format(pygame.key.name(self.game.UP_BIND).upper()), int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
				self.game.UP_BIND = self.assign_key()
			elif self.state == 'down':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Down'.format(pygame.key.name(self.game.DOWN_BIND).upper()), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
				self.game.DOWN_BIND = self.assign_key()
			elif self.state == 'left':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Left'.format(pygame.key.name(self.game.LEFT_BIND).upper()), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
				self.game.LEFT_BIND = self.assign_key()
			elif self.state == 'right':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Right'.format(pygame.key.name(self.game.RIGHT_BIND).upper()), int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
				self.game.RIGHT_BIND = self.assign_key()
			elif self.state == 'x':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (game) - Toggle AI Snake'.format(pygame.key.name(self.game.X_BIND).upper()), int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
				self.game.X_BIND = self.assign_key()
			elif self.state == 'ctrl':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (hold) - Turbo Mode'.format(pygame.key.name(self.game.CTRL_BIND).upper()), int(self.game.font_size / 2), self.opt6x, self.opt6y, font_name = self.game.menu2_font)
				self.game.CTRL_BIND = self.assign_key()
			elif self.state == 'esc':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Back/Pause'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.opt7x, self.opt7y, font_name = self.game.menu2_font)
				self.game.BACK_BIND = self.assign_key()
			elif self.state == 'space':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (game over) - New Game'.format(pygame.key.name(self.game.SPACE_BIND).upper()), int(self.game.font_size / 2), self.opt8x, self.opt8y, font_name = self.game.menu2_font)
				self.game.SPACE_BIND = self.assign_key()
			elif self.state == 'backspace':
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (game) - Quit'.format(pygame.key.name(self.game.MENU_BIND).upper()), int(self.game.font_size / 2), self.opt9x, self.opt9y, font_name = self.game.menu2_font)
				self.game.MENU_BIND = self.assign_key()
			elif self.state == 'reset':
				self.game.CTRL_BIND = pygame.K_LCTRL
				self.game.START_BIND = pygame.K_RETURN
				self.game.BACK_BIND = pygame.K_ESCAPE
				self.game.MENU_BIND = pygame.K_BACKSPACE
				self.game.SPACE_BIND = pygame.K_SPACE
				self.game.UP_BIND = pygame.K_UP
				self.game.DOWN_BIND = pygame.K_DOWN
				self.game.LEFT_BIND = pygame.K_LEFT
				self.game.RIGHT_BIND = pygame.K_RIGHT
				self.game.X_BIND = pygame.K_x

		if self.game.CLICK and self.game.mousex in range(190, 610):
			if self.game.mousey in range(300, 320):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (menu) - Select Option'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
				self.game.START_BIND = self.assign_key()
			elif self.game.mousey in range(321, 340):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Up'.format(pygame.key.name(self.game.UP_BIND).upper()), int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
				self.game.UP_BIND = self.assign_key()
			elif self.game.mousey in range(341, 360):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Down'.format(pygame.key.name(self.game.DOWN_BIND).upper()), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
				self.game.DOWN_BIND = self.assign_key()
			elif self.game.mousey in range(361, 380):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Left'.format(pygame.key.name(self.game.LEFT_BIND).upper()), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
				self.game.LEFT_BIND = self.assign_key()
			elif self.game.mousey in range(381, 400):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Move Right'.format(pygame.key.name(self.game.RIGHT_BIND).upper()), int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
				self.game.RIGHT_BIND = self.assign_key()
			elif self.game.mousey in range(401, 420):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (game) - Toggle AI Snake'.format(pygame.key.name(self.game.X_BIND).upper()), int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
				self.game.X_BIND = self.assign_key()
			elif self.game.mousey in range(421, 440):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (hold) - Turbo Mode'.format(pygame.key.name(self.game.CTRL_BIND).upper()), int(self.game.font_size / 2), self.opt6x, self.opt6y, font_name = self.game.menu2_font)
				self.game.CTRL_BIND = self.assign_key()
			elif self.game.mousey in range(441, 460):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} - Back/Pause'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.opt7x, self.opt7y, font_name = self.game.menu2_font)
				self.game.BACK_BIND = self.assign_key()
			elif self.game.mousey in range(461, 480):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (game over) - New Game'.format(pygame.key.name(self.game.SPACE_BIND).upper()), int(self.game.font_size / 2), self.opt8x, self.opt8y, font_name = self.game.menu2_font)
				self.blit_screen()
				self.game.SPACE_BIND = self.assign_key()
			elif self.game.mousey in range(481, 500):
				self.game.DRsnd_select.play()
				self.game.display.blit(self.game.imgMenuBG, (0,0))
				self.game.draw_text('{0} (game) - Quit'.format(pygame.key.name(self.game.MENU_BIND).upper()), int(self.game.font_size / 2), self.opt9x, self.opt9y, font_name = self.game.menu2_font)
				self.game.MENU_BIND = self.assign_key()
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(501, 520):
				self.game.DRsnd_select.play()
				self.game.CTRL_BIND = pygame.K_LCTRL
				self.game.START_BIND = pygame.K_RETURN
				self.game.BACK_BIND = pygame.K_ESCAPE
				self.game.MENU_BIND = pygame.K_BACKSPACE
				self.game.SPACE_BIND = pygame.K_SPACE
				self.game.UP_BIND = pygame.K_UP
				self.game.DOWN_BIND = pygame.K_DOWN
				self.game.LEFT_BIND = pygame.K_LEFT
				self.game.RIGHT_BIND = pygame.K_RIGHT
				self.game.X_BIND = pygame.K_x
				

	def assign_key(self):
		self.game.draw_text('REBIND CONTROLS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
		self.game.draw_text('Press a key within 5 seconds to rebind.', 15, self.opt10x, self.opt10y, font_name = self.game.menu2_font)
		self.blit_screen()
		self.checks = 0
		while self.checks != 5000:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					return event.key
			pygame.time.delay(1)
			self.checks += 1

class PressStart(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)

	def display_menu(self):
		self.run_display = True
		if not self.game.inited:
			self.game.window = self.game.set_window_mode()
			self.game.logo_screen()

			self.game.WIIstart.play()
			self.game.menumus.play(-1)
			self.game.inited = True

		while self.run_display:
			self.game.check_events()
			if self.game.CLICK or self.game.START_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
				self.game.DRsnd_select.play()
				if self.game.auto_update:
					self.game.updater.display_menu(True)
			elif self.game.BACK_KEY:
				self.game.running = False
				self.run_display = False
				logger.log('Sneky session closed.\n')
				pygame.quit()
				sys.exit()	

			self.game.display.blit(self.game.imgMenu, (0,0))
			self.game.draw_text(('v.' + self.game.gameversion), self.game.font_size / 2, 20, self.game.DISPLAY_H - 50, anchor = 'topleft', font_name = self.game.menu2_font)
			self.game.draw_text(self.game.curr_splash, self.game.font_size / 2, int(self.game.DISPLAY_W/2), 20, color = self.game.red_god, font_name = self.game.menu2_font)
			self.game.draw_text('PRESS START', self.game.font_size, int(self.game.DISPLAY_W/2), int(self.game.DISPLAY_H - 130))
			self.blit_screen()

class ModeMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.allState = ['Classic', 'Apple Bag', 'Portal Border', 'Angry Apple', 'Ultimate Snake', 'De Snake Mode', 'Unknown']
		if self.game.holiday:
			if self.game.holiday == 'christmas_exclusive/':
				self.allState[1], self.allState[3] = 'Treat Bag', 'Angry Treat'
		self.stateIndex = 0
		self.state = self.allState[self.stateIndex]
		self.classicx, self.classicy = self.mid_w, self.mid_h + self.game.font_size
		self.appleBagx, self.appleBagy = self.mid_w, self.mid_h + self.game.font_size * 2
		self.portalx, self.portaly = self.mid_w, self.mid_h + self.game.font_size * 3
		self.angryApplex, self.angryAppley = self.mid_w, self.mid_h + self.game.font_size * 4
		self.ultimatex, self.ultimatey = self.mid_w, self.mid_h + self.game.font_size * 5
		self.deSnakex, self.deSnakey = self.mid_w, self.mid_h + self.game.font_size * 6
		self.debugx, self.debugy = self.mid_w, self.mid_h + self.game.font_size * 7
		self.cursor_rect.midtop = (self.classicx + self.offset, self.classicy)

		self.menumousex = (int(self.mid_w - 165), int(self.mid_w + 160))
		self.opt1mousey = (int(self.mid_h), int(self.mid_h + 20))
		self.opt2mousey = (int(self.mid_h + 30), int(self.mid_h + 50))
		self.opt3mousey = (int(self.mid_h + 60), int(self.mid_h + 80))

	def display_menu(self):
		self.game.newmoded = False
		self.game.save_settings()
		self.run_display = True
		self.start_game = False
		self.start_game_debug = False
		self.save_high_score = False
		while self.run_display:
			self.game.save_settings()
			self.game.check_events()
			self.check_input()
			self.game.display.blit(self.game.imgMenuBG, (0,0))
			self.game.draw_text('SELECT A MODE', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text(self.allState[0], self.game.font_size * 3/4, self.classicx, self.classicy)
			if self.game.allowmode0:
				self.game.draw_text(self.allState[1], self.game.font_size * 3/4, self.appleBagx, self.appleBagy)
			if self.game.allowmode1:
				self.game.draw_text(self.allState[2], self.game.font_size * 3/4, self.portalx, self.portaly)
			if self.game.allowmode2:
				self.game.draw_text(self.allState[3], self.game.font_size * 3/4, self.angryApplex, self.angryAppley)
			if self.game.allowmode3:
				self.game.draw_text(self.allState[4], self.game.font_size * 3/4, self.ultimatex, self.ultimatey)
			if self.game.allowmode4:
				self.game.draw_text(self.allState[5], self.game.font_size * 3/4, self.deSnakex, self.deSnakey)
			if self.game.allowsecretmode:
				self.game.draw_text(self.allState[6], self.game.font_size * 3/4, self.debugx, self.debugy)
			if self.stateIndex < 5:
				if self.state == self.allState[1]:
					self.game.draw_text('HIGH SCORE: ' + str(self.game.high_scores['Apple Bag']), self.game.font_size * 3/4, self.mid_w, 100, font_name = self.game.menu2_font)
				elif self.state == self.allState[3]:
					self.game.draw_text('HIGH SCORE: ' + str(self.game.high_scores['Angry Apple']), self.game.font_size * 3/4, self.mid_w, 100, font_name = self.game.menu2_font)
				else:
					self.game.draw_text('HIGH SCORE: ' + str(self.game.high_scores[self.state]), self.game.font_size * 3/4, self.mid_w, 100, font_name = self.game.menu2_font)
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			for state in self.allState:
				if self.state == state:
					self.start_game = True
					if state == 'De Snake Mode':
						logger.log(state + ' loaded.')
					elif state == 'Unknown':
						self.start_game = False
						logger.log('You stepped into the Unknown...')
					else:
						self.save_high_score = True
						logger.log(state + ' Mode loaded.')
					
					if self.state == 'Classic': self.game.mode(); break
					elif self.state == self.allState[1]: self.game.mode(apple_bag = 1); break
					elif self.state == 'Portal Border': self.game.mode(portal_border = 1); break
					elif self.state == self.allState[3]: self.game.mode(angry_apple = 1); break
					elif self.state == 'Ultimate Snake': self.game.mode(snake_instinct = 1); break
					elif self.state == 'Unknown':
						self.game.WIIstart.stop()
						self.debug_mode()
						if not self.start_game_debug: logger.log('You exited the Unknown...')
						break
					else: self.game.mode(1,1,1); break

		elif self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(320, 345):
				self.start_game = True
				self.save_high_score = True
				self.game.mode()
				logger.log('Classic Mode loaded.')
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(345, 380) and self.game.allowmode0:
				self.start_game = True
				self.save_high_score = True
				logger.log(self.allState[1] + ' Mode loaded.')
				self.game.mode(apple_bag = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(380, 415) and self.game.allowmode1:
				self.start_game = True
				self.save_high_score = True
				logger.log('Portal Border Mode loaded.')
				self.game.mode(portal_border = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(415, 445) and self.game.allowmode3:
				self.start_game = True
				self.save_high_score = True
				logger.log(self.allState[3] + ' Mode loaded.')
				self.game.mode(angry_apple = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(445, 475) and self.game.allowmode2:
				self.start_game = True
				self.save_high_score = True
				logger.log('Ultimate Snake Mode loaded.')
				self.game.mode(snake_instinct = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(475, 505) and self.game.allowmode4:
				self.start_game = True
				logger.log('De Snake Mode loaded.')
				self.game.mode(1,1,1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(505, 535) and self.game.allowmode4:
				logger.log('You stepped into the Unknown...')
				self.game.WIIstart.stop()
				self.debug_mode()
				if not self.start_game_debug: logger.log('You exited the Unknown...')

		if self.start_game:
			self.game.playing = True
			self.game.inmenu = False
			self.run_display = False
			self.game.DRsnd_select.play()
			self.game.change_volume()
			self.game.menumus.stop()
			self.game.show_instructions = True
			self.game.save_high_score = self.save_high_score
		elif self.start_game_debug:
			logger.log('SNEKY DEBUG MODE: loaded custom mode. settings:\n portal_border: {0}\n curled_up: {1}\n apple_bag: {2}\n break_border: {3}\n snake_instinct: {4}\n angry_apple: {5}'.format(self.portal_border, self.curled_up, self.apple_bag, self.break_border, self.snake_instinct, self.angry_apple))
			self.game.playing = True
			self.game.inmenu = False
			self.run_display = False
			self.game.change_volume()
			self.game.gamemus.play(-1)

	def move_cursor(self):
		if  self.game.BACK_KEY:
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
		if self.game.DOWN_KEY:
			if self.stateIndex + 1 < len(self.allState):
				self.cursor_rect.midtop = (self.cursor_rect.midtop[0], self.cursor_rect.midtop[1] + self.game.font_size)
				self.stateIndex += 1
				self.state = self.allState[self.stateIndex]
			else:
				self.cursor_rect.midtop = (self.cursor_rect.midtop[0], self.cursor_rect.midtop[1] - self.game.font_size * (len(self.allState) - 1))
				self.stateIndex -= (len(self.allState) - 1)
				self.state = self.allState[self.stateIndex]
			if ((self.stateIndex == 1 and not self.game.allowmode0)
			or (self.stateIndex == 2 and not self.game.allowmode1)
			or (self.stateIndex == 3 and not self.game.allowmode2)
			or (self.stateIndex == 4 and not self.game.allowmode3)
			or (self.stateIndex == 5 and not self.game.allowmode4)
			or (self.stateIndex == 6 and not self.game.allowsecretmode)):
				self.cursor_rect.midtop = (self.classicx + self.offset, self.classicy)
				self.stateIndex = 0
				self.state = self.allState[0]
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(235, 560):
			if self.game.mousey in range(320, 345) and self.stateIndex != 0:
				self.cursor_rect.midtop = (self.classicx + self.offset, self.classicy)
				self.stateIndex = 0
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(345, 380) and self.stateIndex != 1 and self.game.allowmode0:
				self.cursor_rect.midtop = (self.appleBagx + self.offset, self.appleBagy)
				self.stateIndex = 1
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(380, 415) and self.stateIndex != 2 and self.game.allowmode1:
				self.cursor_rect.midtop = (self.portalx + self.offset, self.portaly)
				self.stateIndex = 2
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(415, 445) and self.stateIndex != 3 and self.game.allowmode2:
				self.cursor_rect.midtop = (self.angryApplex + self.offset, self.angryAppley)
				self.stateIndex = 3
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(445, 475) and self.stateIndex != 4 and self.game.allowmode3:
				self.cursor_rect.midtop = (self.ultimatex + self.offset, self.ultimatey)
				self.stateIndex = 4
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(475, 505) and self.stateIndex != 5 and self.game.allowmode4:
				self.cursor_rect.midtop = (self.deSnakex + self.offset, self.deSnakey)
				self.stateIndex = 5
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(505, 535) and self.stateIndex != 6 and self.game.allowsecretmode:
				self.cursor_rect.midtop = (self.debugx + self.offset, self.debugy)
				self.stateIndex = 6
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()


		if self.game.UP_KEY:
			if self.stateIndex - 1 >= 0:
				self.cursor_rect.midtop = (self.cursor_rect.midtop[0], self.cursor_rect.midtop[1] - self.game.font_size)
				self.stateIndex -= 1
				self.state = self.allState[self.stateIndex]
			else:
				self.cursor_rect.midtop = (self.cursor_rect.midtop[0], self.cursor_rect.midtop[1] + self.game.font_size * (len(self.allState) - 1))
				self.stateIndex += (len(self.allState) - 1)
				self.state = self.allState[self.stateIndex]
			if (self.stateIndex == 6 and not self.game.allowsecretmode):
				self.stateIndex = 5
				if (self.stateIndex == 5 and not self.game.allowmode4):
					self.stateIndex = 4
				if (self.stateIndex == 4 and not self.game.allowmode3):
					self.stateIndex = 3
				if (self.stateIndex == 3 and not self.game.allowmode2):
					self.stateIndex = 2
				if (self.stateIndex == 2 and not self.game.allowmode1):
					self.stateIndex = 1
				if (self.stateIndex == 1 and not self.game.allowmode0):
					self.stateIndex = 0
				self.state = self.allState[self.stateIndex]
				if self.stateIndex == 0:
					self.cursor_rect.midtop = (self.cursor_rect.midtop[0], self.classicy)
				else:
					self.cursor_rect.midtop = (self.cursor_rect.midtop[0], self.cursor_rect.midtop[1] - self.game.font_size * (len(self.allState) - (self.stateIndex + 1)))
			self.game.DRsnd_menumove.play()

	def debug_mode(self):
		self.game.menumus.stop()
		self.debug_run_display = True

		if self.game.never_entered_unknown:
			while self.game.never_entered_unknown:
				self.game.check_events()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						logger.log('Sneky session closed.\n')
						pygame.quit()
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							self.game.never_entered_unknown = False
							self.game.save_settings()
				self.game.display.fill(self.game.BLACK)
				self.game.draw_text('Congratulations.', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2, font_name = self.game.pygame_font)
				self.game.draw_text('You finally did it. You have finally unlocked', self.game.font_size, self.mid_w, self.mid_h + self.game.font_size, font_name = self.game.pygame_font)
				self.game.draw_text('the true debug mode of Sneky.', self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 2, font_name = self.game.pygame_font)
				self.game.draw_text('Please press ENTER to step forward.', self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 4, font_name = self.game.pygame_font)
				self.blit_screen()

		self.portal_border = 0
		self.curled_up = 0
		self.apple_bag = 0
		self.break_border = 0
		self.snake_instinct = 0
		self.angry_apple = 0

		while self.debug_run_display:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					logger.log('Sneky session closed.\n')
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1 or event.key == pygame.K_KP1:
						self.portal_border += 1
						if self.portal_border == 2: self.portal_border = 0
					elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
						self.curled_up += 1
						if self.curled_up == 2: self.curled_up = 0
					elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
						self.apple_bag += 1
						if self.apple_bag == 2: self.apple_bag = 0
					elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
						self.break_border += 1
						if self.break_border == 2: self.break_border = 0
					elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
						self.snake_instinct += 1
						if self.snake_instinct == 2: self.snake_instinct = 0
					elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
						self.angry_apple += 1
						if self.angry_apple == 2: self.angry_apple = 0
					elif event.key == pygame.K_RETURN:
						self.game.mode(self.portal_border, self.curled_up, self.apple_bag, self.break_border, self.snake_instinct, self.angry_apple)
						self.start_game_debug = True
						self.debug_run_display = False
					elif event.key == pygame.K_ESCAPE:
						self.game.WIIstart.play()
						self.game.menumus.play(-1)
						self.debug_run_display = False

			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('SNEKY DEBUG MODE', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2, font_name = self.game.pygame_font)
			self.game.draw_text('NOTE: High scores are NOT saved in this mode.', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 0.5, font_name = self.game.pygame_font)
			self.game.draw_text('portal_border: ' + str(self.portal_border), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size, font_name = self.game.pygame_font)
			self.game.draw_text('curled_up: ' + str(self.curled_up), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 2, font_name = self.game.pygame_font)
			self.game.draw_text('apple_bag: ' + str(self.apple_bag), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 3, font_name = self.game.pygame_font)
			self.game.draw_text('break_border: ' + str(self.break_border), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 4, font_name = self.game.pygame_font)
			self.game.draw_text('snake_instinct: ' + str(self.snake_instinct), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 5, font_name = self.game.pygame_font)
			self.game.draw_text('angry_apple: ' + str(self.angry_apple), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 6, font_name = self.game.pygame_font)
			self.game.draw_text('Use number keys 1-6 to toggle between 0 & 1', self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 8, font_name = self.game.pygame_font)
			self.game.draw_text('ENTER: Start - ESC: Return', self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 9, font_name = self.game.pygame_font)
			self.blit_screen()