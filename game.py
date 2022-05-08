if __name__ == '__main__':
	print('Please run main.py to start Sneky.')
	sys.exit()

import pygame
import logger

logger.log('Initializing Pygame...\n', allowlog = False)
pygame.init()
logger.log('Pygame initialized, loading Sneky.', allowlog = False)
pygame.display.set_caption('Sneky')

import platform
import sys
import os
from menu import *
import updater
import random
import time
from decimal import *
from pygame import mixer
from datetime import datetime

class Game():
	def __init__(self):
		try:
			self.temp_path = os.path.join(sys._MEIPASS) + '/'
		except Exception:
			self.temp_path = ''
		
		# game version
		self.gamestatus = 'release'
		self.gameversion = '1.2.3-dev4'

		if os.name == 'nt':
			self.playername = os.getenv('USERNAME')
		else:
			self.playername = os.getenv('USER').upper()

		self.mousex, self.mousey = 0, 0

		# default keys
		self.CTRL_BIND = pygame.K_LCTRL
		self.START_BIND = pygame.K_RETURN
		self.BACK_BIND = pygame.K_ESCAPE
		self.MENU_BIND = pygame.K_BACKSPACE
		self.SPACE_BIND = pygame.K_SPACE
		self.UP_BIND = pygame.K_UP
		self.DOWN_BIND = pygame.K_DOWN
		self.LEFT_BIND = pygame.K_LEFT
		self.RIGHT_BIND = pygame.K_RIGHT
		self.X_BIND = pygame.K_x

		# allows modes to be playable or not
		self.allowmode0 = False      # apple bag
		self.allowmode1 = False      # portal border
		self.allowmode2 = False      # ultimate mode
		self.allowmode3 = False      # angry apple
		self.allowmode4 = False      # de snake mode
		self.allowsecretmode = False # unknown

		self.never_entered_unknown = True

		# high scores!!!!1
		self.high_scores = {
		'Classic': 0,
		'Apple Bag': 0,
		'Portal Border': 0,
		'Angry Apple': 0,
		'Ultimate Snake': 0
		}

		self.save_high_score = False

		# allows debug features
		self.allow_ai_snake = False
		self.allow_speed_up = False

		# variables to import on startup, as well as store in settings.py (in sneky appdata folder)
		self.items_to_import = [
		'volume',
		'musicvol',
		'soundvol',
		'CTRL_BIND',
		'START_BIND',
		'BACK_BIND',
		'MENU_BIND',
		'SPACE_BIND',
		'X_BIND',
		'UP_BIND',
		'DOWN_BIND',
		'LEFT_BIND',
		'RIGHT_BIND',
		'allowmode0',
		'allowmode1',
		'allowmode2',
		'allowmode3',
		'allowmode4',
		'allowsecretmode',
		'auto_update',
		'check_prerelease',
		'fullscreen',
		'scaled',
		'native_res',
		'allow_ai_snake',
		'allow_speed_up',
		'never_entered_unknown',
		'high_scores'
		]

		if os.name == 'nt': self.appdata_path = os.getenv('LOCALAPPDATA') + '\\Sneky\\'
		elif os.name == 'posix':
			if platform.system() != 'Darwin': self.appdata_path = os.path.expanduser('~/.config/Sneky/')
			else: self.appdata_path = os.path.expanduser('~/Library/Application Support/Sneky/')

		self.settings_fn = 'settings.py'

		self.running, self.playing, self.inmenu, self.show_instructions, self.newmode, self.newmoded = True, False, True, False, False, False
		self.reset_keys()
		# self.START_KEY, self.BACK_KEY, self.SPACE_KEY, self.CTRL_KEY = False, False, False, False
		# self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False

		self.fullscreen = True
		self.native_res = False
		self.scaled = True

		try:
			self.import_settings('fullscreen', catch = True)
			self.import_settings('scaled', catch = True)
			self.import_settings('native_res', catch = True)
			self.oldsave = False
		except:
			try:
				self.import_settings('fullscreen_mode', catch = True)
				self.oldsave = True
			except:
				self.oldsave = False

		if self.oldsave:
			logger.log('Detected pre-1.2.3 save')
			if self.fullscreen_mode == 0:
				self.fullscreen = True; self.scaled = True; self.native_res = False
				logger.log('Importing video settings from pre-1.2.3 save data: success')
			elif self.fullscreen_mode == 1:
				self.fullscreen = False; self.scaled = False; self.native_res = False
				logger.log('Importing video settings from pre-1.2.3 save data: success')
			elif self.fullscreen_mode == 2:
				self.fullscreen = True; self.scaled = False; self.native_res = False
				logger.log('Importing video settings from pre-1.2.3 save data: success')
			elif self.fullscreen_mode == 3:
				self.fullscreen = False; self.scaled = False; self.native_res = True
				logger.log('Importing video settings from pre-1.2.3 save data: success')
			elif self.fullscreen_mode == 4:
				self.fullscreen = True; self.scaled = False; self.native_res = True
				logger.log('Importing video settings from pre-1.2.3 save data: success')
			else:
				logger.log('Importing video settings from pre-1.2.3 save data: error')

		if os.name == 'nt':
			import ctypes
			user32 = ctypes.windll.user32
			user32.SetProcessDPIAware()
			self.current_w, self.current_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		else:
			try:
				import pyautogui
			except ImportError:
				print('You using a non-Windows OS, yeah?\nI need a module named "pyautogui".\nCan you install it for me?\nOh, and please install Tkinter too.\n(sudo apt-get install python3-tk python3-dev)\nThanks.')
				sys.exit()
			except:
				print('Uh oh! I need Tkinter! You need to sudo apt-get install python3-tk python3-dev')
				sys.exit()
			size = pyautogui.size()
			self.current_w, self.current_h = size[0], size[1]

		# Sneky preset resolution
		self.preset_w, self.preset_h = 800, 600

		try:
			self.window = self.set_window_mode()
		except:
			pygame.quit()
			print('\nUh oh... it seems that you... don\'t have a video driver?\nThis tells me that you\'re probably running Sneky in a dump terminal.\nLike WSL.')
			print('\nIf this happened on a binary YOU compiled, maybe you compiled the binary with WSL?\nAs Pygame doesn\'t really work is WSL, some modules for creating the Pygame window might not exist,\ncausing this error. So try recompiling using a REAL Linux machine!')
			print('\nIf that didn\'t work, or you didn\'t compile the binary with WSL,\nor it happened on my own binaries, PLEASE report it here:\nhttps://github.com/gamingwithevets/sneky/issues')
			sys.exit()

		self.pygame_font = 'default'
		self.arrow_font = self.temp_path + 'fonts/MinecraftRegular.ttf'
		self.menu2_font = self.temp_path + 'fonts/Minecraftia.ttf'
		self.menu_font = self.temp_path + 'fonts/8_BIT_WONDER.TTF'
		self.game_font = self.temp_path + 'fonts/River Adventurer.ttf'
		self.font_size = 32
		self.BLACK, self.WHITE = (0,0,0), (255,255,255)
		self.holidayname = ''
		self.holiday = ''
		self.auto_update = True
		self.check_prerelease = False
		self.updatechecked = False
		self.inited = False
		self.check_holidays()
		self.init_menus()
		self.curr_menu = self.press_start
		self.volume = 1
		self.musicvol = 1
		self.soundvol = 1
		self.showfps = True
		self.limitedfps = False
		self.mode()

	def init_menus(self):
		self.press_start = PressStart(self)
		self.main_menu = MainMenu(self)
		self.options = OptionsMenu(self)
		self.clear_data = ClearData(self)
		self.videomenu = VideoMenu(self)
		self.volumemenu = VolumeMenu(self)
		self.updatemenu = UpdateMenu(self)
		self.updater = Updater(self)
		self.controls = ControlsMenu(self)
		self.credits = CreditsMenu(self)
		self.mode_menu = ModeMenu(self)

	def update_fps(self):
		if self.showfps:
			if self.limitedfps: self.clock.tick(self.FPS)
			else: self.clock.tick()
			fps = self.clock.get_fps()
			self.draw_text(str(int(fps * 10)), int(self.font_size / 3), 0, self.DISPLAY_H, anchor = 'bottomleft', color = self.black, font_name = self.menu2_font)
		pygame.display.update()

	def set_window_mode(self):
		if self.fullscreen:
			if self.native_res:
				if self.scaled:
					self.DISPLAY_W, self.DISPLAY_H = self.preset_w, self.preset_h
					self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
					self.allow_widescreen = False
					return pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.SCALED | pygame.FULLSCREEN)
				else:
					self.DISPLAY_W, self.DISPLAY_H = self.current_w, self.current_h
					self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
					self.allow_widescreen = True
					return pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.FULLSCREEN)
			else: 
				if self.scaled:
					self.DISPLAY_W, self.DISPLAY_H = self.preset_w, self.preset_h
					self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
					self.allow_widescreen = False
					return pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.SCALED | pygame.FULLSCREEN)
				else:
					self.DISPLAY_W, self.DISPLAY_H = self.preset_w, self.preset_h
					self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
					self.allow_widescreen = False
					return pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.FULLSCREEN)
		else:
			if self.native_res:
				self.DISPLAY_W, self.DISPLAY_H = self.current_w, self.current_h
				self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
				self.allow_widescreen = True
				return pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
			else: 
				self.DISPLAY_W, self.DISPLAY_H = self.preset_w, self.preset_h
				self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
				self.allow_widescreen = False
				return pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

	def check_holidays(self):
		# check for Christmas (Dec 21 - Jan 5)
		if (datetime.now().month == 12 and datetime.now().day >= 21) or \
			(datetime.now().month == 1 and datetime.now().day <= 5):
			self.holidayname = 'christmas'
			self.holiday = 'christmas_exclusive/'
		# check for devs' bday (Jan 19/Sep 28)
		elif datetime.now().month == 1 and datetime.now().day == 19:
				self.holidayname = 'bday_gwe'
		elif datetime.now().month == 9 and datetime.now().day == 28:
				self.holidayname = 'bday_sj'
		# check for Sneky's birthday (Dec 10)
		elif datetime.now().month == 12 and datetime.now().day == 10:
				self.holidayname = 'bday_sneky'

	def generate_splash(self):
		self.global_splashes = [
		'Welcome to Sneky!',
		'The snake can die by touching the border in the angry mode!',
		'Avoiding copyright claims is our motto!',
		'Oh hello!',
		'This version of Snake is special!',
		'Please don\'t copyright us :(',
		'Don\'t underestimate Ultra Instinct Sneky\'s power!',
		'Now merged with all holiday Sneky versions!'
		]
		if self.holidayname:
			if self.holidayname == 'christmas':
				self.splashes = [
				'Merry Christmas!',
				'Now with candy cones!',
				'SANTA IS FAKE',
				'Why is there no Christmas tree in Sneky?',
				'This is your Christmas present :)'
				]
			elif self.holidayname == 'bday_gwe':
				self.splashes = [
				'Happy birthday, GamingWithEvets!',
				'Today is GWE\'s birthday! PLEASE celebrate!!!',
				'Today is the birthday of GWE, one of the game devs!'
				]
			elif self.holidayname == 'bday_sj':
				self.splashes = [
				'Happy birthday, SeverusFate!',
				'Happy birthday, Severus Jake!',
				'Today is Severus\'s birthday! PLEASE celebrate!!!',
				'Today is the birthday of Severus, one of the game devs!'
				]
			elif self.holidayname == 'bday_sneky':
				self.splashes = [
				'Today is the day the first public release of Sneky was released!',
				'Happy birthday, Sneky!',
				'',
				'Today\'s the day the first public Sneky release, beta 1.0.4, was uploaded!'
				]
				if datetime.now().year - 2021 == 1:
					self.splashes[2] = 'Today, Sneky is turning 1 year old!'
				else:
					self.splashes[2] = 'Today, Sneky is turning {0} years old!'.format(datetime.now().year - 2021)
		else:
			self.splashes = ['8 ERROR.']
		if random.randint(0, 1) == 0 and not self.holidayname:
			self.curr_splash = self.global_splashes[random.randint(0, len(self.global_splashes) - 1)]
		else:
			self.curr_splash = self.splashes[random.randint(0, len(self.splashes) - 1)]

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running, self.playing = False, False
				self.curr_menu.run_display = False
				self.g_over = False
				logger.log('Sneky session closed.\n')
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == self.START_BIND:
					self.START_KEY = True
				if event.key == self.BACK_BIND:
					self.BACK_KEY = True
				if event.key == self.MENU_BIND:
					self.MENU_KEY = True
				if event.key == self.SPACE_BIND:
					self.SPACE_KEY = True

				if event.key == self.UP_BIND:
					self.UP_KEY = True
				if event.key == self.DOWN_BIND:
					self.DOWN_KEY = True
				if event.key == self.LEFT_BIND:
					self.LEFT_KEY = True
				if event.key == self.RIGHT_BIND:
					self.RIGHT_KEY = True
			elif event.type == pygame.MOUSEMOTION:
				self.MOUSEMOVE = True
				self.mousex, self.mousey = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					self.MOUSESLIDERUP = True
				elif event.button == 5:
					self.MOUSESLIDERDOWN = True
				else:
					self.CLICK = True

	def reset_keys(self):
		self.START_KEY, self.BACK_KEY, self.MENU_KEY, self.SPACE_KEY = False, False, False, False
		self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False
		self.MOUSEMOVE, self.CLICK = False, False
		self.MOUSESLIDERUP, self.MOUSESLIDERDOWN = False, False

	def draw_text(self, text, size, x, y, color = None, font_name = None, screen = None, anchor = 'center'):
		if color == None: color = self.WHITE
		if font_name == self.pygame_font: font_name = None
		elif font_name == None: font_name = self.menu_font
		if screen == None: screen = self.display
		font = pygame.font.Font(font_name, int(size))
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		exec('text_rect.' + anchor + ' = (x,y)')
		screen.blit(text_surface, text_rect)


	def game_loop(self):
		self.new_game()
		self.trans_scr()
		while self.playing:
			self.check_events()
			self.run()
			self.reset_keys()
			if self.g_over:
				self.draw_game_screen()
			
			self.window.blit(self.display, (0,0))

			if self.paused or self.newmode:
				self.trans_scr()

			pygame.display.update()
		
		self.trans_scr()

	def init_intros(self):
		self.snake_instinct_intro = 'certain amount of apples. Let\'s use Sneky\'s powers to win!'
		self.apple_bag_intro = [
		'Multiple apples are spawning! Will Sneky eat them or be hungry?',
		''
		]
		self.portal_border_intro = ''
		self.angry_apple_intro = [
		'You are an angry apple! You\'re tired of Sneky eating all of your apple',
		'friends, so you try to escape him by running out of the playfield!',
		'Escape Sneky to get points. You\'ll get faster, but so does Sneky.',
		]
		self.classic_intro = [
		'You are Sneky! He\'s hungry and wants to eat some delicious apples.',
		'Eat apples to increase your score, and try not to hit the border',
		'or yourself!'
		]
		if self.holidayname:
			if self.holidayname == 'christmas':
				self.snake_instinct_intro = 'certain amount of candy cones. Let\'s use Sneky\'s powers to win!'
				self.apple_bag_intro = [
				'Santa\'s giving out more candy cones! Sneky doesn\'t hesitate',
				'to eat \'em!'
				]
				self.portal_border_intro = 'Time to get some treats from Santa!'
				self.angry_apple_intro = [
				'You are an angry candy cone! You see that Sneky has eaten too much cones',
				'and isn\'t stopping! He\'s gonna get fat at this rate. So you try to',
				'escape him! Then you\'ll get a point and you and Sneky will speed up.',
				]
				self.classic_intro = [
				'It\'s Christmas! Sneky wants Santa\'s candy cones! Eat \'em and don\'t',
				'touch yourself or the border, or you\'ll die!',
				''
				]


	def trans_scr(self):
		
		if self.g_over:
			self.draw_game_screen()

			# fade diplay
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

			# save scores
			if self.save_high_score:
				if self.angry_apple == 1:
					if self.score > self.high_scores['Angry Apple']: self.high_scores['Angry Apple'] = self.score
				if self.ai_snake == 0:
					if self.snake_instinct == 1:
						if self.score > self.high_scores['Ultimate Snake']: self.high_scores['Ultimate Snake'] = self.score
					elif self.apple_bag == 1:
						if self.score > self.high_scores['Apple Bag']: self.high_scores['Apple Bag'] = self.score
					elif self.portal_border == 1:
						if self.score > self.high_scores['Portal Border']: self.high_scores['Portal Border'] = self.score
					else:
						if self.score > self.high_scores['Classic']: self.high_scores['Classic'] = self.score

			# gameover text
			self.gamemus.stop()
			if self.win:
				logger.log('No more apples on the playfield!')
				if self.ai_snake == 0:
					logger.log('Player ' + self.playername + ' won!')
					self.draw_text('YOU WIN!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				else:
					if self.angry_apple == 0:
						self.draw_text('CHEATER...', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
						logger.log('My my! What a cheater you are!\nYour score will not be saved.')
					else:
						self.draw_text('YOU WIN!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
						logger.log('Sneky died!')
						logger.log('You will pay for this...')
						self.GSdie.play()
				self.GSwin.play()
			else:
				logger.log('Sneky died!')
				if self.ai_snake == 0:
					logger.log('Player ' + self.playername + ' lost!')
					self.draw_text('YOU DIED!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
					self.GSdie.play()
				else:
					if self.angry_apple == 0:
						self.draw_text('JUST LIKE THEY ALWAYS SAY, CHEATERS NEVER WIN.', int(self.font_size / 1.25), self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
						logger.log('Cheaters never win. And you cheated and lost.\nYour score will not be saved.')
						self.GSdie.play()
					else:
						self.draw_text('YOU DIED!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
						logger.log('Sneky ate the Angry Apple!')
						self.SMB2down.play()
			self.draw_text('{0}: New Game'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.game_font, screen = self.window)
			self.draw_text('{0}/{1}: Quit'.format(pygame.key.name(self.BACK_BIND).upper(), pygame.key.name(self.MENU_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.game_font, screen = self.window)

			# self.window.blit(self.over_text, self.over_rect)
			pygame.display.update()

			while self.g_over:

				self.update_fps()

				# check input
				self.check_events()
				if self.BACK_KEY or self.MENU_KEY:
					self.g_over = False
				if self.SPACE_KEY:
					self.playing = True
					self.g_over = False
					self.reset_keys()
					logger.log('Player ' + self.playername + ' decides to play again!')
					self.gamemus.play(-1)
					self.game_loop()
				self.reset_keys()

		elif self.paused:
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

			# save scores
			if self.save_high_score:
				if self.snake_instinct == 1:
					if self.score > self.high_scores['Ultimate Snake']: self.high_scores['Ultimate Snake'] = self.score
				elif self.apple_bag == 1:
					if self.score > self.high_scores['Apple Bag']: self.high_scores['Apple Bag'] = self.score
				elif self.portal_border == 1:
					if self.score > self.high_scores['Portal Border']: self.high_scores['Portal Border'] = self.score
				elif self.angry_apple == 1:
					if self.score > self.high_scores['Angry Apple']: self.high_scores['Angry Apple'] = self.score
				else:
					if self.score > self.high_scores['Classic']: self.high_scores['Classic'] = self.score

			# gameover text
			self.draw_text('GAME PAUSED', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
			logger.log('Player ' + self.playername + ' paused the game!')
			self.draw_text('{0}: Resume Game'.format(pygame.key.name(self.BACK_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.game_font, screen = self.window)
			self.draw_text('{0}: Quit'.format(pygame.key.name(self.MENU_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.game_font, screen = self.window)

				# self.window.blit(self.over_text, self.over_rect)
			pygame.mixer.pause()
			self.SMB3pause.play()
			pygame.display.update()

			while self.paused:

				self.update_fps()

				# check input
				self.check_events()
				if self.MENU_KEY:
					self.paused = False
					self.playing = False
					self.reset_keys()
				if self.BACK_KEY:
					self.paused = False
					self.reset_keys()
					pygame.mixer.unpause()
					self.SMB3pause.play()
					logger.log('Player ' + self.playername + ' unpaused the game!')
					return

		elif self.show_instructions:
			self.draw_game_screen()
			self.window.blit(self.display, (0,0))

			# fade diplay
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

			# game instructions
			self.init_intros()
			if self.portal_border == 1 and self.curled_up == 1 and self.apple_bag == 1:
				self.draw_text(self.mode_menu.allState[5], self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text('The Debug Mode of Sneky. Like cheating? This is for you!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text('Sneky can now walk through himself, turn around, and even', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
				self.draw_text('walk through the portal borders!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 4, font_name = self.menu2_font, screen = self.window)
				self.draw_text('NOTE: No high scores will be saved in this mode.', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 5, font_name = self.menu2_font, screen = self.window)
			elif self.snake_instinct == 1:
				self.draw_text(self.mode_menu.allState[4], self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text('Sneky switches color and power every time you collect a', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.snake_instinct_intro, self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
			elif self.apple_bag == 1:
				self.draw_text(self.mode_menu.allState[1], self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text(self.apple_bag_intro[0], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.apple_bag_intro[1], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
			elif self.portal_border == 1:
				self.draw_text(self.mode_menu.allState[2], self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text('The border\'s now a portal to the other side of the playfield!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.portal_border_intro, self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
			elif self.angry_apple == 1:
				self.draw_text(self.mode_menu.allState[3], self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text(self.angry_apple_intro[0], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.angry_apple_intro[1], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.angry_apple_intro[2], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 4, font_name = self.menu2_font, screen = self.window)
				self.draw_text('If Sneky dies, you win! But if he eats you, you lose!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 5, font_name = self.menu2_font, screen = self.window)
			else:
				self.draw_text(self.mode_menu.allState[0], self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text(self.classic_intro[0], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.classic_intro[1], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.classic_intro[2], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 4, font_name = self.menu2_font, screen = self.window)

			self.draw_text('{0}: Start'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 7, font_name = self.game_font, screen = self.window)
			self.draw_text('{0}/{1}: Quit'.format(pygame.key.name(self.BACK_BIND).upper(), pygame.key.name(self.MENU_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 8, font_name = self.game_font, screen = self.window)

			# self.window.blit(self.over_text, self.over_rect)
			pygame.display.update()

			while self.show_instructions:

				self.update_fps()

				# check input
				self.check_events()
				if self.BACK_KEY or self.MENU_KEY:
					self.show_instructions = False
					self.playing = False
				if self.SPACE_KEY:
					self.reset_keys()
					self.show_instructions = False
					self.gamemus.play(-1)
					return
				self.reset_keys()

		elif self.newmode:
			self.draw_game_screen()
			self.window.blit(self.display, (0,0))

			# fade diplay
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

			# save scores
			if self.save_high_score:
				if self.snake_instinct == 1:
					if self.score > self.high_scores['Ultimate Snake']: self.high_scores['Ultimate Snake'] = self.score
				elif self.apple_bag == 1:
					if self.score > self.high_scores['Apple Bag']: self.high_scores['Apple Bag'] = self.score
				elif self.portal_border == 1:
					if self.score > self.high_scores['Portal Border']: self.high_scores['Portal Border'] = self.score
				elif self.angry_apple == 1:
					if self.score > self.high_scores['Angry Apple']: self.high_scores['Angry Apple'] = self.score
				else:
					if self.score > self.high_scores['Classic']: self.high_scores['Classic'] = self.score

			# new mode message
			if self.allowsecretmode:
				self.draw_text('...!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text('You suddenly hear a secret door opening...', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size, font_name = self.menu2_font, screen = self.window)
				self.draw_text('maybe you should go check?', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text('{0}: Yeah, sure'.format(pygame.key.name(self.BACK_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 4, font_name = self.game_font, screen = self.window)
				self.draw_text('{0}: Nah, later'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 5, font_name = self.game_font, screen = self.window)
			elif self.allow_ai_snake and self.allow_speed_up:
				self.draw_text('CONGRATS...', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text('You have reached the HARDEST part of Ultimate Snake Mode.', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size, font_name = self.menu2_font, screen = self.window)
				self.draw_text('Now Sneky can go right through the border, but doesn\'t', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 1.5, font_name = self.menu2_font, screen = self.window)
				self.draw_text('teleport to the other side of the playfield anymore.', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text('Good luck trying not to lose track of Sneky while he\'s', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2.5, font_name = self.menu2_font, screen = self.window)
				self.draw_text('out of bounds!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
				self.draw_text('You\'ve also unlocked De Snake Mode and 2 debugging', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 4, font_name = self.menu2_font, screen = self.window)
				self.draw_text('features: the AI Snake mode and the Turbo Mode.', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 4.5, font_name = self.menu2_font, screen = self.window)
				self.draw_text('Can you take on the challenge or do you wanna quit?', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 5, font_name = self.menu2_font, screen = self.window)
				self.draw_text('{0}: I\'ll quit'.format(pygame.key.name(self.BACK_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 6, font_name = self.game_font, screen = self.window)
				self.draw_text('{0}: I\'ll try my best to win'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 7, font_name = self.game_font, screen = self.window)
			else:
				self.draw_text('NEW MODE UNLOCKED!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				self.draw_text('You have unlocked: ' + self.thenewmode, self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size, font_name = self.menu2_font, screen = self.window)
				self.draw_text('Do you want to try it out?', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text('{0}: Yeah sure'.format(pygame.key.name(self.BACK_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.game_font, screen = self.window)
				self.draw_text('{0}: Nah I\'m good'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 4, font_name = self.game_font, screen = self.window)

			pygame.mixer.pause()
			self.DRsnd_won.play()
			# self.window.blit(self.over_text, self.over_rect)
			pygame.display.update()

			self.save_settings()

			while self.newmode:

				self.update_fps()

				# check input
				self.check_events()
				if self.BACK_KEY or self.MENU_KEY:
					self.newmode = False
					self.playing = False
				if self.SPACE_KEY:
					self.reset_keys()
					self.newmode = False
					self.newmoded = True
					pygame.mixer.unpause()
					return
				self.reset_keys()

		if not self.inmenu and not self.playing:
			logger.log('Player ' + self.playername + ' quit the game!')
			self.show_instructions = False
			self.inmenu = True
			self.gamemus.stop()
			self.WIIstart.play()
			self.menumus.play(-1)

	def show_turbo(self):
		if self.turbo:
			if self.angry_apple == 0:
				self.draw_text('TURBO MODE IS ON', 25, self.DISPLAY_W / 2, 30, self.red, self.game_font)
			else:
				self.draw_text('YOU AND SNEKY SPED UP!', 15, self.DISPLAY_W / 2 - 50, 30, self.red, self.game_font)

	def draw_game_screen(self):
		# white BG
		self.display.fill(self.WHITE)

		# speed
		if not self.turbo:
			pygame.time.delay(int(self.speed))
		else:
			if self.allow_speed_up:
				if self.angry_apple == 0:
					pygame.time.delay(0)
				else:
					pygame.time.delay(100)
					
		self.show_turbo()

		self.update_fps()

		#score
		self.show_score()

		# speed
		self.show_speed()

		# apple pos
		#self.draw_text('Apple: {0}, {1}'.format(self.apple[0], self.apple[1]), 25, 100, 30, self.gray, self.game_font)

		# snake pos
		#self.draw_text('Snake: {0}, {1}'.format(self.snake_head[0], self.snake_head[1]), 25, self.DISPLAY_W / 2 - 50, 30, self.gray, self.game_font)

		# apple_bag pos
		#self.draw_text('Last Apple: {0}, {1}'.format(self.apple_List[0][0], self.apple_List[0][1]), 25, 100, 30, self.gray, self.game_font)

		# playfield
		for x in range(self.border_x, self.DISPLAY_W - 20, 40):
			for y in range(self.border_y, self.DISPLAY_H - 20, 40):
				pygame.draw.rect(self.display,(170, 215, 81),(x,y,self.cell_size,self.cell_size))
				pygame.draw.rect(self.display,(162, 209, 72),(x + 20,y,self.cell_size,self.cell_size))
			for y in range(self.border_y + 20, self.DISPLAY_H - 20, 40):
				pygame.draw.rect(self.display,(170, 215, 81),(x + 20,y,self.cell_size,self.cell_size))
				pygame.draw.rect(self.display,(162, 209, 72),(x,y,self.cell_size,self.cell_size))

		# border
		pygame.draw.rect(self.display,self.gray,(self.border_x,self.border_y,self.DISPLAY_W - self.border_x - 20,self.DISPLAY_H - self.border_y - 20),10)        

		if self.snake_instinct == 1:
			if self.score < 10:
				self.apple_bag = 1
			if self.score == 10:
				self.apple_bag = 0
			if self.score == 20:
				self.curled_up = 1
			if self.score == 30:
				self.portal_border = 1
			if self.score == 90:
				self.break_border = 1

		# snake color
		if self.break_border == 1:
		   self.snake_color = self.ultra_white
		elif self.portal_border == 1:
			self.snake_color = self.light_blue
		elif self.curled_up == 1:
			self.snake_color = self.red_god
		elif self.apple_bag == 1:
			self.snake_color = self.super_yellow    
		else:
			self.snake_color = self.green

		# draw snake body
		for s in self.snake:
			pygame.draw.rect(self.display, self.snake_color,(s[0],s[1],self.cell_size,self.cell_size))
			#self.display.blit(self.body_default,pygame.Rect(s[0], s[1], self.cell_size, self.cell_size))

			#self.display.blit(self.imgTail_u,pygame.Rect(s[0], s[1], self.cell_size, self.cell_size))
		
		# draw snake tail
		#self.display.blit(self.imgTail_u,pygame.Rect(self.snake[-1][0], self.snake[-1][1], self.cell_size, self.cell_size))
		
		# draw snake head
		#pygame.draw.rect(self.display,self.green,(self.snake_head[0],self.snake_head[1],self.cell_size,self.cell_size))

		# draw apple
		for ap in self.apple_List:
			self.display.blit(self.imgApple,pygame.Rect(ap[0], ap[1], self.cell_size, self.cell_size))
		#self.display.blit(self.imgApple,pygame.Rect(self.apple[0], self.apple[1], self.cell_size, self.cell_size))

		if self.g_over:
			if not self.win:
				if self.angry_apple == 0:
					self.display.blit(self.imgHead_die,pygame.Rect(self.snake[0][0], self.snake[0][1], self.cell_size, self.cell_size))
					self.draw_hat(self.snake[0][0], self.snake[0][1])
				else:
					self.display.blit(self.imgHead_win,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
					self.draw_hat()
			else:
				if self.angry_apple == 0:
					self.display.blit(self.imgHead_win,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
					self.draw_hat()
				else:
					self.display.blit(self.imgHead_die,pygame.Rect(self.snake[0][0], self.snake[0][1], self.cell_size, self.cell_size))
					self.draw_hat(self.snake[0][0], self.snake[0][1])
			
		else:
			if self.direction == 'RIGHT':
				self.display.blit(self.imgHead_r,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
				self.draw_hat()
			if self.direction == 'LEFT':
				self.display.blit(self.imgHead_l,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
				self.draw_hat()
			if self.direction == 'UP':
				self.display.blit(self.imgHead_u,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
				self.draw_hat()
			if self.direction == 'DOWN':
				self.display.blit(self.imgHead_d,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
				self.draw_hat()

	def draw_hat(self, snakepos0 = None, snakepos1 = None):
		if self.holidayname:
			if self.holidayname == 'christmas':
				if snakepos0 == None:
					snakepos0 = self.snake_head[0]
				if snakepos1 == None:
					snakepos1 = self.snake_head[1]

				if self.direction == 'RIGHT':
					self.display.blit(self.imgHead_hat,pygame.Rect(snakepos0, snakepos1 - self.cell_size, self.cell_size, self.cell_size))
				if self.direction == 'LEFT':
					self.display.blit(self.imgHead_hat,pygame.Rect(snakepos0, snakepos1 - self.cell_size, self.cell_size, self.cell_size))
				if self.direction == 'UP':
					self.display.blit(self.imgHead_hat,pygame.Rect(snakepos0, snakepos1 - (self.cell_size + 3), self.cell_size, self.cell_size))
				if self.direction == 'DOWN':
					self.display.blit(self.imgHead_hat,pygame.Rect(snakepos0, snakepos1 - (self.cell_size + 3), self.cell_size, self.cell_size))

	def move_apple(self):
		key_pressed = pygame.key.get_pressed()
		if key_pressed[self.UP_BIND]:
			self.apple_List[0][1] -= self.cell_size
		elif key_pressed[self.DOWN_BIND]:
			self.apple_List[0][1] += self.cell_size
		elif key_pressed[self.RIGHT_BIND]:
			self.apple_List[0][0] += self.cell_size
		elif key_pressed[self.LEFT_BIND]:
			self.apple_List[0][0] -= self.cell_size

		if (self.apple_List[0][0] >= self.DISPLAY_W - 20
		or self.apple_List[0][0] <= self.border_x - 10
		or self.apple_List[0][1] >= self.DISPLAY_H - 20
		or self.apple_List[0][1] <= self.border_y - 10):
			self.score += 1
			del self.apple_List[0]
			self.BAcorrect.play()
			self.disallowpopping = True
			if int(self.speed) > 0:
				self.speed *= 0.97
			else:
				self.speed -= 0.5
			
			self.spawn_apple()

	def spawn_apple(self):
		if self.angry_apple == 1:
			while True:
				# generate 1 apple
				apple_x = random.randrange(self.border_x,self.DISPLAY_W-self.border_x,20)
				apple_y = random.randrange(self.border_y,self.DISPLAY_H-self.border_y,20)
				self.apple = [apple_x, apple_y]
				if self.apple not in self.snake:
					self.apple_List.insert(-1,self.apple)
					break
		else:
			if self.apple_bag == 0:
				if self.snake_instinct == 0:
					while True:
						# generate 1 apple
						apple_x = random.randrange(self.border_x,self.DISPLAY_W-self.border_x,20)
						apple_y = random.randrange(self.border_y,self.DISPLAY_H-self.border_y,20)
						self.apple = [apple_x, apple_y]
						if self.apple not in self.snake:
							self.apple_List.insert(-1,self.apple)
							break
				else:
					# generate apple = score divide by 10
					if len(self.apple_List) <= 10:
						for i in range(int(self.score // 10)):
							apple_x = random.randrange(self.border_x,self.DISPLAY_W - 20,20)
							apple_y = random.randrange(self.border_y,self.DISPLAY_H - 20,20)
							self.apple = [apple_x, apple_y]
							if self.apple not in self.apple_List and self.apple not in self.snake:
								self.apple_List.insert(-1,self.apple)
								break
			else:
				# generate apple bag = score
				for i in range(self.score):
					apple_x = random.randrange(self.border_x,self.DISPLAY_W - 20,20)
					apple_y = random.randrange(self.border_y,self.DISPLAY_H - 20,20)
					self.apple = [apple_x, apple_y]
					if self.apple not in self.apple_List and self.apple not in self.snake:
						self.apple_List.insert(-1,self.apple)

	def run(self):

		self.turbo = False
		# check function input
		if self.BACK_KEY:
			self.paused = True
		elif self.MENU_KEY:
			self.playing = False


		key_pressed = pygame.key.get_pressed()
		if key_pressed[self.X_BIND]:
			if self.allow_ai_snake:
				if self.angry_apple == 0:
					if self.ai_snake:
						logger.log('AI Snake off.')
					else:
						logger.log('AI Snake on. The game will now play itself!')
					self.ai_snake = not self.ai_snake
				else:
					logger.log('AI Snake cannot be toggled in Angry Apple mode.')


		if key_pressed[self.CTRL_BIND]:
			if self.angry_apple == 0:
				if self.speed > 0: self.turbo = True
			else:
				if self.speed > 100: self.turbo = True

		self.draw_game_screen()
		
		# auto mode
		if self.ai_snake == 1:
			if self.angry_apple == 0:
				try:
					pygame.draw.rect(self.display,self.red,(self.apple_List[0][0],self.apple_List[0][1],self.cell_size,self.cell_size))
				except IndexError:
					self.playing = False
					self.g_over = True
					self.win = True
					return

			if self.curled_up == 0:
				if (self.apple_List[0][1] < self.snake_head[1] and self.direction != 'DOWN'
				and not self.snake_head[1] - self.cell_size <= self.border_y - 10
				and [self.snake_head[0],self.snake_head[1] - self.cell_size] not in self.snake):
					if self.direction != 'UP':
						self.direction = 'UP'
						self.allowmovesound = True

				elif (self.apple_List[0][1] > self.snake_head[1] and self.direction != 'UP' 
				and not self.snake_head[1] + self.cell_size >= self.DISPLAY_H - 20	
				and [self.snake_head[0],self.snake_head[1] + self.cell_size] not in self.snake):
					if self.direction != 'DOWN':
						self.direction = 'DOWN'
						self.allowmovesound = True

				elif (self.apple_List[0][0] > self.snake_head[0] and self.direction != 'LEFT' 
				and not self.snake_head[0] + self.cell_size >= self.DISPLAY_W - 20
				and [self.snake_head[0] + self.cell_size,self.snake_head[1]] not in self.snake):
					if self.direction != 'RIGHT':
						self.direction = 'RIGHT'
						self.allowmovesound = True

				elif (self.apple_List[0][0] < self.snake_head[0] and self.direction != 'RIGHT' 
				and not self.snake_head[0] - self.cell_size <= self.border_x - 10
				and [self.snake_head[0] - self.cell_size,self.snake_head[1]] not in self.snake):
					if self.direction != 'LEFT':
						self.direction = 'LEFT'
						self.allowmovesound = True

				elif self.direction == 'RIGHT' or self.direction == 'LEFT':
					if [self.snake_head[0],self.snake_head[1] - self.cell_size] not in self.snake:
						if self.direction != 'UP':
							self.direction = 'UP'
							self.allowmovesound = True
					else:
						if self.direction != 'DOWN':
							self.direction = 'DOWN'
							self.allowmovesound = True

				elif self.direction == 'UP' or self.direction == 'DOWN':
					if [self.snake_head[0] + self.cell_size,self.snake_head[1]] not in self.snake:
						if self.direction != 'RIGHT':
							self.direction = 'RIGHT'
							self.allowmovesound = True
					else:
						if self.direction != 'LEFT':
							self.direction = 'LEFT'
							self.allowmovesound = True

			else:
				if self.apple_List[0][1] < self.snake_head[1]:
					if self.direction != 'UP':
						self.direction = 'UP'
						self.allowmovesound = True
				elif self.apple_List[0][1] > self.snake_head[1]:
					if self.direction != 'DOWN':
						self.direction = 'DOWN'
						self.allowmovesound = True
				elif self.apple_List[0][0] > self.snake_head[0]:
					if self.direction != 'RIGHT':
						self.direction = 'RIGHT'
						self.allowmovesound = True
				elif self.apple_List[0][0] < self.snake_head[0]:
					if self.direction != 'LEFT':
						self.direction = 'LEFT'
						self.allowmovesound = True

		if self.angry_apple == 0:
			if self.ai_snake == 0:
				# check input
				if self.curled_up == 0:
					if self.UP_KEY and self.direction != 'DOWN' and self.direction != 'UP':
						self.direction = 'UP'
						self.allowmovesound = True
					elif self.DOWN_KEY and self.direction != 'UP' and self.direction != 'DOWN':
						self.direction = 'DOWN'
						self.allowmovesound = True
					elif self.RIGHT_KEY and self.direction != 'LEFT' and self.direction != 'RIGHT':
						self.direction = 'RIGHT'
						self.allowmovesound = True
					elif self.LEFT_KEY and self.direction != 'RIGHT' and self.direction != 'LEFT':
						self.direction = 'LEFT'
						self.allowmovesound = True
				else:
					if self.UP_KEY and self.direction != 'UP':
						self.allowmovesound = True
						self.direction = 'UP'
					elif self.DOWN_KEY and self.direction != 'DOWN':
						self.direction = 'DOWN'
						self.allowmovesound = True
					elif self.RIGHT_KEY and self.direction != 'RIGHT':
						self.direction = 'RIGHT'
						self.allowmovesound = True
					elif self.LEFT_KEY and self.direction != 'LEFT':
						self.direction = 'LEFT'
						self.allowmovesound = True

		else:
			self.move_apple()

		# check direction
		if self.direction == 'UP':
			if self.allowmovesound:
				self.GSmove_u.play()
				self.allowmovesound = False
				self.UP_KEY = False
			self.snake_head[1] -= self.cell_size
		elif self.direction == 'DOWN':
			if self.allowmovesound:
				self.GSmove_d.play()
				self.allowmovesound = False
				self.DOWN_KEY = False
			self.snake_head[1] += self.cell_size
		elif self.direction == 'RIGHT':
			if self.allowmovesound:
				self.GSmove_r.play()
				self.allowmovesound = False
				self.RIGHT_KEY = False
			self.snake_head[0] += self.cell_size
		elif self.direction == 'LEFT':
			if self.allowmovesound:
				self.GSmove_l.play()
				self.allowmovesound = False
				self.LEFT_KEY = False
			self.snake_head[0] -= self.cell_size
		
		# direction
		#self.draw_text('Direction: ' + self.direction, 25, 350, 30, self.gray, self.game_font)

		# eat yourself
		if self.curled_up == 0 and self.snake_head in self.snake:
			pygame.draw.rect(self.display, self.snake_color,(self.snake[0][0],self.snake[0][1],self.cell_size,self.cell_size))
			self.playing = False
			self.g_over = True
			if self.angry_apple == 1:
				self.win = True
		
		if self.break_border == 0:
		#hit border
			if (self.snake_head[0] >= self.DISPLAY_W - 20
			or self.snake_head[0] <= self.border_x - 10
			or self.snake_head[1] >= self.DISPLAY_H - 20
			or self.snake_head[1] <= self.border_y - 10):
				if self.portal_border == 0:
					# snake border die
					pygame.draw.rect(self.display, self.snake_color,(self.snake[0][0],self.snake[0][1],self.cell_size,self.cell_size))
					self.playing = False
					self.g_over = True
					if self.angry_apple == 1:
						self.win = True

				else:
					# portal border
					if self.snake_head[0] <= self.border_x - 15:
						self.snake_head[0] = self.DISPLAY_W - 2 * self.cell_size
						self.GSportal.play()
					elif self.snake_head[0] >= self.DISPLAY_W - self.cell_size:
						self.snake_head [0] = self.border_x
						self.GSportal.play()
					elif self.snake_head[1] >= self.DISPLAY_H - self.cell_size:
						self.snake_head[1] = self.border_y
						self.GSportal.play()
					elif self.snake_head[1] <= self.border_y - 15:
						self.snake_head[1] = self.DISPLAY_H - 2 * self.cell_size
						self.GSportal.play()
		
		# snake moving
		if not self.g_over:
			self.snake.insert(0, list(self.snake_head))
		
		# eat apple
		if self.snake_head in self.apple_List:
			self.GSeatapple.play()
			self.apple_List.remove(self.snake_head)
			if self.angry_apple == 0:
				self.score += 1
			else:
				self.window.blit(self.display, (0,0))
				pygame.display.update()
				self.playing = False
				self.g_over = True
				return
			
			if int(self.speed) > 0:
					self.speed *= 0.97
			else:
				self.speed -= 0.5

			# generate apple
			self.spawn_apple()			
				
		else:
			if not self.disallowpopping:
				if not self.g_over:
					self.snake.pop()
			else:
				self.disallowpopping = False

		# unlock modes
		if self.score == 20 and self.portal_border == 0 and self.curled_up == 0 and self.apple_bag == 0 and not self.allowmode0 and not self.newmoded:
			self.newmode = True
			self.allowmode0 = True
			self.thenewmode = 'Apple Bag'
		elif self.score == 20 and self.portal_border == 0 and self.curled_up == 0 and self.apple_bag == 1 and not self.allowmode1 and not self.newmoded:
			self.newmode = True
			self.allowmode1 = True
			self.thenewmode = 'Portal Border'
		elif self.score == 20 and self.portal_border == 1 and self.curled_up == 0 and self.apple_bag == 0 and not self.allowmode2 and not self.newmoded:
			self.newmode = True
			self.allowmode2 = True
			self.thenewmode = 'Angry Apple'
		elif self.score == 20 and self.angry_apple == 1 and not self.allowmode3 and not self.newmoded:
			self.newmode = True
			self.allowmode3 = True
			self.thenewmode = 'Ultimate Snake'
		elif self.score == 90 and self.snake_instinct == 1 and not self.allowmode4 and not self.newmoded:
			self.newmode = True
			self.allowmode4 = True
			self.allow_ai_snake = True
			self.allow_speed_up = True
		elif self.score == 3000 and self.portal_border == 1 and self.curled_up == 1 and self.apple_bag == 1 and not self.allowsecretmode and not self.newmoded:
			self.newmode = True
			self.allowsecretmode = True
			

		# if no more apples are left, auto win
		if self.apple_List == []:
			self.playing = False
			self.g_over = True
			self.win = True

	def get_ar(self, width: int, height: int):
		def gcd(a, b): return a if b == 0 else gcd(b, a % b)

		r = gcd(width, height)
		x = int(width / r)
		y = int(height / r)

		return f'{x}:{y}'

	def mode(self, portal_border = 0, curled_up = 0, apple_bag = 0, break_border = 0, snake_instinct = 0, angry_apple = 0):
		# size each cell
		self.cell_size = 20

		# get aspect ratio
		current_ar = self.get_ar(self.current_w, self.current_h)

		widescreen_ar = ['16:9', '16:10', '21:9', '683:384', '85:48']
		#print('Aspect Ratio (float): ' + str(current_ar))
		#print('Widescreen Aspect Ratios (float):\n' + str(widescreen_ar))

		widescreen = False

		for ar in widescreen_ar:
			if current_ar == ar: widescreen = True; break

		#load image
		if widescreen and self.allow_widescreen:
			self.imgLoad = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/loading_16_9.png'), (self.DISPLAY_W, self.DISPLAY_H))
			self.imgMenu = pygame.transform.scale(pygame.image.load(self.temp_path +  'images/' + self.holiday + 'menu_16_9.png'), (self.DISPLAY_W, self.DISPLAY_H))
			self.imgMenuBG = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/' + self.holiday + 'menubg_16_9.png'), (self.DISPLAY_W, self.DISPLAY_H))
		else:
			self.imgLoad = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/loading.png'), (self.DISPLAY_W, self.DISPLAY_H))
			self.imgMenu = pygame.transform.scale(pygame.image.load(self.temp_path +  'images/' + self.holiday + 'menu.png'), (self.DISPLAY_W, self.DISPLAY_H))
			self.imgMenuBG = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/' + self.holiday + 'menubg.png'), (self.DISPLAY_W, self.DISPLAY_H))
		self.imgGWE = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/GWE.png'), (512, 438))
		self.imgSJ = pygame.image.load(self.temp_path + 'images/SJ.png')
		self.imgPG = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/pygame.png'), (512, 144))
		self.imgSJ_rect, self.imgGWE_rect, self.imgPG_rect = self.imgSJ.get_rect(), self.imgGWE.get_rect(), self.imgPG.get_rect()
		self.imgSJ_rect.center, self.imgGWE_rect.center, self.imgPG_rect.center = (self.DISPLAY_W / 2, self.DISPLAY_H / 2), (self.DISPLAY_W / 2, self.DISPLAY_H / 2), (self.DISPLAY_W / 2, self.DISPLAY_H / 2)

		#self.body_default = pygame.transform.scale(pygame.image.load('images/body_default.png'),(self.cell_size,self.cell_size))

		self.imgHead_r = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/head_r.png'),(self.cell_size,self.cell_size))
		self.imgHead_l = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/head_l.png'),(self.cell_size,self.cell_size))
		self.imgHead_u = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/head_u.png'),(self.cell_size,self.cell_size))
		self.imgHead_d = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/head_d.png'),(self.cell_size,self.cell_size))
		self.imgHead_die = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/head_die.png'),(self.cell_size,self.cell_size))
		self.imgHead_win = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/head_win.png'),(self.cell_size,self.cell_size))
		#self.imgTail_r = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/tail_r.png'),(self.cell_size,self.cell_size))
		#self.imgTail_l = pygame.transform.rotate(self.imgTail_r, 180)
		#self.imgTail_u = pygame.transform.rotate(self.imgTail_r, 90)
		#self.imgTail_d = pygame.transform.rotate(self.imgTail_r, 270)

		# Load special images for holidays
		if self.holiday:
			self.imgHead_hat = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/' + self.holiday + 'hat.png'),(self.cell_size + 10, self.cell_size + 5))
			self.imgApple = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/' + self.holiday + 'apple.png'),(self.cell_size / 2, self.cell_size))
		else:
			self.imgApple = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/apple.png'),(self.cell_size - 3, self.cell_size))

		# Load audio
		self.WIIstart = pygame.mixer.Sound(self.temp_path + 'audio/wii.start.mp3')
		
		self.DRsnd_menumove = pygame.mixer.Sound(self.temp_path + 'audio/dr.snd_menumove.wav')
		self.DRsnd_select = pygame.mixer.Sound(self.temp_path + 'audio/dr.snd_select.wav')
		self.DRsnd_cantselect = pygame.mixer.Sound(self.temp_path + 'audio/dr.snd_cantselect.wav')
		self.DRsnd_won = pygame.mixer.Sound(self.temp_path + 'audio/dr.snd_won.wav')

		self.GSmove_u = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.move_up.wav')
		self.GSmove_d = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.move_down.wav')
		self.GSmove_l = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.move_left.wav')
		self.GSmove_r = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.move_right.wav')
		self.GSeatapple = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.eatapple.wav')
		self.GSportal = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.portal.wav')
		self.GSwin = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.win.wav')
		self.GSdie = pygame.mixer.Sound(self.temp_path + 'audio/ggsnake.die.wav')

		self.SMB2down = pygame.mixer.Sound(self.temp_path + 'audio/smb2.down.ogg')
		self.SMB3pause = pygame.mixer.Sound(self.temp_path + 'audio/smb3.pause.wav')

		self.BAcorrect = pygame.mixer.Sound(self.temp_path + 'audio/brainage.correct.wav')

		# PERCENTAGE of the alpha layer
		self.alpha_percentage = 20

		self.delta_type = 1

		# FPS (for limited FPS)
		self.FPS = 100

		self.clock = pygame.time.Clock()

		# color
		self.white = (255,255,255)
		self.ultra_white = (230,240,240)
		self.red = (255,0,0)
		self.red_god = (170, 6, 5)
		self.green = (0, 127, 70)
		self.blue = (0,0,255)
		self.light_blue = (27, 214, 249)
		self.gray = (128,128,128)
		self.yellow = (255,255,0)
		self.super_yellow = (254, 246, 107)
		self.black = (0,0,0)

		# border
		self.border_x = 20
		self.border_y = 60

		# feature
		self.portal_border = portal_border
		self.curled_up = curled_up
		self.apple_bag = apple_bag
		self.break_border = break_border
		self.snake_instinct = snake_instinct
		self.ai_snake = angry_apple
		self.angry_apple = angry_apple

	def new_game(self):
		# snake
		self.snake_head = [100,100]
		self.snake = [[100,100],[80,100],[60,100]]


		# apple
		if self.playing:
			self.apple_List = []
			self.spawn_apple()

		# self.direction
		self.direction = 'RIGHT'

		# score
		self.score = 0

		# speed - lower => faster
		self.speed = 150
		self.turbo = False

		# check if move sound should play and avoid repeated plays
		self.allowmovesound = False

		# ANGRY APPLE: makes snake longer when 1 point is added
		self.disallowpopping = False

		self.paused = False
		self.g_over = False
		self.win = False

	def show_score(self):
		self.draw_text('Score: {0}'.format(self.score), 25, 100, 30, self.gray, self.game_font)
		if self.save_high_score:
			if self.snake_instinct == 1:
				self.draw_text('HIGH SCORE: {0}'.format(self.high_scores['Ultimate Snake']), 15, 100, 10, self.gray, self.game_font)
				if self.score > self.high_scores['Ultimate Snake']: self.draw_text('HIGH SCORE!', 15, 100, 50, self.red, self.game_font)
			elif self.apple_bag == 1:
				self.draw_text('HIGH SCORE: {0}'.format(self.high_scores['Apple Bag']), 15, 100, 10, self.gray, self.game_font)
				if self.score > self.high_scores['Apple Bag']: self.draw_text('HIGH SCORE!', 15, 100, 50, self.red, self.game_font)
			elif self.portal_border == 1:
				self.draw_text('HIGH SCORE: {0}'.format(self.high_scores['Portal Border']), 15, 100, 10, self.gray, self.game_font)
				if self.score > self.high_scores['Portal Border']: self.draw_text('HIGH SCORE!', 15, 100, 50, self.red, self.game_font)
			elif self.angry_apple == 1:
				self.draw_text('HIGH SCORE: {0}'.format(self.high_scores['Angry Apple']), 15, 100, 10, self.gray, self.game_font)
				if self.score > self.high_scores['Angry Apple']: self.draw_text('HIGH SCORE!', 15, 100, 50, self.red, self.game_font)
			else:
				self.draw_text('HIGH SCORE: {0}'.format(self.high_scores['Classic']), 15, 100, 10, self.gray, self.game_font)
				if self.score > self.high_scores['Classic']: self.draw_text('HIGH SCORE!', 15, 100, 50, self.red, self.game_font)

	def show_speed(self):
		# speed percent
		speed_percent = (150 - self.speed) / 150 * 100
		
		if self.angry_apple == 1:
			if self.turbo:
				self.draw_text('Snake Speed: 33.33%', 25, self.DISPLAY_W - 200, 30, self.gray, self.game_font)
				self.draw_text('TEMPORARY!'.format(29 / 30 * 100), 13, self.DISPLAY_W - 200, 50, self.red, self.game_font)
			else:
				if speed_percent >= 100:
					self.draw_text('Snake Speed: 100.00%', 25, self.DISPLAY_W - 200, 30, self.gray, self.game_font)
					self.draw_text('MAX!'.format(29 / 30 * 100), 13, self.DISPLAY_W - 200, 50, self.red, self.game_font)
				else:
					self.draw_text('Snake Speed: {:.2f}%'.format(speed_percent), 25, self.DISPLAY_W - 200, 30, self.gray, self.game_font)
		else:
			if self.turbo:
				self.draw_text('Speed: 100.00%', 25, self.DISPLAY_W - 200, 30, self.gray, self.game_font)
				self.draw_text('TEMPORARY!'.format(29 / 30 * 100), 13, self.DISPLAY_W - 200, 50, self.red, self.game_font)
			else:
				if speed_percent >= 100:
					self.draw_text('Speed: 100.00%', 25, self.DISPLAY_W - 200, 30, self.gray, self.game_font)
					self.draw_text('MAX!'.format(29 / 30 * 100), 13, self.DISPLAY_W - 200, 50, self.red, self.game_font)
				else:
					self.draw_text('Speed: {:.2f}%'.format(speed_percent), 25, self.DISPLAY_W - 200, 30, self.gray, self.game_font)

	def change_volume(self):
			# set volume (MUST SET FOR ALL SOUNDS)
			self.menumus.set_volume(self.musicvol * self.volume)
			self.gamemus.set_volume(self.musicvol * self.volume)

			self.WIIstart.set_volume(self.musicvol * self.volume)

			self.DRsnd_menumove.set_volume(self.soundvol * self.volume)
			self.DRsnd_select.set_volume(self.soundvol * self.volume)
			self.DRsnd_cantselect.set_volume(self.soundvol * self.volume)
			self.DRsnd_won.set_volume(self.soundvol * self.volume)

			self.GSmove_u.set_volume(self.soundvol * self.volume)
			self.GSmove_d.set_volume(self.soundvol * self.volume)
			self.GSmove_l.set_volume(self.soundvol * self.volume)
			self.GSmove_r.set_volume(self.soundvol * self.volume)
			self.GSeatapple.set_volume(self.soundvol * self.volume)
			self.GSportal.set_volume(self.soundvol * self.volume)
			self.GSwin.set_volume(self.soundvol * self.volume)
			self.GSdie.set_volume(self.soundvol * self.volume)

			self.SMB2down.set_volume(self.soundvol * self.volume)
			self.SMB3pause.set_volume(self.soundvol * self.volume)

			self.BAcorrect.set_volume(self.soundvol * self.volume)

	def load_music(self):
		self.menumus = pygame.mixer.Sound(self.temp_path + 'audio/' + self.holiday + 'wii.menu.mp3')
		self.gamemus = pygame.mixer.Sound(self.temp_path + 'audio/' + self.holiday + 'bg_music_1.mp3')

	def print_loading(self, text):
		self.display.fill(self.black)
		self.draw_text('LOADING', self.font_size, self.DISPLAY_W/2, self.DISPLAY_H/2)
		self.draw_text(text, self.font_size / 2, self.DISPLAY_W/2, self.DISPLAY_H/2 + 30, font_name = self.menu2_font)
		self.window.blit(self.display, (0,0))
		pygame.display.update()

	def logo_screen(self):
		logger.log('Loading music')
		self.print_loading('Loading music')
		self.load_music()

		for item in self.items_to_import:
			try:
				if item != 'fullscreen' or item != 'scaled' or 'item' != 'native_res':
					self.print_loading('Loading setting "' + item + '"')
					self.import_settings(item)
					logger.log('Loading setting "' + item + '": success')
			except:
				logger.log('Loading setting "' + item + '": error')
				pass


		self.print_loading('Checking saved settings')
		if self.allowmode4:
			if not self.allow_ai_snake:
				logger.log('Enabling AI Snake mode because De Snake Mode is unlocked and it hasn\'t been unlocked yet.')
				self.allow_ai_snake = True
			if not self.allow_speed_up:
				logger.log('Enabling Turbo mode because De Snake Mode is unlocked and it hasn\'t been unlocked yet.')
				self.allow_speed_up = True
		elif not self.allowmode4:
			if self.allow_ai_snake:
				logger.log('Disabling AI Snake mode because it is unlocked before unlocking De Snake Mode.')
				self.allow_ai_snake = False
			if self.allow_speed_up:
				logger.log('Disabling Turbo mode because it is unlocked before unlocking De Snake Mode.')
				self.allow_speed_up = False

		for score in self.high_scores:
			if self.high_scores[score] < 0:
				logger.log('Invalid ' + score + ' score: ' + str(self.high_scores[score]) + '\nResetting score to 0.')
				self.high_scores[score] = 0

		self.print_loading('Getting splash text')
		self.generate_splash()
		self.print_loading('Adjusting volume')
		self.change_volume()

		self.save_settings()
		
		self.fadeBg = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
		self.fadeBg.set_alpha(255)
		self.fadeBg.fill(self.black)
		self.alpha = 0
		self.display.blit(self.imgLoad, (0,0))
		self.display.blit(self.imgSJ, self.imgSJ_rect)

		while self.alpha < 255:
			pygame.time.delay(25)
			self.alpha += 20
			self.display.set_alpha(self.alpha)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					self.display.set_alpha(255)
					return
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.window.blit(self.fadeBg, (0,0))
			self.window.blit(self.display, (0,0))
			pygame.display.update()
		pygame.time.delay(1000)
		self.alpha = 0
		while self.alpha < 255:
			pygame.time.delay(25)
			self.alpha += 20
			self.fadeBg.set_alpha(self.alpha)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					return
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.window.blit(self.display, (0,0))
			self.window.blit(self.fadeBg, (0,0))
			pygame.display.update()
		self.display.blit(self.imgLoad, (0,0))
		self.display.blit(self.imgGWE, self.imgGWE_rect)
		self.window.blit(self.display, (0,0))
		self.alpha = 0
		while self.alpha < 255:
			pygame.time.delay(25)
			self.alpha += 20
			self.display.set_alpha(self.alpha)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					self.display.set_alpha(255)
					return
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.window.blit(self.fadeBg, (0,0))
			self.window.blit(self.display, (0,0))
			pygame.display.update()
		pygame.time.delay(1000)
		self.alpha = 0
		while self.alpha < 255:
			pygame.time.delay(25)
			self.alpha += 20
			self.fadeBg.set_alpha(self.alpha)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					return
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.window.blit(self.display, (0,0))
			self.window.blit(self.fadeBg, (0,0))
			pygame.display.update()
		self.display.blit(self.imgLoad, (0,0))
		self.display.blit(self.imgPG, self.imgPG_rect)
		self.window.blit(self.display, (0,0))
		self.alpha = 0
		while self.alpha < 255:
			pygame.time.delay(25)
			self.alpha += 20
			self.display.set_alpha(self.alpha)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					self.display.set_alpha(255)
					return
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.window.blit(self.fadeBg, (0,0))
			self.window.blit(self.display, (0,0))
			pygame.display.update()
		pygame.time.delay(1000)
		self.alpha = 0
		while self.alpha < 255:
			pygame.time.delay(25)
			self.alpha += 20
			self.fadeBg.set_alpha(self.alpha)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					return
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.window.blit(self.display, (0,0))
			self.window.blit(self.fadeBg, (0,0))
			pygame.display.update()
		self.display.fill(self.black)
		self.window.blit(self.display, (0,0))
		pygame.display.update()
		
	def save_settings(self):
		# save settings to settings.py
		f = open(self.appdata_path + self.settings_fn, 'w', encoding = 'utf8')
		f.write('# WARNING! This script is AUTO-GENERATED by Sneky.\n# You should NOT modify it in any way!\n\n# Nevermind, you won\'t even listen anyway. Go ahead and do anything you want.\n\n')
		for item in self.items_to_import:
			exec('f.write(\'{0} = {{0}}\\n\'.format(self.{0}))'.format(item))
		f.close()

	def import_settings(self, var, catch = False):
		if catch:
			exec('from settings import ' + var)
			exec('self.{0} = {0}'.format(var))
		else:
			try:
				exec('from settings import ' + var)
				exec('self.{0} = {0}'.format(var))
			except Exception:
				pass
