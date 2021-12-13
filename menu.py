import pygame
import sys
import time
import logger

class Menu():
	def __init__(self, game):
		self.game = game
		self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0,0, self.game.font_size, self.game.font_size)
		self.offset = -200

	def draw_cursor(self, size = None):
		if size == None:
			self.game.draw_text('→', 30, self.cursor_rect.x, self.cursor_rect.y, font_name = self.game.arrow_font)
		else:
			self.game.draw_text('→', size, self.cursor_rect.x, self.cursor_rect.y, font_name = self.game.arrow_font)

	def blit_screen(self):
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

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
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

class OptionsMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self,game)
		self.state = 'VOLUME'
		self.volx, self.voly = self.mid_w, self.mid_h + self.game.font_size
		self.controlsx, self.controlsy = self.mid_w, self.mid_h + self.game.font_size *2
		self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('SETTINGS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size * 3/2) 
			self.game.draw_text('VOLUME', int(self.game.font_size * 3/4), self.volx, self.voly) 
			self.game.draw_text('CONTROLS', int(self.game.font_size * 3/4), self.controlsx, self.controlsy) 
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.UP_KEY or self.game.DOWN_KEY:
			if self.state == 'VOLUME':
				self.state = 'CONTROLS'
				self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
			elif self.state == 'CONTROLS':
				self.state = 'VOLUME'
				self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
			self.game.DRsnd_menumove.play()

		elif self.game.START_KEY:
			# TO-DO: Create a Volume Menu and a Controls Menu
			pass

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			if self.state == 'CONTROLS':
				self.game.curr_menu = self.game.controls
				self.game.DRsnd_select.play()
			elif self.state == 'VOLUME':
				self.game.curr_menu = self.game.volumemenu
				self.game.DRsnd_select.play()
			self.run_display = False

class CreditsMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
				self.game.DRsnd_select.play()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('CREDITS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('Menu & Music/SFX Injection: GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, font_name = self.game.menu2_font)
			self.game.draw_text('Menu Template: ChristianD37 - Mode Menu: SeverusFate', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30, font_name = self.game.menu2_font)
			self.game.draw_text('Game & Image Injection: SeverusFate & GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50, font_name = self.game.menu2_font)
			self.game.draw_text('Crash Handler & Logger: GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 70, font_name = self.game.menu2_font)
			self.game.draw_text('Apple Image: Luna4s - Snake & Title Screen Images: GamingWithEvets', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90, font_name = self.game.menu2_font)
			self.game.draw_text('Sounds from DELTARUNE, Google Snake Game, SMB2 USA, Brain Age', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 110, font_name = self.game.menu2_font)
			self.game.draw_text('Music:', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 130, font_name = self.game.menu2_font)
			self.game.draw_text('\"Nintendo Anti-Piracy Self-Reporter\" - Joey Perleoni', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 150, font_name = self.game.menu2_font)
			self.game.draw_text('\"Nothing to Say\" - Md Abdul Kader Zilani', int(self.game.font_size / 2), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 170, font_name = self.game.menu2_font)
			self.blit_screen()

class VolumeMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.state = 'master'
		self.mastervolx, self.mastervoly = self.mid_w, self.mid_h + 10
		self.musicvolx, self.musicvoly = self.mid_w, self.mid_h + 40
		self.soundvolx, self.soundvoly = self.mid_w, self.mid_h + 70
		self.savex, self.savey = self.mid_w, self.mid_h + 100
		self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
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

	def mastervol(self):
		self.mv_run_display = True
		while self.mv_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.mv_run_display = False
				self.game.DRsnd_select.play()
			elif self.game.LEFT_KEY:
				self.game.volume -= 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.RIGHT_KEY:
				self.game.volume += 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.DOWN_KEY:
				self.game.volume -= 0.05
				self.game.DRsnd_menumove.play()
			elif self.game.UP_KEY:
				self.game.volume += 0.05
				self.game.DRsnd_menumove.play()
			if self.game.volume > 1:
				self.game.volume = 1
			elif self.game.volume < 0:
				self.game.volume = 0
			self.game.change_volume()

			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('VOLUME', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('MASTER VOLUME: {0}%'.format(round(self.game.volume * 100)), int(self.game.font_size * 3/4), self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: -1% - {1}: +1% - {2}: +5% - {3}: -5%'.format(pygame.key.name(self.game.UP_BIND).upper(), pygame.key.name(self.game.DOWN_BIND).upper(), pygame.key.name(self.game.LEFT_BIND).upper(), pygame.key.name(self.game.RIGHT_BIND).upper()), 15, self.game.DISPLAY_W / 2, self.mastervoly + 25, font_name = self.game.menu2_font)
			self.blit_screen()

	def musicvol(self):
		self.ms_run_display = True
		while self.ms_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.ms_run_display = False
				self.game.DRsnd_select.play()
			elif self.game.LEFT_KEY:
				self.game.musicvol -= 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.RIGHT_KEY:
				self.game.musicvol += 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.DOWN_KEY:
				self.game.musicvol -= 0.05
				self.game.DRsnd_menumove.play()
			elif self.game.UP_KEY:
				self.game.musicvol += 0.05
				self.game.DRsnd_menumove.play()
			if self.game.musicvol > 1:
				self.game.musicvol = 1
			elif self.game.musicvol < 0:
				self.game.musicvol = 0
			self.game.change_volume()

			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('VOLUME', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('MUSIC: {0}%'.format(round(self.game.musicvol * 100)), int(self.game.font_size * 3/4), self.musicvolx, self.musicvoly, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: -1% - {1}: +1% - {2}: +5% - {3}: -5%'.format(pygame.key.name(self.game.UP_BIND).upper(), pygame.key.name(self.game.DOWN_BIND).upper(), pygame.key.name(self.game.LEFT_BIND).upper(), pygame.key.name(self.game.RIGHT_BIND).upper()), 15, self.game.DISPLAY_W / 2, self.musicvoly + 25, font_name = self.game.menu2_font)
			self.blit_screen()

	def soundvol(self):
		self.sound_run_display = True
		while self.sound_run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.sound_run_display = False
				self.game.DRsnd_select.play()
			elif self.game.LEFT_KEY:
				self.game.soundvol -= 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.RIGHT_KEY:
				self.game.soundvol += 0.01
				self.game.DRsnd_menumove.play()
			elif self.game.DOWN_KEY:
				self.game.soundvol -= 0.05
				self.game.DRsnd_menumove.play()
			elif self.game.UP_KEY:
				self.game.soundvol += 0.05
				self.game.DRsnd_menumove.play()
			if self.game.soundvol > 1:
				self.game.soundvol = 1
			elif self.game.soundvol < 0:
				self.game.soundvol = 0
			self.game.change_volume()

			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('VOLUME', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('SOUND: {0}%'.format(round(self.game.soundvol * 100)), int(self.game.font_size * 3/4), self.soundvolx, self.soundvoly, font_name = self.game.menu2_font)
			self.game.draw_text('{0}: -1% - {1}: +1% - {2}: +5% - {3}: -5%'.format(pygame.key.name(self.game.UP_BIND).upper(), pygame.key.name(self.game.DOWN_BIND).upper(), pygame.key.name(self.game.LEFT_BIND).upper(), pygame.key.name(self.game.RIGHT_BIND).upper()), 15, self.game.DISPLAY_W / 2, self.soundvoly + 25, font_name = self.game.menu2_font)
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
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('REBIND CONTROLS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('{0} (menu) - Select Option'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Cursor/Snake Up'.format(pygame.key.name(self.game.UP_BIND).upper()), int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Cursor/Snake Down'.format(pygame.key.name(self.game.DOWN_BIND).upper()), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Cursor/Snake Left'.format(pygame.key.name(self.game.LEFT_BIND).upper()), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
			self.game.draw_text('{0} - Move Cursor/Snake Right'.format(pygame.key.name(self.game.RIGHT_BIND).upper()), int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
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

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.options
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			self.game.DRsnd_select.play()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('REBIND CONTROLS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('Press a key within 5 seconds to rebind.', 15, self.opt10x, self.opt10y, font_name = self.game.menu2_font)
			if self.state == 'enter':
				self.game.draw_text('{0} (menu) - Select Option'.format(pygame.key.name(self.game.START_BIND).upper()), int(self.game.font_size / 2), self.opt0x, self.opt0y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.START_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'up':
				self.game.draw_text('{0} - Move Cursor/Snake Up'.format(pygame.key.name(self.game.UP_BIND).upper()), int(self.game.font_size / 2), self.opt1x, self.opt1y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.UP_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'down':
				self.game.draw_text('{0} - Move Cursor/Snake Down'.format(pygame.key.name(self.game.DOWN_BIND).upper()), int(self.game.font_size / 2), self.opt2x, self.opt2y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.DOWN_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'left':
				self.game.draw_text('{0} - Move Cursor/Snake Left'.format(pygame.key.name(self.game.LEFT_BIND).upper()), int(self.game.font_size / 2), self.opt3x, self.opt3y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.LEFT_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'right':
				self.game.draw_text('{0} - Move Cursor/Snake Right'.format(pygame.key.name(self.game.RIGHT_BIND).upper()), int(self.game.font_size / 2), self.opt4x, self.opt4y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.RIGHT_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'x':
				self.game.draw_text('{0} (game) - Toggle AI Snake'.format(pygame.key.name(self.game.X_BIND).upper()), int(self.game.font_size / 2), self.opt5x, self.opt5y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.X_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'ctrl':
				self.game.draw_text('{0} (hold) - Turbo Mode'.format(pygame.key.name(self.game.CTRL_BIND).upper()), int(self.game.font_size / 2), self.opt6x, self.opt6y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.CTRL_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'esc':
				self.game.draw_text('{0} - Back/Pause'.format(pygame.key.name(self.game.BACK_BIND).upper()), int(self.game.font_size / 2), self.opt7x, self.opt7y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.BACK_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'space':
				self.game.draw_text('{0} (game over) - New Game'.format(pygame.key.name(self.game.SPACE_BIND).upper()), int(self.game.font_size / 2), self.opt8x, self.opt8y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.SPACE_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
			elif self.state == 'backspace':
				self.game.draw_text('{0} (game) - Quit'.format(pygame.key.name(self.game.MENU_BIND).upper()), int(self.game.font_size / 2), self.opt9x, self.opt9y, font_name = self.game.menu2_font)
				self.blit_screen()
				while self.checks != 5000:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							self.game.MENU_BIND = event.key
							self.checks = 4999
					pygame.time.delay(1)
					self.checks += 1
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
			self.checks = 0

class PressStart(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)

	def display_menu(self):
		self.run_display = True
		self.game.load_music()

		# try importing settings from setting.py
		# needs importing every possible (valid) setting there is,
		# and try clauses aren't restartable, so requires multiple try-except clauses

		try:
			from settings import volume
			self.game.volume = volume
		except Exception:
			pass

		try:
			from settings import musicvol
			self.game.musicvol = musicvol
		except Exception:
			pass

		try:
			from settings import soundvol
			self.game.soundvol = soundvol
		except Exception:
			pass

		try:
			from settings import CTRL_BIND
			self.game.CTRL_BIND = CTRL_BIND
		except Exception:
			pass

		try:
			from settings import START_BIND
			self.game.START_BIND = START_BIND
		except Exception:
			pass

		try:
			from settings import BACK_BIND
			self.game.BACK_BIND = BACK_BIND
		except Exception:
			pass

		try:
			from settings import MENU_BIND
			self.game.MENU_BIND = MENU_BIND
		except Exception:
			pass

		try:
			from settings import SPACE_BIND
			self.game.SPACE_BIND = SPACE_BIND
		except Exception:
			pass

		try:
			from settings import UP_BIND
			self.game.UP_BIND = UP_BIND
		except Exception:
			pass

		try:
			from settings import DOWN_BIND
			self.game.DOWN_BIND = DOWN_BIND
		except Exception:
			pass

		try:
			from settings import LEFT_BIND
			self.game.LEFT_BIND = LEFT_BIND
		except Exception:
			pass

		try:
			from settings import RIGHT_BIND
			self.game.RIGHT_BIND = RIGHT_BIND
		except Exception:
			pass

		self.game.change_volume()
		self.game.NAPSR.play(-1)
		logger.startuplog(self.game.gamestatus, self.game.gameversion)
		while self.run_display:
			self.game.check_events()
			if self.game.START_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
				self.game.DRsnd_select.play()
			self.game.display.blit(self.game.imgMenu, (0, 0))
			if self.game.gamestatus != None and self.game.gamestatus != 'release':
				self.game.draw_text((self.game.gamestatus + ' ' + self.game.gameversion), self.game.font_size / 2, 70, 20, font_name = self.game.menu2_font)
			else:
				self.game.draw_text(('v.' + self.game.gameversion), self.game.font_size / 2, 70, 20, font_name = self.game.menu2_font)
			self.game.draw_text('PRESS START', self.game.font_size, int(self.game.DISPLAY_W/2), int(self.game.DISPLAY_H - 100 - self.game.font_size))
			self.blit_screen()

class ModeMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
		self.allState = ['CLASSIC', 'APPLE BAG', 'PORTAL BORDER', 'ULTIMATE SNAKE', 'ANGRY APPLE', 'DE SNAKE MODE']
		self.stateIndex = 0
		self.state = self.allState[self.stateIndex]
		self.classicx, self.classicy = self.mid_w, self.mid_h + self.game.font_size
		self.appleBagx, self.appleBagy = self.mid_w, self.mid_h + self.game.font_size * 2
		self.portalx, self.portaly = self.mid_w, self.mid_h + self.game.font_size * 3
		self.ultimatex, self.ultimatey = self.mid_w, self.mid_h + self.game.font_size * 4
		self.angryApplex, self.angryAppley = self.mid_w, self.mid_h + self.game.font_size * 5
		self.deSnakex, self.deSnakey = self.mid_w, self.mid_h + self.game.font_size * 6
		self.cursor_rect.midtop = (self.classicx + self.offset, self.classicy)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill((self.game.BLACK))
			self.game.draw_text('SELECT A MODE', self.game.font_size, self.mid_w, self.mid_h - self.game.font_size * 3/2)
			self.game.draw_text('CLASSIC', self.game.font_size * 3/4, self.classicx, self.classicy)
			self.game.draw_text('APPLE BAG', self.game.font_size * 3/4, self.appleBagx, self.appleBagy)
			self.game.draw_text('PORTAL BORDER', self.game.font_size * 3/4, self.portalx, self.portaly)
			self.game.draw_text('ULTIMATE SNAKE', self.game.font_size * 3/4, self.ultimatex, self.ultimatey)
			self.game.draw_text('ANGRY APPLE', self.game.font_size * 3/4, self.angryApplex, self.angryAppley)
			self.game.draw_text( self.allState[5], self.game.font_size * 3/4, self.deSnakex, self.deSnakey)
			self.game.draw_text( self.state, self.game.font_size * 3/4, self.mid_w, 100)
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		self.move_cursor()
		if self.game.BACK_KEY:
			self.game.curr_menu = self.game.main_menu
			self.run_display = False
			self.game.DRsnd_select.play()
		elif self.game.START_KEY:
			if self.state == 'CLASSIC':
				self.game.mode()
				logger.log('Classic Mode loaded.')

			if self.state == 'APPLE BAG':
				logger.log('Apple Bag Mode loaded.')
				self.game.mode(apple_bag = 1)

			if self.state == 'PORTAL BORDER':
				logger.log('Portal Border Mode loaded.')
				self.game.mode(portal_border = 1)

			if self.state == 'ULTIMATE SNAKE':
				logger.log('Ultimate Snake Mode loaded.')
				self.game.mode(snake_instinct = 1)

			if self.state == 'ANGRY APPLE':
				#logger.log('Tried to load Angry Apple mode, but failed (TBA)')
				#self.work_in_progress()
				logger.log('Angry Apple Mode loaded.')
				self.game.mode(angry_apple = 1)

			if self.state == 'DE SNAKE MODE':
				logger.log('De Snake Mode loaded.')
				self.game.mode(1,1,1)

			self.game.playing = True
			self.game.inmenu = False
			self.run_display = False
			self.game.DRsnd_select.play()
			self.game.change_volume()
			self.game.NAPSR.stop()
			self.game.gamemus.play(-1)
			self.game.show_instructions = True

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
			self.game.DRsnd_menumove.play()

	def work_in_progress(self):
		self.run_display = True
		while self.run_display:
			self.blit_screen()
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY :
				self.game.curr_menu = self.game.mode_menu
				self.run_display = False
				self.game.DRsnd_select.play()
			self.game.display.fill(self.game.BLACK)
			self.game.display.blit(self.game.imgMenu, (0, 0))
			self.game.draw_text('TO BE AVAILABLE', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)

if __name__ == '__main__':
	print('Please run main.py to start the game!')
			