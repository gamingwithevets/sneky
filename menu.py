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

	def draw_cursor(self):
		self.game.draw_text('→', 30, self.cursor_rect.x, self.cursor_rect.y, font_name = self.game.arrow_font)

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
			self.game.draw_text('OPTIONS', self.game.font_size, self.optionsx, self.optionsy)
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
			self.game.draw_text('OPTIONS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size * 3/2) 
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
			self.game.draw_text('SAVE SETTINGS', int(self.game.font_size * 3/4), self.savex, self.savey, font_name = self.game.menu2_font)
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
				self.state = 'save'
				self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
			elif self.state == 'save':
				self.state = 'master'
				self.cursor_rect.midtop = (self.mastervolx + self.offset, self.mastervoly)
			self.game.DRsnd_menumove.play()
		elif self.game.UP_KEY:
			if self.state == 'master':
				self.state = 'save'
				self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
			elif self.state == 'save':
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
			elif self.state == 'save':
				# save volume settings to volume.py
				f = open('volume.py', 'w', encoding = 'utf8')
				f.write('# WARNING! This script is auto-generated by Sneky.\n# You should NOT modify it in any way!\n\n')
				f.write('# master volume\nvolume = {0}\n\n'.format(self.game.volume))
				f.write('# music volume\nmusicvol = {0}\n\n'.format(self.game.musicvol))
				f.write('# sound volume\nsoundvol = {0}\n\n'.format(self.game.soundvol))
				f.close()
				self.game.draw_text('Volume settings saved successfully', 15, self.game.DISPLAY_W / 2, self.savey + 25, font_name = self.game.menu2_font)
				self.blit_screen()
				time.sleep(1)
				self.game.reset_keys()


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
			self.game.draw_text('← -1%  → +1%  ↑ +5% ↓ -5%', 15, self.game.DISPLAY_W / 2, self.mastervoly + 25, font_name = self.game.arrow_font)
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
			self.game.draw_text('← -1%  → +1%  ↑ +5% ↓ -5%', 15, self.game.DISPLAY_W / 2, self.musicvoly + 25, font_name = self.game.arrow_font)
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
			self.game.draw_text('← -1%  → +1%  ↑ +5% ↓ -5%', 15, self.game.DISPLAY_W / 2, self.soundvoly + 25, font_name = self.game.arrow_font)
			self.blit_screen()

class ControlsMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			if self.game.START_KEY or self.game.BACK_KEY:
				self.game.curr_menu = self.game.options
				self.run_display = False
				self.game.DRsnd_select.play()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text('GAME CONTROLS', self.game.font_size, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - self.game.font_size)
			self.game.draw_text('↑ ↓ ← → - Move Snake', int(self.game.font_size * 3/4), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10, font_name = self.game.arrow_font)
			self.game.draw_text('X - Toggle AI Snake', int(self.game.font_size * 3/4), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 40, font_name = self.game.menu2_font)
			self.game.draw_text('CTRL (hold) - Turbo Mode', int(self.game.font_size * 3/4), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 70, font_name = self.game.menu2_font)
			self.game.draw_text('ESC - Pause', int(self.game.font_size * 3/4), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 100, font_name = self.game.menu2_font)
			self.game.draw_text('BACKSPACE - Quit', int(self.game.font_size * 3/4), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 130, font_name = self.game.menu2_font)
			self.blit_screen()

class PressStart(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)

	def display_menu(self):
		self.run_display = True
		self.game.load_music()

		# try importing volume settings from volume.py
		# needs importing every possible (valid) volume setting there is,
		# and try clauses aren't restartable, so requires multiple try-except clauses

		try:
			from volume import volume
			self.game.volume = volume
		except Exception:
			pass

		try:
			from volume import musicvol
			self.game.musicvol = musicvol
		except Exception:
			pass

		try:
			from volume import soundvol
			self.game.soundvol = soundvol
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
			