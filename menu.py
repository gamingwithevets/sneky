import sys
if __name__ == '__main__':
	print('Please run main.py to start Sneky.')
	sys.exit()

import pygame
import os
import math
import time
import logger, updater
import shutil
import random
from datetime import datetime
import webbrowser

class Menu(object):
	def __init__(self, game):
		self.game = game
		self.back_button_highlighted = False
		self.enter_button_highlighted = False
		self.enter_button_disabled = False
		self.nav_button_condition_reload()

	def init_values(self, game):
		self.game = game
		self.mid_w, self.mid_h = int(self.game.DISPLAY_W / 2), int(self.game.DISPLAY_H / 2)
		self.run_display = True
		self.cursor_rect = pygame.Rect(0,0, self.game.font_size, self.game.font_size)
		self.offset = -200

	def draw_cursor(self, size = 30):
		if self.game.holidayname == 'christmas': temp_cursor = pygame.transform.scale(self.game.imgApple_menu, (int(11 * (size / 21)), size))
		else: temp_cursor = pygame.transform.scale(self.game.imgApple_menu, (int(40 * (size / 46)), size))
		temp_cursor_rect = pygame.Rect(self.cursor_rect)
		temp_cursor_rect.midtop = (temp_cursor_rect.midtop[0], temp_cursor_rect.midtop[1] - int(size / 2 - 2)) 
		self.game.display.blit(temp_cursor, temp_cursor_rect)

	def blit_screen(self, fps_font = 'default', showfps = True):
		if showfps: self.game.update_fps(fps_font)
		self.game.window.blit(self.game.display, (0,0))
		pygame.display.update()
		self.game.reset_keys()


	def back_button(self):
		if not self.back_button_highlighted: self.game.display.blit(self.game.imgBack, self.game.imgBack_rect)
		else: self.game.display.blit(self.game.imgBack_highlight, self.game.imgBack_rect)

		self.nav_button_condition_reload()
		if self.back_button_condition and not self.game.menu.back_button_highlighted:
			self.game.DRsnd_menumove.play()
			self.back_button_highlighted = True
		elif not self.game.menu.back_button_condition and self.game.menu.back_button_highlighted: self.game.menu.back_button_highlighted = False

	def enter_button(self):
		if self.enter_button_disabled: self.game.display.blit(self.game.imgEnter_disabled, self.game.imgEnter_rect)
		else:
			if self.enter_button_highlighted: self.game.display.blit(self.game.imgEnter_highlight, self.game.imgEnter_rect)
			else: self.game.display.blit(self.game.imgEnter, self.game.imgEnter_rect)

		self.nav_button_condition_reload()
		if self.enter_button_condition and not self.enter_button_highlighted:
			if not self.enter_button_disabled: self.game.DRsnd_menumove.play()
			self.enter_button_highlighted = True
		elif not self.enter_button_condition and self.enter_button_highlighted: self.enter_button_highlighted = False

	def nav_button_condition_reload(self):
		self.back_button_condition = self.game.mousex in range(16, 88) and self.game.mousey in range(self.game.DISPLAY_H - 86, self.game.DISPLAY_H - 31)
		self.enter_button_condition = self.game.mousex in range(self.game.DISPLAY_W - 82, self.game.DISPLAY_W - 14) and self.game.mousey in range(self.game.DISPLAY_H - 86, self.game.DISPLAY_H - 31)

	def back_button_click(self):
		self.nav_button_condition_reload()
		if self.game.CLICK and self.back_button_condition and self.back_button_highlighted: return True
		
	def enter_button_click(self):
		self.nav_button_condition_reload()
		if self.game.CLICK and self.enter_button_condition and self.enter_button_highlighted:
			if self.enter_button_disabled: self.game.DRsnd_cantselect.play()
			else: return True

class MainMenu(Menu):
	def __init__(self, game):
		Menu.init_values(self, game)
		self.state = 'LAUNCH GAME'
		self.startx, self.starty = self.mid_w, self.mid_h + int(self.game.font_size * 3/2)
		self.optionsx, self.optionsy = self.mid_w, self.mid_h + int(self.game.font_size * 5/2)
		self.creditsx, self.creditsy = self.mid_w, self.mid_h + int(self.game.font_size * 7/2)
		self.quitx, self.quity = self.mid_w, self.mid_h + int(self.game.font_size * 9/2)
		self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

		self.menumousex = (self.mid_w - 180, self.mid_w + 175)
		self.startmousey = (self.mid_h - 3, self.mid_h + 65)
		self.optionsmousey = (self.mid_h + 65, self.mid_h + 100)
		self.creditsmousey = (self.mid_h + 100, self.mid_h + 130)
		self.quitmousey = (self.mid_h + 130, self.mid_h + 160)

	def display_menu(self):
		if self.game.auto_update: self.game.updater.display_menu(True)

		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('MAIN MENU', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
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
		elif self.game.BACK_KEY or self.game.menu.back_button_click():
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
		Menu.init_values(self,game)
		self.state = 'GENERAL'
		self.generalx, self.generaly = self.mid_w, self.mid_h + self.game.font_size
		self.videox, self.videoy = self.mid_w, self.mid_h + self.game.font_size *2
		self.volx, self.voly = self.mid_w, self.mid_h + self.game.font_size *3
		self.controlsx, self.controlsy = self.mid_w, self.mid_h + self.game.font_size *4
		self.updatex, self.updatey = self.mid_w, self.mid_h + self.game.font_size *5
		self.clearx, self.cleary = self.mid_w, self.mid_h + self.game.font_size *6
		self.cursor_rect.midtop = (self.generalx + self.offset, self.generaly)

		self.menumousex = (self.mid_w - 100, self.mid_w + 95)
		self.generalmousey = (self.mid_h + 20, self.mid_h + 50)
		self.videomousey = (self.mid_h + 50, self.mid_h + 80)
		self.volmousey = (self.mid_h + 80, self.mid_h + 110)
		self.controlsmousey = (self.mid_h + 110, self.mid_h + 140)
		self.updatemousey = (self.mid_h + 140, self.mid_h + 170)
		self.clearmousey = (self.mid_h + 170, self.mid_h + 200)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('GENERAL', int(self.game.font_size * 3/4), self.generalx, self.generaly)
			self.game.draw_text('VIDEO', int(self.game.font_size * 3/4), self.videox, self.videoy)
			self.game.draw_text('VOLUME', int(self.game.font_size * 3/4), self.volx, self.voly)
			self.game.draw_text('CONTROLS', int(self.game.font_size * 3/4), self.controlsx, self.controlsy)
			self.game.draw_text('UPDATES', int(self.game.font_size * 3/4), self.updatex, self.updatey)
			self.game.draw_text('CLEAR DATA', int(self.game.font_size * 3/4), self.clearx, self.cleary)
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'GENERAL':
				self.state = 'VIDEO'
				self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)
			elif self.state == 'VIDEO':
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
				self.state = 'GENERAL'
				self.cursor_rect.midtop = (self.generalx + self.offset, self.generaly)
			self.game.DRsnd_menumove.play()
		if self.game.UP_KEY:
			if self.state == 'GENERAL':
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
			elif self.state == 'VIDEO':
				self.state = 'GENERAL'
				self.cursor_rect.midtop = (self.generalx + self.offset, self.generaly)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.generalmousey) and self.state != 'GENERAL':
				self.cursor_rect.midtop = (self.generalx + self.offset, self.generaly)
				self.state = 'GENERAL'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.videomousey) and self.state != 'VIDEO':
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
		if self.game.BACK_KEY or self.game.menu.back_button_click():
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'GENERAL': self.game.curr_menu = self.game.general_menu
			elif self.state == 'CONTROLS': self.game.curr_menu = self.game.controls
			elif self.state == 'VIDEO': self.game.curr_menu = self.game.videomenu
			elif self.state == 'VOLUME': self.game.curr_menu = self.game.volumemenu
			elif self.state == 'UPDATES': self.game.curr_menu = self.game.updatemenu
			elif self.state == 'CLEAR': self.game.curr_menu = self.game.clear_data
			self.run_display = False
		elif self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.generalmousey):
				self.game.curr_menu = self.game.general_menu
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.videomousey):
				self.game.curr_menu = self.game.videomenu
				self.game.DRsnd_select.play()
			elif self.game.mousey in range(*self.volmousey):
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
		Menu.init_values(self,game)
		self.state = 'saved'
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 10
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 40
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)

		self.menumousex = (self.mid_w - 165, self.mid_w + 160)
		self.opt1mousey = (self.mid_h, self.mid_h + 20)
		self.opt2mousey = (self.mid_h + 30, self.mid_h + 50)
		self.opt3mousey = (self.mid_h + 60, self.mid_h + 80)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('CLEAR DATA', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			self.game.draw_text('CLEAR HIGH SCORES', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text('CLEAR SESSION LOGS', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text('CLEAR DATA AND LOGS', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
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
		if self.game.BACK_KEY or self.game.menu.back_button_click():
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
		clear2_run_display = True
		while clear2_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY or self.game.menu.back_button_click():
				clear2_run_display = False
				self.game.DRsnd_select.play()
				self.run_display = True
			elif self.game.START_KEY or self.game.menu.enter_button_click():
				clear2_run_display = False
				self.game.DRsnd_select.play()
				self.clear_data3(cleardata, clearlogs)
				break
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.menu.enter_button()
			self.game.draw_text('CLEAR DATA', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			if cleardata:
				self.game.draw_text('WARNING! You are about to clear all saved high scores.', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, color = self.game.red, font_name = self.game.menu2_font)
				if clearlogs:
					self.game.draw_text('You\'re also clearing all your session logs.', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text('This cannot be undone!', int(self.game.font_size / 2), self.mid_w, self.mid_h + 50, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR EVERYTHING', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
					self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: CANCEL', int(self.game.font_size / 2), self.mid_w, self.mid_h + 110, font_name = self.game.menu2_font)
				else:
					self.game.draw_text('This cannot be undone!', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, color = self.game.red, font_name = self.game.menu2_font)
					self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR ALL SAVED DATA', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font)
					self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: CANCEL', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
			elif clearlogs:
				self.game.draw_text('WARNING! You are about to clear all your session logs.', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, color = self.game.red, font_name = self.game.menu2_font)
				self.game.draw_text('This cannot be undone!', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, color = self.game.red, font_name = self.game.menu2_font)
				self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR ALL SESSION LOGS', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font)
				self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: CANCEL', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
			self.blit_screen()

	def clear_data3(self, cleardata = True, clearlogs = False):
		clear3_run_display = True
		self.game.menu.enter_button_disabled = True
		enter_button_disabled = True
		timer = 5
		while clear3_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY or self.game.menu.back_button_click():
				clear3_run_display = False
				self.game.DRsnd_select.play()
				self.run_display = True
				self.game.menu.enter_button_disabled = False
			elif (self.game.START_KEY or self.game.menu.enter_button_click()):
				if enter_button_disabled: self.game.DRsnd_cantselect.play()
				else:
					clear3_run_display = False
					self.game.DRsnd_select.play()
					self.clear_data(cleardata, clearlogs)
					break
			if timer <= 0:
				enter_button_disabled = False
				self.game.menu.enter_button_disabled = False
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.menu.enter_button()
			if enter_button_disabled: self.game.draw_text(f'{int(timer / 100) + (timer % 100 > 0)}', self.game.font_size, *self.game.imgEnter_rect.center, font_name = self.game.menu2_font, color = self.game.red_god)
			self.game.draw_text('CLEAR DATA', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			if cleardata:
				if clearlogs:
					self.game.draw_text('Are you REALLY sure you wanna clear your high scores and session logs?', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, color = self.game.red, font_name = self.game.menu2_font)
					if enter_button_disabled: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR HIGH SCORES AND LOGS ({int(timer / 100) + (timer % 100 > 0)})', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font, color = self.game.gray)
					else: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR DATA AND LOGS', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font)
				else:
					self.game.draw_text('Are you REALLY sure you wanna clear your high scores?', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, color = self.game.red, font_name = self.game.menu2_font)
					if enter_button_disabled: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR SAVED HIGH SCORES ({int(timer / 100) + (timer % 100 > 0)})', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font, color = self.game.gray)
					else: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR ALL SAVED DATA', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font)
			elif clearlogs:
				self.game.draw_text('Are you REALLY sure you wanna clear all session logs?', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, color = self.game.red, font_name = self.game.menu2_font)
				if enter_button_disabled: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR ALL SESSION LOGS ({int(timer / 100) + (timer % 100 > 0)})', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font, color = self.game.gray)
				else: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: CLEAR ALL SESSION LOGS', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: CANCEL', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
			self.game.draw_text('THIS IS YOUR LAST WARNING!', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, color = self.game.red, font_name = self.game.menu2_font)
			self.blit_screen()
			timer -= self.deltatime

	def clear_data(self, cleardata = True, clearlogs = False):
		if cleardata:
			self.allowmode0 = False
			self.allowmode1 = False
			self.allowmode2 = False
			self.allowmode3 = False
			self.allowmode4 = False
			self.allowsecretmode = False
			self.never_entered_unknown = True
			self.high_scores = {
			'Classic': 0,
			'Apple Bag': 0,
			'Portal Border': 0,
			'Angry Apple': 0,
			'Ultimate Snake': 0
			}
			self.game.angry_apple_halloween_hs = 3599000
			self.game.save_settings()
		if os.path.exists(self.game.appdata_path) and os.path.exists(self.game.appdata_path + logger.logfile) and clearlogs: os.remove(self.game.appdata_path + logger.logfile)
		if self.clearlogs:
			logger.log('The following has been cleared:', allowlog = False)
			if cleardata: print('- Saved high scores')
			print('- Session logs')
			print('Sneky session closed.')
			pygame.quit()
			sys.exit()
		else:
			logger.log('The following has been cleared:\n- Saved high scores')

			clear4_run_display = True
			while clear4_run_display:
				self.game.reset_keys()
				self.game.check_events()
				if self.game.BACK_KEY or back_button_click():
					clear4_run_display = False
					self.game.DRsnd_select.play()
					self.run_display = True
				self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
				self.game.menu.back_button()
				self.game.draw_text('CLEAR DATA', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
				self.game.draw_text('All game data has been cleared.', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, color = self.game.red, font_name = self.game.menu2_font)
				self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: BACK', int(self.game.font_size / 2), self.mid_w, self.mid_h + 50, font_name = self.game.menu2_font)
				self.blit_screen()

class CreditsMenu(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			if self.game.BACK_KEY or self.game.menu.back_button_click():
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
				self.game.DRsnd_select.play()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('CREDITS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			self.game.draw_text('Original version by SeverusFate and GamingWithEvets', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, font_name = self.game.menu2_font)
			self.game.draw_text('(c) 2021-2022 GamingWithEvets Inc. All rights reserved.', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, font_name = self.game.menu2_font)
			self.game.draw_text('See full credits in the README, either on GitHub or', int(self.game.font_size / 2), self.mid_w, self.mid_h + 70, font_name = self.game.menu2_font)
			self.game.draw_text('included with the source code', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
			self.blit_screen()

class VideoMenu(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)
		self.state = 'fullscreen'
		self.set_values()
		self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)

	def set_values(self):
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 10
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 40
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.opt4x, self.opt4y = self.mid_w, self.mid_h + 100
		self.opt5x, self.opt5y = self.mid_w, self.mid_h + 130

		self.menumousex = (self.mid_w - 165, self.mid_w + 160)
		self.opt1mousey = (self.mid_h, self.mid_h + 20)
		self.opt2mousey = (self.mid_h + 30, self.mid_h + 50)
		self.opt3mousey = (self.mid_h + 60, self.mid_h + 80)
		self.opt4mousey = (self.mid_h + 90,self.mid_h + 110)
		self.opt5mousey = (self.mid_h + 120, self.mid_h + 140)

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
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('VIDEO SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text(f'Fullscreen: {self.fullscreen_str}', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			if not self.fullscreen: self.game.draw_text(f'Scaled Mode: {self.scaled_str}', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font, color = self.game.gray)
			else: self.game.draw_text(f'Scaled Mode: {self.scaled_str}', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			if self.game.enable_native:
				if self.scaled and self.fullscreen: self.game.draw_text(f'Native Resolution ({self.game.current_w}x{self.game.current_h}): {self.native_res_str}', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font, color = self.game.gray)
				else: self.game.draw_text(f'Native Resolution ({self.game.current_w}x{self.game.current_h}): {self.native_res_str}', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
				self.game.draw_text('APPLY SETTINGS', int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
				self.game.draw_text('RESET TO DEFAULTS', int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
			else:
				self.game.draw_text('APPLY SETTINGS', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
				self.game.draw_text('RESET TO DEFAULTS', int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
			self.game.draw_text(f'Current window setting: {self.curr_setting}', int(self.game.font_size / 2), self.opt4x, self.opt4y + 70, font_name = self.game.menu2_font)
			self.game.save_settings()
			self.draw_cursor(int(self.game.font_size / 2))
			self.blit_screen()


	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'fullscreen':
				if not self.fullscreen:
					if self.game.enable_native: self.state = 'native'
					else: self.state = 'apply'
					self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				else:
					self.state = 'scaled'
					self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'scaled':
				if self.scaled and self.fullscreen:
					self.state = 'apply'
					self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				else:
					if self.game.enable_native: self.state = 'native'
					else: self.state = 'apply'
					self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'native':
				self.state = 'apply'
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'apply':
				self.state = 'reset'
				if self.game.enable_native: self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				else: self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'reset':
				self.state = 'fullscreen'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'fullscreen':
				self.state = 'reset'
				if self.game.enable_native: self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				else: self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'reset':
				self.state = 'apply'
				if self.game.enable_native: self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				else: self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'apply':
				if self.scaled and self.fullscreen:
					self.state = 'scaled'
					self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				else:
					if self.game.enable_native:
						self.state = 'native'
						self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
					else:
						if not self.fullscreen:
							self.state = 'fullscreen'
							self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
						else:
							self.state = 'scaled'
							self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
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
			if self.game.enable_native:
				if self.game.mousey in range(*self.opt3mousey) and self.state != 'native' and (not self.scaled or not self.fullscreen):
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
			else:
				if self.game.mousey in range(*self.opt3mousey) and self.state != 'apply':
					self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
					self.state = 'apply'
					self.game.DRsnd_menumove.play()
				elif self.game.mousey in range(*self.opt4mousey) and self.state != 'reset':
					self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
					self.state = 'reset'
					self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY or self.game.menu.back_button_click():
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
				if self.fullscreen and not self.scaled and not self.native_res: should_continue = self.noscale_warning()
				elif not self.fullscreen and self.game.fullscreen: should_continue = self.small_text_warning()
				elif self.native_res and not self.game.native_res and ((self.fullscreen and not self.scaled) or not self.fullscreen): should_continue = self.native_warning()
				if should_continue:
					self.game.fullscreen = self.fullscreen
					self.game.scaled = self.scaled
					self.game.native_res = self.native_res
					self.game.window = self.game.set_window_mode()
					self.game.init_menus()
					self.game.mode()
					Menu.init_values(self, self.game)
					self.set_values()
					self.set_cursor_pos()
					self.game.change_volume()
			elif self.state == 'reset':
				if self.game.fullscreen == True and self.game.scaled == True and self.game.native_res == False: should_continue = False
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
					Menu.init_values(self, self.game)
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
			elif self.game.enable_native and self.game.mousey in range(*self.opt3mousey) and (not self.scaled or not self.fullscreen):
				self.game.DRsnd_select.play()
				self.native_res = not self.native_res
			elif (self.game.enable_native and self.game.mousey in range(*self.opt4mousey)) or (not self.game.enable_native and self.game.mousey in range(*self.opt3mousey)):
				self.game.DRsnd_select.play()
				if self.fullscreen == self.game.fullscreen and self.scaled == self.game.scaled and self.native_res == self.game.native_res:
					should_continue = False
				else: should_continue = True
				if self.fullscreen and not self.scaled and not self.native_res: should_continue = self.noscale_warning()
				elif not self.fullscreen and self.game.fullscreen: should_continue = self.small_text_warning()
				elif self.native_res and not self.game.native_res and ((self.fullscreen and not self.scaled) or not self.fullscreen): should_continue = self.native_warning()
				if should_continue:
					self.game.fullscreen = self.fullscreen
					self.game.scaled = self.scaled
					self.game.native_res = self.native_res
					self.game.window = self.game.set_window_mode()
					self.game.init_menus()
					self.game.mode()
					Menu.init_values(self, self.game)
					self.set_values()
					self.set_cursor_pos()
					self.game.change_volume()
			elif (self.game.enable_native and self.game.mousey in range(*self.opt5mousey)) or (not self.game.enable_native and self.game.mousey in range(*self.opt4mousey)):
				self.game.DRsnd_select.play()
				if self.game.fullscreen == True and self.game.scaled == True and self.game.native_res == True: should_continue = False
				else: should_continue = True
				if should_continue:
					self.game.DRsnd_select.play()
					self.game.fullscreen = True
					self.game.scaled = True
					self.game.native_res = True
					self.game.window = self.game.set_window_mode()
					self.game.init_menus()
					self.game.mode()
					Menu.init_values(self, self.game)
					self.set_values()
					self.set_cursor_pos()
					self.game.change_volume()

	def set_cursor_pos(self):
		if self.state == 'apply': self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
		elif self.state == 'reset': self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)

	def noscale_warning(self):
		noscale_run_display = True
		self.game.menu.enter_button_disabled = True
		enter_button_disabled = True
		timer = 5
		while noscale_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY or self.game.menu.back_button_click():
				noscale_run_display = False
				self.game.menu.enter_button_disabled = False
				enter_button_disabled = False
				self.game.DRsnd_select.play()
				return False
			elif self.game.START_KEY or self.game.menu.enter_button_click():
				if enter_button_disabled: self.game.DRsnd_cantselect.play()
				else:
					noscale_run_display = False
					self.game.DRsnd_select.play()
					return True
			if timer <= 0:
				self.game.menu.enter_button_disabled = False
				enter_button_disabled = False
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.menu.enter_button()
			if enter_button_disabled: self.game.draw_text(f'{int(timer / 100) + (timer % 100 > 0)}', self.game.font_size, *self.game.imgEnter_rect.center, font_name = self.game.menu2_font, color = self.game.red_god)
			self.game.draw_text('VIDEO SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('WARNING! Fullscreen without scaled mode or native', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, font_name = self.game.menu2_font)
			self.game.draw_text('resolution may cause screen issues!', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, font_name = self.game.menu2_font)
			self.game.draw_text('Are you sure you want to continue?', int(self.game.font_size / 2), self.mid_w, self.mid_h + 50, font_name = self.game.menu2_font)
			if enter_button_disabled: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: YES ({int(timer / 100) + (timer % 100 > 0)})', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font, color = self.game.gray)
			else: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: YES', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: NO', int(self.game.font_size / 2), self.mid_w, self.mid_h + 110, font_name = self.game.menu2_font)
			self.blit_screen()
			timer -= self.deltatime

	def native_warning(self):
		native_run_display = True
		while native_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY or self.game.menu.back_button_click():
				native_run_display = False
				self.game.DRsnd_select.play()
				return False
			elif self.game.START_KEY or self.game.menu.enter_button_click():
				native_run_display = False
				self.game.DRsnd_select.play()
				return self.small_text_warning()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.menu.enter_button()
			self.game.draw_text('VIDEO SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('Hahaha! I see that you\'ve dug into the game code to', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, font_name = self.game.menu2_font)
			self.game.draw_text('re-enable the native resolution option. Note that this', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, font_name = self.game.menu2_font)
			self.game.draw_text('mode is experimental, so use it at your own risk!', int(self.game.font_size / 2), self.mid_w, self.mid_h + 50, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: ENABLE NATIVE RESOLUTION', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: GO BACK', int(self.game.font_size / 2), self.mid_w, self.mid_h + 110, font_name = self.game.menu2_font)
			self.blit_screen()

	def small_text_warning(self):
		small_text_run_display = True
		self.game.menu.enter_button_disabled = True
		enter_button_disabled = True
		timer = 5
		while small_text_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.BACK_KEY or self.game.menu.back_button_click():
				small_text_run_display = False
				self.game.menu.enter_button_disabled = False
				enter_button_disabled = False
				self.game.DRsnd_select.play()
				return False
			elif self.game.START_KEY or self.game.menu.enter_button_click():
				if enter_button_disabled: self.game.DRsnd_cantselect.play()
				else:
					small_text_run_display = False
					self.game.DRsnd_select.play()
					return True
			if timer <= 0:
				self.game.menu.enter_button_disabled = False
				enter_button_disabled = False
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.menu.enter_button()
			if enter_button_disabled: self.game.draw_text(f'{int(timer / 100) + (timer % 100 > 0)}', self.game.font_size, *self.game.imgEnter_rect.center, font_name = self.game.menu2_font, color = self.game.red_god)
			self.game.draw_text('VIDEO SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('NOTE: If you see that the text/screen is too small, you', int(self.game.font_size / 2), self.mid_w, self.mid_h + 10, font_name = self.game.menu2_font)
			self.game.draw_text('probably should switch to fullscreen with scaled mode.', int(self.game.font_size / 2), self.mid_w, self.mid_h + 30, font_name = self.game.menu2_font)
			self.game.draw_text('Do you want to apply this setting?', int(self.game.font_size / 2), self.mid_w, self.mid_h + 50, font_name = self.game.menu2_font)
			if enter_button_disabled: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: YES ({int(timer / 100) + (timer % 100 > 0)})', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font, color = self.game.gray)
			else: self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} / ENTER BUTTON: YES', int(self.game.font_size / 2), self.mid_w, self.mid_h + 90, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} / BACK BUTTON: NO', int(self.game.font_size / 2), self.mid_w, self.mid_h + 110, font_name = self.game.menu2_font)
			self.blit_screen()
			timer -= self.deltatime

class UpdateMenu(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)
		self.state = 'check'
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 10
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 40
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)

		self.menumousex = (self.mid_w - 165, self.mid_w + 160)
		self.opt1mousey = (self.mid_h, self.mid_h + 20)
		self.opt2mousey = (self.mid_h + 30, self.mid_h + 50)
		self.opt3mousey = (self.mid_h + 60, self.mid_h + 80)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			if self.game.auto_update: self.auto_str = 'ON'
			else: self.auto_str = 'OFF'
			if self.game.check_prerelease: self.prer_str = 'ON'
			else: self.prer_str = 'OFF'
			self.game.check_events()
			self.check_input()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('UPDATES', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('CHECK FOR UPDATES', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text(f'Automatically Check for Updates: {self.auto_str}', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text(f'Check Prerelease Versions: {self.prer_str}', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
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
		if self.game.BACK_KEY or self.game.menu.back_button_click():
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'check':
				self.game.curr_menu = self.game.updater
				self.run_display = False
			elif self.state == 'auto': self.game.auto_update = not self.game.auto_update
			elif self.state == 'prer': self.game.check_prerelease = not self.game.check_prerelease

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

class GeneralMenu(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)
		self.state = 'leg'
		self.opt1x, self.opt1y = self.mid_w, self.mid_h + 10
		self.opt2x, self.opt2y = self.mid_w, self.mid_h + 40
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 70
		self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)

		self.menumousex = (self.mid_w - 165, self.mid_w + 160)
		self.opt1mousey = (self.mid_h, self.mid_h + 20)
		self.opt2mousey = (self.mid_h + 30, self.mid_h + 50)
		self.opt3mousey = (self.mid_h + 60, self.mid_h + 80)
	def display_menu(self):
		self.run_display = True
		while self.run_display:
			if self.game.legacy_experience: self.leg_str = 'ON'
			else: self.leg_str = 'OFF'
			if self.game.dark_mode: self.dark_str = 'ON'
			else: self.dark_str = 'OFF'
			if self.game.showfps: self.fps_str = 'ON'
			else: self.fps_str = 'OFF'
			self.game.check_events()
			self.check_input()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('GENERAL', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text(f'Legacy Experience: {self.leg_str}', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text(f'Dark Mode: {self.dark_str}', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text(f'Show FPS Count: {self.fps_str}', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
			self.game.save_settings()
			self.draw_cursor(int(self.game.font_size / 2))
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'leg':
				self.state = 'dark'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'dark':
				self.state = 'fps'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'fps':
				self.state = 'leg'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'leg':
				self.state = 'fps'
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
			elif self.state == 'fps':
				self.state = 'dark'
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
			elif self.state == 'dark':
				self.state = 'leg'
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
			self.game.DRsnd_menumove.play()

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey) and self.state != 'leg':
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
				self.state = 'leg'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt2mousey) and self.state != 'dark':
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				self.state = 'dark'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt3mousey) and self.state != 'fps':
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'fps'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY or self.game.menu.back_button_click():
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'leg': self.game.legacy_experience = not self.game.legacy_experience
			elif self.state == 'dark': self.game.dark_mode = not self.game.dark_mode
			elif self.state == 'fps': self.game.showfps = not self.game.showfps

		if self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey):
				self.game.DRsnd_select.play()
				self.game.legacy_experience = not self.game.legacy_experience
			elif self.game.mousey in range(*self.opt2mousey):
				self.game.DRsnd_select.play()
				self.game.dark_mode = not self.game.dark_mode
			elif self.game.mousey in range(*self.opt3mousey):
				self.game.DRsnd_select.play()
				self.game.showfps = not self.game.showfps

class Updater(Menu):
	def __init__(self, game):
		Menu.init_values(self, game)
		self.state = 'install'
		self.opt0x, self.opt0y = self.mid_w, self.mid_h +  10
		self.opt1x, self.opt1y = self.mid_w, self.mid_h +  40 
		self.opt2x, self.opt2y = self.mid_w, self.mid_h +  70
		self.opt3x, self.opt3y = self.mid_w, self.mid_h + 100
		self.opt4x, self.opt4y = self.mid_w, self.mid_h + 130
		self.opt5x, self.opt5y = self.mid_w, self.mid_h + 160
		self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)

		self.menumousex = (self.mid_w - 165, self.mid_w + 160)
		self.opt2mousey = (self.mid_h + 80, self.mid_h + 100)
		self.opt3mousey = (self.mid_h + 100, self.mid_h + 120)
		self.opt4mousey = (self.mid_h + 120, self.mid_h + 140)
		self.opt5mousey = (self.mid_h + 140, self.mid_h + 160)
		
	def display_menu(self, auto = False):
		self.run_display = True
		self.auto = auto
		if self.run_display:
			if self.auto and self.game.updatechecked:
				self.run_display = False
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.draw_text('UPDATES', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2) 
			self.game.draw_text('Checking for updates. Please wait...', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
			if self.auto: self.game.draw_text('To disable automatic updates, please go to Settings -> Updates.', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.blit_screen()
			self.updstat = updater.check_updates(self.game.gameversion, self.game.check_prerelease)
			if self.updstat['newupdate']: self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)	
			while self.run_display:
				self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
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
					self.game.draw_text(f'{self.updstat["tag_name"]} - {self.updstat["title"]}', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
					self.game.draw_text('VISIT DOWNLOAD PAGE', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
					self.game.draw_text('REMIND ME LATER', int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
				elif self.updstat['unofficial']:
					self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
					if (self.game.START_KEY or self.game.BACK_KEY) or (self.game.CLICK and self.game.mousex in range(*self.menumousex) and self.game.mousey in range(*self.opt5mousey)):
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
						if (self.game.START_KEY or self.game.BACK_KEY) or (self.game.CLICK and self.game.mousex in range(*self.menumousex) and self.game.mousey in range(*self.opt2mousey)):
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

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt3mousey) and self.state != 'install':
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'install'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt4mousey) and self.state != 'remind':
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				self.state = 'remind'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			if not self.auto: self.game.curr_menu = self.game.updatemenu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			if self.state == 'install': self.download()
			elif self.state == 'remind':
				self.game.updatechecked = True
				if not self.auto: self.game.curr_menu = self.game.updatemenu
				self.run_display = False

		if self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.updstat['newupdate']:
				if self.game.mousey in range(*self.opt3mousey):
					self.game.DRsnd_select.play()
					self.download()
				elif self.game.mousey in range(*self.opt4mousey):
					self.game.DRsnd_select.play()
					self.game.updatechecked = True
					if not self.auto: self.game.curr_menu = self.game.updatemenu
					self.run_display = False

	def download(self): webbrowser.open_new_tab('https://github.com/gamingwithevets/sneky/releases/tag/v' + self.updstat['tag_name'])

class VolumeMenu(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)
		self.state = 'master'
		self.mastervolx, self.mastervoly = self.mid_w, self.mid_h + 10
		self.musicvolx, self.musicvoly = self.mid_w, self.mid_h + 40
		self.soundvolx, self.soundvoly = self.mid_w, self.mid_h + 70
		self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)

		self.volup1_button_highlighted = False
		self.volup5_button_highlighted = False
		self.voldown1_button_highlighted = False
		self.voldown5_button_highlighted = False
		self.volup1_button_disabled = False
		self.volup5_button_disabled = False
		self.voldown1_button_disabled = False
		self.voldown5_button_disabled = False

		self.menumousex = (self.mid_w - 165, self.mid_w + 160)
		self.opt1mousey = (self.mid_h - 5, self.mid_h + 25)
		self.opt2mousey = (self.mid_h + 25, self.mid_h + 55)
		self.opt3mousey = (self.mid_h + 55, self.mid_h + 85)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('VOLUME SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			self.game.draw_text(f'MASTER VOLUME: {round(self.game.volume * 100)}%', int(self.game.font_size * 3/4), self.mastervolx, self.mastervoly, font_name = self.game.menu2_font)
			self.game.draw_text(f'MUSIC: {round(self.game.musicvol * 100)}%', int(self.game.font_size * 3/4), self.musicvolx, self.musicvoly, font_name = self.game.menu2_font)
			self.game.draw_text(f'SOUND: {round(self.game.soundvol * 100)}%', int(self.game.font_size * 3/4), self.soundvolx, self.soundvoly, font_name = self.game.menu2_font)
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

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey) and self.state != 'master':
				self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)
				self.state = 'master'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt2mousey) and self.state != 'music':
				self.cursor_rect.midtop = (self.musicvolx + self.offset, self.musicvoly)
				self.state = 'music'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt3mousey) and self.state != 'sound':
				self.cursor_rect.midtop = (self.soundvolx + self.offset, self.soundvoly)
				self.state = 'sound'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY or self.game.menu.back_button_click():
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

		if self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt1mousey):
				self.game.DRsnd_select.play()
				self.mastervol()
			elif self.game.mousey in range(*self.opt2mousey):
				self.game.DRsnd_select.play()
				self.musicvol()
			elif self.game.mousey in range(*self.opt3mousey):
				self.game.DRsnd_select.play()
				self.soundvol()

	def mastervol(self):
		self.mv_run_display = True
		while self.mv_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY or self.game.menu.back_button_click():
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
			elif self.voldown1_button_click():
				self.game.volume -= 0.01
				if self.voldown1_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.volup1_button_click():
				self.game.volume += 0.01
				if self.volup1_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.voldown5_button_click():
				self.game.volume -= 0.05
				if self.voldown5_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.volup5_button_click():
				self.game.volume += 0.05
				if self.volup5_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			if self.game.volume > 1:
				self.game.volume = 1
			elif self.game.volume < 0:
				self.game.volume = 0
			if self.game.volume == 1:
				self.volup1_button_disabled = True
				self.volup5_button_disabled = True
			else:
				self.volup1_button_disabled = False
				self.volup5_button_disabled = False
			if self.game.volume == 0:
				self.voldown1_button_disabled = True
				self.voldown5_button_disabled = True
			else:
				self.voldown1_button_disabled = False
				self.voldown5_button_disabled = False
			self.game.change_volume()
			self.game.save_settings()

			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.vol_buttons()
			self.game.draw_text('VOLUME SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			self.game.draw_text(f'MASTER VOLUME: {round(self.game.volume * 100)}%', int(self.game.font_size * 3/4), self.mid_w, self.mid_h + 10, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.UP_BIND).upper()}: -1% - {pygame.key.name(self.game.DOWN_BIND).upper()}: +1% - {pygame.key.name(self.game.LEFT_BIND).upper()}: -5% - {pygame.key.name(self.game.RIGHT_BIND).upper()}: +5%', 15, self.mid_w, self.mastervoly + 25, font_name = self.game.menu2_font)
			self.game.draw_text('Or, use your mouse slider or the buttons below', 15, self.mid_w, self.mastervoly + 50, font_name = self.game.menu2_font)
			self.blit_screen()

	def musicvol(self):
		self.ms_run_display = True
		while self.ms_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY or self.game.menu.back_button_click():
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
			elif self.voldown1_button_click():
				self.game.musicvol -= 0.01
				if self.voldown1_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.volup1_button_click():
				self.game.musicvol += 0.01
				if self.volup1_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.voldown5_button_click():
				self.game.musicvol -= 0.05
				if self.voldown5_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.volup5_button_click():
				self.game.musicvol += 0.05
				if self.volup5_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			if self.game.musicvol > 1:
				self.game.musicvol = 1
			elif self.game.musicvol < 0:
				self.game.musicvol = 0
			if self.game.musicvol == 1:
				self.volup1_button_disabled = True
				self.volup5_button_disabled = True
			else:
				self.volup1_button_disabled = False
				self.volup5_button_disabled = False
			if self.game.musicvol == 0:
				self.voldown1_button_disabled = True
				self.voldown5_button_disabled = True
			else:
				self.voldown1_button_disabled = False
				self.voldown5_button_disabled = False
			self.game.change_volume()
			self.game.save_settings()

			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.vol_buttons()
			self.game.draw_text('VOLUME SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			self.game.draw_text(f'MUSIC: {round(self.game.musicvol * 100)}%', int(self.game.font_size * 3/4), self.musicvolx, self.musicvoly, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.UP_BIND).upper()}: -1% - {pygame.key.name(self.game.DOWN_BIND).upper()}: +1% - {pygame.key.name(self.game.LEFT_BIND).upper()}: -5% - {pygame.key.name(self.game.RIGHT_BIND).upper()}: +5%', 15, self.mid_w, self.musicvoly + 25, font_name = self.game.menu2_font)
			self.game.draw_text('Or, use your mouse slider or the buttons below', 15, self.mid_w, self.musicvoly + 50, font_name = self.game.menu2_font)
			self.blit_screen()

	def soundvol(self):
		self.sound_run_display = True
		while self.sound_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY or self.game.menu.back_button_click():
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
			elif self.voldown1_button_click():
				self.game.soundvol -= 0.01
				if self.voldown1_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.volup1_button_click():
				self.game.soundvol += 0.01
				if self.volup1_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.voldown5_button_click():
				self.game.soundvol -= 0.05
				if self.voldown5_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			elif self.volup5_button_click():
				self.game.soundvol += 0.05
				if self.volup5_button_disabled: self.game.DRsnd_cantselect.play()
				else: self.game.DRsnd_select.play()
			if self.game.soundvol > 1:
				self.game.soundvol = 1
			elif self.game.soundvol < 0:
				self.game.soundvol = 0
			if self.game.soundvol == 1:
				self.volup1_button_disabled = True
				self.volup5_button_disabled = True
			else:
				self.volup1_button_disabled = False
				self.volup5_button_disabled = False
			if self.game.soundvol == 0:
				self.voldown1_button_disabled = True
				self.voldown5_button_disabled = True
			else:
				self.voldown1_button_disabled = False
				self.voldown5_button_disabled = False
			self.game.change_volume()
			self.game.save_settings()

			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.vol_buttons()
			self.game.draw_text('VOLUME SETTINGS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			self.game.draw_text(f'SOUND: {round(self.game.soundvol * 100)}%', int(self.game.font_size * 3/4), self.soundvolx, self.soundvoly, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.UP_BIND).upper()}: -1% - {pygame.key.name(self.game.DOWN_BIND).upper()}: +1% - {pygame.key.name(self.game.LEFT_BIND).upper()}: -5% - {pygame.key.name(self.game.RIGHT_BIND).upper()}: +5%', 15, self.mid_w, self.soundvoly + 25, font_name = self.game.menu2_font)
			self.game.draw_text('Or, use your mouse slider or the buttons below', 15, self.mid_w, self.soundvoly + 50, font_name = self.game.menu2_font)
			self.blit_screen()


	def vol_buttons(self):
		self.vol_button_condition_reload()

		if self.volup1_button_disabled: self.game.display.blit(self.game.imgVolUp1_disabled, self.game.imgVolUp1_rect)
		elif not self.volup1_button_highlighted: self.game.display.blit(self.game.imgVolUp1, self.game.imgVolUp1_rect)
		else: self.game.display.blit(self.game.imgVolUp1_highlight, self.game.imgVolUp1_rect)
		if self.volup5_button_disabled: self.game.display.blit(self.game.imgVolUp5_disabled, self.game.imgVolUp5_rect)
		elif not self.volup5_button_highlighted: self.game.display.blit(self.game.imgVolUp5, self.game.imgVolUp5_rect)
		else: self.game.display.blit(self.game.imgVolUp5_highlight, self.game.imgVolUp5_rect)
		if self.voldown1_button_disabled: self.game.display.blit(self.game.imgVolDown1_disabled, self.game.imgVolDown1_rect)
		elif not self.voldown1_button_highlighted: self.game.display.blit(self.game.imgVolDown1, self.game.imgVolDown1_rect)
		else: self.game.display.blit(self.game.imgVolDown1_highlight, self.game.imgVolDown1_rect)
		if self.voldown5_button_disabled: self.game.display.blit(self.game.imgVolDown5_disabled, self.game.imgVolDown5_rect)
		elif not self.voldown5_button_highlighted: self.game.display.blit(self.game.imgVolDown5, self.game.imgVolDown5_rect)
		else: self.game.display.blit(self.game.imgVolDown5_highlight, self.game.imgVolDown5_rect)

		if self.volup1_button_condition and not self.volup1_button_highlighted:
			if not self.volup1_button_disabled: self.game.DRsnd_menumove.play()
			self.volup1_button_highlighted = True
		elif not self.volup1_button_condition and self.volup1_button_highlighted: self.volup1_button_highlighted = False
		if self.volup5_button_condition and not self.volup5_button_highlighted:
			if not self.volup5_button_disabled: self.game.DRsnd_menumove.play()
			self.volup5_button_highlighted = True
		elif not self.volup5_button_condition and self.volup5_button_highlighted: self.volup5_button_highlighted = False
		if self.voldown1_button_condition and not self.voldown1_button_highlighted:
			if not self.voldown1_button_disabled: self.game.DRsnd_menumove.play()
			self.voldown1_button_highlighted = True
		elif not self.voldown1_button_condition and self.voldown1_button_highlighted: self.voldown1_button_highlighted = False
		if self.voldown5_button_condition and not self.voldown5_button_highlighted:
			if not self.voldown5_button_disabled: self.game.DRsnd_menumove.play()
			self.voldown5_button_highlighted = True
		elif not self.voldown5_button_condition and self.voldown5_button_highlighted: self.voldown5_button_highlighted = False

	def volup1_button_click(self):
		self.nav_button_condition_reload()
		if self.game.CLICK and self.volup1_button_condition and self.volup1_button_highlighted: return True
	
	def volup5_button_click(self):
		self.nav_button_condition_reload()
		if self.game.CLICK and self.volup5_button_condition and self.volup5_button_highlighted: return True

	def voldown1_button_click(self):
		self.nav_button_condition_reload()
		if self.game.CLICK and self.voldown1_button_condition and self.voldown1_button_highlighted: return True
		
	def voldown5_button_click(self):
		self.nav_button_condition_reload()
		if self.game.CLICK and self.voldown5_button_condition and self.voldown5_button_highlighted: return True

	def vol_button_condition_reload(self):
		self.game.imgVolUp1_rect.midleft = (self.mid_w + 1, self.cursor_rect.midtop[1] + 104)
		self.game.imgVolUp5_rect.midleft = (self.mid_w + 71, self.cursor_rect.midtop[1] + 104)
		self.game.imgVolDown1_rect.midright = (self.mid_w - 1, self.cursor_rect.midtop[1] + 104)
		self.game.imgVolDown5_rect.midright = (self.mid_w - 71, self.cursor_rect.midtop[1] + 104)

		volup1_rangex = (self.game.imgVolUp1_rect.topleft[0], self.game.imgVolUp1_rect.topright[0] + 1)
		volup1_rangey = (self.game.imgVolUp1_rect.topleft[1], self.game.imgVolUp1_rect.bottomleft[1] + 1)
		volup5_rangex = (self.game.imgVolUp5_rect.topleft[0], self.game.imgVolUp5_rect.topright[0] + 1)
		volup5_rangey = (self.game.imgVolUp5_rect.topleft[1], self.game.imgVolUp5_rect.bottomleft[1] + 1)
		voldown1_rangex = (self.game.imgVolDown1_rect.topleft[0], self.game.imgVolDown1_rect.topright[0] + 1)
		voldown1_rangey = (self.game.imgVolDown1_rect.topleft[1], self.game.imgVolDown1_rect.bottomleft[1] + 1)
		voldown5_rangex = (self.game.imgVolDown5_rect.topleft[0], self.game.imgVolDown5_rect.topright[0] + 1)
		voldown5_rangey = (self.game.imgVolDown5_rect.topleft[1], self.game.imgVolDown5_rect.bottomleft[1] + 1)
		self.volup1_button_condition = self.game.mousex in range(*volup1_rangex) and self.game.mousey in range(*volup1_rangey)
		self.volup5_button_condition = self.game.mousex in range(*volup5_rangex) and self.game.mousey in range(*volup5_rangey)
		self.voldown1_button_condition = self.game.mousex in range(*voldown1_rangex) and self.game.mousey in range(*voldown1_rangey)
		self.voldown5_button_condition = self.game.mousex in range(*voldown5_rangex) and self.game.mousey in range(*voldown5_rangey)


class ControlsMenu(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)
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
		self.opt11x, self.opt11y = self.mid_w, self.mid_h + 230
		self.offset -= 10
		self.cursor_rect.midtop = (self.opt0x + self.offset, self.opt0y)
		self.checks = 0

		self.menumousex = (self.mid_w - 210, self.mid_w + 210)
		self.opt0mousey = (self.mid_h, self.mid_h + 20)
		self.opt1mousey = (self.mid_h + 20, self.mid_h + 40)
		self.opt2mousey = (self.mid_h + 40, self.mid_h + 60)
		self.opt3mousey = (self.mid_h + 60, self.mid_h + 80)
		self.opt4mousey = (self.mid_h + 80, self.mid_h + 100)
		self.opt5mousey = (self.mid_h + 100, self.mid_h + 120)
		self.opt6mousey = (self.mid_h + 120, self.mid_h + 140)
		self.opt7mousey = (self.mid_h + 140, self.mid_h + 160)
		self.opt8mousey = (self.mid_h + 160, self.mid_h + 180)
		self.opt9mousey = (self.mid_h + 180, self.mid_h + 200)
		self.opt10mousey = (self.mid_h + 200, self.mid_h + 220)
		self.opt11mousey = (self.mid_h + 220, self.mid_h + 240)

	def display_menu(self):
		self.run_display = True
		self.game.save_settings()
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
			self.game.draw_text('REBIND CONTROLS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			self.game.draw_text(f'{pygame.key.name(self.game.START_BIND).upper()} (menu) - Select Option', int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.UP_BIND).upper()} - Move Up', int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.DOWN_BIND).upper()} - Move Down', int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.LEFT_BIND).upper()} - Move Left', int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
			self.game.draw_text(f'{pygame.key.name(self.game.RIGHT_BIND).upper()} - Move Right', int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
			if self.game.allow_ai_snake: self.game.draw_text(f'{pygame.key.name(self.game.X_BIND).upper()} (game) - Toggle AI Snake', int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
			else: self.game.draw_text('??? - ???', int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font, color = self.game.gray)
			if self.game.allow_speed_up: self.game.draw_text(f'{pygame.key.name(self.game.CTRL_BIND).upper()} (game - hold) - Turbo Mode', int(self.game.font_size / 2), self.opt6x, self.opt6y, font_name = self.game.menu2_font)
			else: self.game.draw_text('??? - ???', int(self.game.font_size / 2), self.opt6x, self.opt6y, font_name = self.game.menu2_font, color = self.game.gray)
			self.game.draw_text(f'{pygame.key.name(self.game.BACK_BIND).upper()} - Back/Pause', int(self.game.font_size / 2), self.opt7x, self.opt7y, font_name = self.game.menu2_font)
			if self.game.holidayname == 'halloween':
				self.game.draw_text(f'{pygame.key.name(self.game.SPACE_BIND).upper()} - New Game (game over) /', int(self.game.font_size / 2), self.opt8x, self.opt8y, font_name = self.game.menu2_font)
				self.game.draw_text('Place Poison Apple (Angry Apple)', int(self.game.font_size / 2), self.opt9x, self.opt9y, font_name = self.game.menu2_font)
				self.game.draw_text(f'{pygame.key.name(self.game.MENU_BIND).upper()} (game) - Quit', int(self.game.font_size / 2), self.opt10x, self.opt10y, font_name = self.game.menu2_font)
				self.game.draw_text('RESET TO DEFAULTS', int(self.game.font_size / 2), self.opt11x, self.opt11y, font_name = self.game.menu2_font)
			else:
				self.game.draw_text(f'{pygame.key.name(self.game.SPACE_BIND).upper()} (game over) - New Game', int(self.game.font_size / 2), self.opt8x, self.opt8y, font_name = self.game.menu2_font)
				self.game.draw_text(f'{pygame.key.name(self.game.MENU_BIND).upper()} (game) - Quit', int(self.game.font_size / 2), self.opt9x, self.opt9y, font_name = self.game.menu2_font)
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
				if self.game.allow_ai_snake:
					self.state = 'x'
					self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				elif self.game.allow_speed_up:
					self.state = 'ctrl'
					self.cursor_rect.midtop = (self.opt6x + self.offset, self.opt6y)
				else:
					self.state = 'esc'
					self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
			elif self.state == 'x':
				if self.game.allow_speed_up:
					self.state = 'ctrl'
					self.cursor_rect.midtop = (self.opt6x + self.offset, self.opt6y)
				else:
					self.state = 'esc'
					self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
			elif self.state == 'ctrl':
				self.state = 'esc'
				self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
			elif self.state == 'esc':
				self.state = 'space'
				self.cursor_rect.midtop = (self.opt8x + self.offset, self.opt8y)
			elif self.state == 'space':
				self.state = 'backspace'
				if self.game.holidayname == 'halloween': self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
				else: self.cursor_rect.midtop = (self.opt9x + self.offset, self.opt9y)
			elif self.state == 'backspace':
				self.state = 'reset'
				if self.game.holidayname == 'halloween': self.cursor_rect.midtop = (self.opt11x + self.offset, self.opt11y)
				else: self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
			elif self.state == 'reset':
				self.state = 'enter'
				self.cursor_rect.midtop = (self.opt0x + self.offset, self.opt0y)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'enter':
				self.state = 'reset'
				if self.game.holidayname == 'halloween': self.cursor_rect.midtop = (self.opt11x + self.offset, self.opt11y)
				else: self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
			elif self.state == 'reset':
				self.state = 'backspace'
				if self.game.holidayname == 'halloween': self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
				else: self.cursor_rect.midtop = (self.opt9x + self.offset, self.opt9y)
			elif self.state == 'backspace':
				self.state = 'space'
				self.cursor_rect.midtop = (self.opt8x + self.offset, self.opt8y)
			elif self.state == 'space':
				self.state = 'esc'
				self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
			elif self.state == 'esc':
				if self.game.allow_speed_up:
					self.state = 'ctrl'
					self.cursor_rect.midtop = (self.opt6x + self.offset, self.opt6y)
				elif self.game.allow_ai_snake:
					self.state = 'x'
					self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				else:
					self.state = 'right'
					self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
			elif self.state == 'ctrl':
				if self.game.allow_ai_snake:
					self.state = 'x'
					self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				else:
					self.state = 'right'
					self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
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

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt0mousey) and self.state != 'enter':
				self.cursor_rect.midtop = (self.opt0x + self.offset, self.opt0y)
				self.state = 'enter'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt1mousey) and self.state != 'up':
				self.cursor_rect.midtop = (self.opt1x + self.offset, self.opt1y)
				self.state = 'up'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt2mousey) and self.state != 'down':
				self.cursor_rect.midtop = (self.opt2x + self.offset, self.opt2y)
				self.state = 'down'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt3mousey) and self.state != 'left':
				self.cursor_rect.midtop = (self.opt3x + self.offset, self.opt3y)
				self.state = 'left'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt4mousey) and self.state != 'right':
				self.cursor_rect.midtop = (self.opt4x + self.offset, self.opt4y)
				self.state = 'right'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt5mousey) and self.state != 'x' and self.game.allow_ai_snake:
				self.cursor_rect.midtop = (self.opt5x + self.offset, self.opt5y)
				self.state = 'x'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt6mousey) and self.state != 'ctrl' and self.game.allow_speed_up:
				self.cursor_rect.midtop = (self.opt6x + self.offset, self.opt6y)
				self.state = 'ctrl'
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt7mousey) and self.state != 'esc':
				self.cursor_rect.midtop = (self.opt7x + self.offset, self.opt7y)
				self.state = 'esc'
				self.game.DRsnd_menumove.play()
			elif (self.game.mousey in range(*self.opt8mousey) or (self.game.holidayname == 'halloween' and self.game.mousey in range(*self.opt9mousey))) and self.state != 'space':
				self.cursor_rect.midtop = (self.opt8x + self.offset, self.opt8y)
				self.state = 'space'
				self.game.DRsnd_menumove.play()
			elif ((self.game.holidayname != 'halloween' and self.game.mousey in range(*self.opt9mousey)) or (self.game.holidayname == 'halloween' and self.game.mousey in range(*self.opt10mousey))) and self.state != 'backspace':
				if self.game.holidayname == 'halloween': self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
				else: self.cursor_rect.midtop = (self.opt9x + self.offset, self.opt9y)
				self.state = 'backspace'
				self.game.DRsnd_menumove.play()
			elif ((self.game.holidayname != 'halloween' and self.game.mousey in range(*self.opt10mousey)) or (self.game.holidayname == 'halloween' and self.game.mousey in range(*self.opt11mousey))) and self.state != 'reset':
				if self.game.holidayname == 'halloween': self.cursor_rect.midtop = (self.opt11x + self.offset, self.opt11y)
				else: self.cursor_rect.midtop = (self.opt10x + self.offset, self.opt10y)
				self.state = 'reset'
				self.game.DRsnd_menumove.play()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY or self.game.menu.back_button_click():
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			
			if self.state == 'enter': self.game.START_BIND = self.assign_key(self.game.START_BIND, 'Select Option', self.opt0x, self.opt0y, 'menu')
			elif self.state == 'up': self.game.UP_BIND = self.assign_key(self.game.UP_BIND, 'Move Up', self.opt1x, self.opt1y)
			elif self.state == 'down': self.game.DOWN_BIND = self.assign_key(self.game.DOWN_BIND, 'Move Down', self.opt2x, self.opt2y)
			elif self.state == 'left': self.game.LEFT_BIND = self.assign_key(self.game.LEFT_BIND, 'Move Left', self.opt3x, self.opt3y)
			elif self.state == 'right': self.game.RIGHT_BIND = self.assign_key(self.game.RIGHT_BIND, 'Move Right', self.opt4x, self.opt4y)
			elif self.state == 'x': self.game.X_BIND = self.assign_key(self.game.X_BIND, 'Toggle AI Snake', self.opt5x, self.opt5y, 'game')
			elif self.state == 'ctrl': self.game.CTRL_BIND = self.assign_key(self.game.CTRL_BIND, 'Turbo Mode', self.opt6x, self.opt6y, 'game - hold')
			elif self.state == 'esc': self.game.BACK_BIND = self.assign_key(self.game.BACK_BIND, 'Back/Pause', self.opt7x, self.opt7y)
			elif self.state == 'space':
				if self.game.holidayname == 'halloween':
					self.game.SPACE_BIND = self.assign_key(self.game.SPACE_BIND, 'New Game (game over) /', self.opt8x, self.opt8y)
				else: self.game.SPACE_BIND = self.assign_key(self.game.SPACE_BIND, 'New Game', self.opt8x, self.opt8y, 'game over')
			elif self.state == 'backspace':
				if self.game.holidayname == 'halloween': self.game.MENU_BIND = self.assign_key(self.game.MENU_BIND, 'Quit', self.opt10x, self.opt10y)
				else: self.game.MENU_BIND = self.assign_key(self.game.MENU_BIND, 'Quit', self.opt9x, self.opt9y)
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

		if self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt0mousey):
				self.game.DRsnd_select.play()
				self.game.START_BIND = self.assign_key(self.game.START_BIND, 'Select Option', self.opt0x, self.opt0y, 'menu')
			elif self.game.mousey in range(*self.opt1mousey):
				self.game.DRsnd_select.play()
				self.game.UP_BIND = self.assign_key(self.game.UP_BIND, 'Move Up', self.opt1x, self.opt1y)
			elif self.game.mousey in range(*self.opt2mousey):
				self.game.DRsnd_select.play()
				self.game.DOWN_BIND = self.assign_key(self.game.DOWN_BIND, 'Move Down', self.opt2x, self.opt2y)
			elif self.game.mousey in range(*self.opt3mousey):
				self.game.DRsnd_select.play()
				self.game.LEFT_BIND = self.assign_key(self.game.LEFT_BIND, 'Move Left', self.opt3x, self.opt3y)
			elif self.game.mousey in range(*self.opt4mousey):
				self.game.DRsnd_select.play()
				self.game.RIGHT_BIND = self.assign_key(self.game.RIGHT_BIND, 'Move Right', self.opt4x, self.opt4y)
			elif self.game.mousey in range(*self.opt5mousey) and self.game.allow_ai_snake:
				self.game.DRsnd_select.play()
				self.game.X_BIND = self.assign_key(self.game.X_BIND, 'Toggle AI Snake', self.opt5x, self.opt5y, 'game')
			elif self.game.mousey in range(*self.opt6mousey) and self.game.allow_speed_up:
				self.game.DRsnd_select.play()
				self.game.CTRL_BIND = self.assign_key(self.game.CTRL_BIND, 'Turbo Mode', self.opt6x, self.opt6y, 'game - hold')
			elif self.game.mousey in range(*self.opt7mousey):
				self.game.DRsnd_select.play()
				self.game.BACK_BIND = self.assign_key(self.game.BACK_BIND, 'Back/Pause', self.opt7x, self.opt7y)
			elif self.game.mousey in range(*self.opt8mousey) or (self.game.holidayname == 'halloween' and self.game.mousey in range(*self.opt9mousey)):
				self.game.DRsnd_select.play()
				if self.game.holidayname == 'halloween': self.game.SPACE_BIND = self.assign_key(self.game.SPACE_BIND, 'New Game (game over) /', self.opt8x, self.opt8y)
				else: self.game.SPACE_BIND = self.assign_key(self.game.SPACE_BIND, 'New Game', self.opt8x, self.opt8y, 'game over')
			elif (self.game.holidayname != 'halloween' and self.game.mousey in range(*self.opt9mousey)) or (self.game.holidayname == 'halloween' and self.game.mousey in range(*self.opt10mousey)):
				self.game.DRsnd_select.play()
				if self.game.holidayname == 'halloween': self.game.MENU_BIND = self.assign_key(self.game.MENU_BIND, 'Quit', self.opt10x, self.opt10y)
				else: self.game.MENU_BIND = self.assign_key(self.game.MENU_BIND, 'Quit', self.opt9x, self.opt9y)
			elif (self.game.holidayname != 'halloween' and self.game.mousey in range(*self.opt10mousey)) or (self.game.holidayname == 'halloween' and self.game.mousey in range(*self.opt11mousey)):
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
				

	def assign_key(self, old_value, desc, x, y, paren = None):
		checks = 5
		while checks > 0:
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			if old_value == self.game.SPACE_BIND: self.game.draw_text('Place Poison Apple (Angry Apple)', int(self.game.font_size / 2), self.opt9x, self.opt9y, font_name = self.game.menu2_font)
			self.game.draw_text('REBIND CONTROLS', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size)
			if paren: self.game.draw_text(f'{pygame.key.name(old_value).upper()} ({paren}) - {desc}', int(self.game.font_size / 2), x, y, font_name = self.game.menu2_font)
			else: self.game.draw_text(f'{pygame.key.name(old_value).upper()} - {desc}', int(self.game.font_size / 2), x, y, font_name = self.game.menu2_font)
			self.game.draw_text(f'Press a key within {math.ceil(checks)} seconds to rebind.', int(self.game.font_size / 2), self.opt11x, self.opt11y + 20, font_name = self.game.menu2_font)
			self.blit_screen()
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					return event.key
			pygame.time.delay(1)
			checks -= self.game.deltatime
		return old_value

class PressStart(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)
		self.timer = 0

	def display_menu(self):
		self.run_display = True
		if not self.game.inited:
			self.game.window = self.game.set_window_mode()
			self.game.logo_screen()

			if not self.game.holidaydir: self.game.WIIstart.play()
			self.game.menumus.play(-1)
			self.game.inited = True

		while self.run_display:
			self.game.check_events()
			if self.game.CLICK or self.game.START_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
				self.game.DRsnd_select.play()
			elif self.game.BACK_KEY:
				self.game.running = False
				self.run_display = False
				logger.log('Sneky session closed.\n')
				pygame.quit()
				sys.exit()

			if self.timer >= 2000:
				logger.log('Playing demo.')
				self.game.menumus.fadeout(500)
				pygame.time.delay(500)
				self.game.play_demo()
				logger.log('Demo finished.')
				self.timer = 0
				if not self.game.holidaydir: self.game.WIIstart.play()
				self.game.menumus.play(-1)

			for x in range(0, self.game.DISPLAY_W, 2*self.game.cell_size):
				for y in range(0, self.game.DISPLAY_H, 2*self.game.cell_size):
					pygame.draw.rect(self.game.display,(170, 215, 81),(x,y,self.game.cell_size,self.game.cell_size))
					pygame.draw.rect(self.game.display,(162, 209, 72),(x + self.game.cell_size,y,self.game.cell_size,self.game.cell_size))
				for y in range(0 + self.game.cell_size, self.game.DISPLAY_H, 2*self.game.cell_size):
					pygame.draw.rect(self.game.display,(170, 215, 81),(x + self.game.cell_size,y,self.game.cell_size,self.game.cell_size))
					pygame.draw.rect(self.game.display,(162, 209, 72),(x,y,self.game.cell_size,self.game.cell_size))
			self.game.display.blit(self.game.imgSneky, self.game.imgSneky_rect)
			self.game.display.blit(self.game.imgMenu, self.game.imgMenu_rect)
			self.game.draw_text('v.' + self.game.gameversion, self.game.font_size / 2, 20, self.game.DISPLAY_H - 50, anchor = 'topleft', font_name = self.game.menu2_font)
			self.game.draw_text(self.game.curr_splash, self.game.font_size / 2, self.mid_w, 20, color = self.game.red_god, font_name = self.game.menu2_font)
			self.game.draw_text('PRESS START', self.game.font_size, self.mid_w, int(self.game.DISPLAY_H - 130))
			self.game.draw_text('(c) 2021-2022 GamingWithEvets Inc. All rights go to their respective owners.', int(self.game.font_size/2.5), self.mid_w, int(self.game.DISPLAY_H - int(self.game.font_size/2.5)), font_name = self.game.menu2_font)
			self.blit_screen()
			self.timer += 1

class ModeMenu(Menu):
	def __init__(self,game):
		Menu.init_values(self,game)
		self.allState = ['Classic', 'Apple Bag', 'Portal Border', 'Angry Apple', 'Ultimate Snake', 'De Snake Mode', 'Unknown']
		if self.game.holidayname == 'christmas': self.allState[1], self.allState[3] = 'Treat Bag', 'Angry Candy Cone'
		elif self.game.holidayname == 'halloween': self.allState[1] = 'Poison Apple Hell'
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

		self.menumousex = (self.mid_w - 165, self.mid_w + 160)
		self.opt0mousey = (self.mid_h + 20, self.mid_h + 45)
		self.opt1mousey = (self.mid_h + 45, self.mid_h + 80)
		self.opt2mousey = (self.mid_h + 80, self.mid_h + 115)
		self.opt3mousey = (self.mid_h + 115, self.mid_h + 145)
		self.opt4mousey = (self.mid_h + 145, self.mid_h + 175)
		self.opt5mousey = (self.mid_h + 175, self.mid_h + 205)
		self.opt6mousey = (self.mid_h + 205, self.mid_h + 235)

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
			self.game.draw_tiled_bg(); self.game.display.blit(self.game.imgMenuBG, self.game.imgMenuBG_rect)
			self.game.menu.back_button()
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
				if self.state == self.allState[1]: self.game.draw_text('HIGH SCORE: ' + str(self.game.high_scores['Apple Bag']), self.game.font_size * 3/4, self.mid_w, 100, font_name = self.game.menu2_font)
				elif self.state == self.allState[3]:
					if self.game.holidayname == 'halloween': self.game.draw_text(f'BEST TIME: {self.game.timecode(self.game.angry_apple_halloween_hs)}', self.game.font_size * 3/4, self.mid_w, 100, font_name = self.game.menu2_font)
					else: self.game.draw_text(f'HIGH SCORE: {self.game.high_scores["Angry Apple"]}', self.game.font_size * 3/4, self.mid_w, 100, font_name = self.game.menu2_font)
				else: self.game.draw_text(f'HIGH SCORE: {self.game.high_scores[self.state]}', self.game.font_size * 3/4, self.mid_w, 100, font_name = self.game.menu2_font)
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY or self.game.menu.back_button_click():
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			for state in self.allState:
				if self.state == state:
					self.start_game = True
					if state == 'De Snake Mode': logger.log(state + ' loaded.')
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
					else: self.game.mode(1,1,1, poison_apples = 0); break

		elif self.game.CLICK and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt0mousey):
				self.start_game = True
				self.save_high_score = True
				self.game.mode()
				logger.log('Classic Mode loaded.')
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(*self.opt1mousey) and self.game.allowmode0:
				self.start_game = True
				self.save_high_score = True
				logger.log(self.allState[1] + ' Mode loaded.')
				self.game.mode(apple_bag = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(*self.opt2mousey) and self.game.allowmode1:
				self.start_game = True
				self.save_high_score = True
				logger.log('Portal Border Mode loaded.')
				self.game.mode(portal_border = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(*self.opt3mousey) and self.game.allowmode3:
				self.start_game = True
				self.save_high_score = True
				logger.log(self.allState[3] + ' Mode loaded.')
				self.game.mode(angry_apple = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(*self.opt4mousey) and self.game.allowmode2:
				self.start_game = True
				self.save_high_score = True
				logger.log('Ultimate Snake Mode loaded.')
				self.game.mode(snake_instinct = 1)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(*self.opt5mousey) and self.game.allowmode4:
				self.start_game = True
				logger.log('De Snake Mode loaded.')
				self.game.mode(1,1,1, poison_apples = 0)
				self.game.DRsnd_select.play()

			elif self.game.mousey in range(*self.opt6mousey) and self.game.allowmode4:
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
			if not self.game.holidaydir: self.game.WIIstart.stop()
			self.game.menumus.stop()
			self.game.show_instructions = True
			self.game.save_high_score = self.save_high_score
		elif self.start_game_debug:
			logger.log(f'Loaded custom mode. Settings:\n portal_border: {self.portal_border}\n curled_up: {self.curled_up}\n apple_bag: {self.apple_bag}\n break_border: {self.break_border}\n snake_instinct: {self.snake_instinct}\n angry_apple: {self.angry_apple}\n poison_apples: {self.poison_apples}', tag = 'DEBUG MODE')
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

		if self.game.MOUSEMOVE and self.game.mousex in range(*self.menumousex):
			if self.game.mousey in range(*self.opt0mousey) and self.stateIndex != 0:
				self.cursor_rect.midtop = (self.classicx + self.offset, self.classicy)
				self.stateIndex = 0
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt1mousey) and self.stateIndex != 1 and self.game.allowmode0:
				self.cursor_rect.midtop = (self.appleBagx + self.offset, self.appleBagy)
				self.stateIndex = 1
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt2mousey) and self.stateIndex != 2 and self.game.allowmode1:
				self.cursor_rect.midtop = (self.portalx + self.offset, self.portaly)
				self.stateIndex = 2
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt3mousey) and self.stateIndex != 3 and self.game.allowmode2:
				self.cursor_rect.midtop = (self.angryApplex + self.offset, self.angryAppley)
				self.stateIndex = 3
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt4mousey) and self.stateIndex != 4 and self.game.allowmode3:
				self.cursor_rect.midtop = (self.ultimatex + self.offset, self.ultimatey)
				self.stateIndex = 4
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt5mousey) and self.stateIndex != 5 and self.game.allowmode4:
				self.cursor_rect.midtop = (self.deSnakex + self.offset, self.deSnakey)
				self.stateIndex = 5
				self.state = self.allState[self.stateIndex]
				self.game.DRsnd_menumove.play()
			elif self.game.mousey in range(*self.opt6mousey) and self.stateIndex != 6 and self.game.allowsecretmode:
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
				self.blit_screen('pygame')

		self.portal_border = 0
		self.curled_up = 0
		self.apple_bag = 0
		self.break_border = 0
		self.snake_instinct = 0
		self.angry_apple = 0
		self.poison_apples = 1

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
					elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
						self.poison_apples += 1
						if self.poison_apples == 2: self.poison_apples = 0
					elif event.key == pygame.K_RETURN:
						self.game.mode(self.portal_border, self.curled_up, self.apple_bag, self.break_border, self.snake_instinct, self.angry_apple, self.poison_apples)
						self.start_game_debug = True
						self.debug_run_display = False
					elif event.key == pygame.K_ESCAPE:
						if not self.game.holidaydir: self.game.WIIstart.play()
						self.game.menumus.play(-1)
						self.debug_run_display = False

			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('SNEKY DEBUG MODE', self.game.font_size, self.mid_w, 0, font_name = self.game.pygame_font, anchor = 'midtop')
			self.game.draw_text('NOTE: High scores are NOT saved in this mode.', self.game.font_size, self.mid_w, self.game.font_size, font_name = self.game.pygame_font, anchor = 'midtop')
			self.game.draw_text('portal_border: ' + str(self.portal_border), self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3, font_name = self.game.pygame_font)
			self.game.draw_text('curled_up: ' + str(self.curled_up), self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 2, font_name = self.game.pygame_font)
			self.game.draw_text('apple_bag: ' + str(self.apple_bag), self.game.font_size, self.mid_w, self.mid_h - self.game.font_size, font_name = self.game.pygame_font)
			self.game.draw_text('break_border: ' + str(self.break_border), self.game.font_size, self.mid_w, self.mid_h, font_name = self.game.pygame_font)
			self.game.draw_text('snake_instinct: ' + str(self.snake_instinct), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size, font_name = self.game.pygame_font)
			self.game.draw_text('angry_apple: ' + str(self.angry_apple), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 2, font_name = self.game.pygame_font)
			self.game.draw_text('poison_apples (Halloween theme only!): ' + str(self.poison_apples), self.game.font_size, self.mid_w, self.mid_h + self.game.font_size * 3, font_name = self.game.pygame_font)
			self.game.draw_text('Use number keys 1-7 to toggle between 0 & 1', self.game.font_size, self.mid_w, self.game.DISPLAY_H - self.game.font_size, font_name = self.game.pygame_font, anchor = 'midbottom')
			self.game.draw_text('ENTER: Start - ESC: Return', self.game.font_size, self.mid_w, self.game.DISPLAY_H, font_name = self.game.pygame_font, anchor = 'midbottom')
			self.blit_screen('pygame')