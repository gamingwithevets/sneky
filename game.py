import pygame
import os
from menu import *
import logger
import random
import time
import sys
from decimal import *
from pygame import mixer
from datetime import datetime

class Game():
	def __init__(self):
		try:
			self.temp_path = os.path.join(sys._MEIPASS) + '/'
		except Exception:
			self.temp_path = ''

		pygame.init()
		pygame.display.set_caption("Sneky")
		# game version
		self.gamestatus = 'release'
		self.gameversion = '1.2.1'

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
		self.allowmode0 = False # apple bag
		self.allowmode1 = False # portal border
		self.allowmode2 = False # ultimate mode
		self.allowmode3 = False # angry apple
		self.allowmode4 = False # de snake mode


		self.running, self.playing, self.inmenu, self.show_instructions, self.newmode, self.newmoded = True, False, True, False, False, False
		self.reset_keys()
		# self.START_KEY, self.BACK_KEY, self.SPACE_KEY, self.CTRL_KEY = False, False, False, False
		# self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False

		# display resolution
		self.DISPLAY_W, self.DISPLAY_H = 800, 600
		self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
		self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
		self.arrow_font = self.temp_path + 'fonts/MinecraftRegular.ttf'
		self.menu2_font = self.temp_path + 'fonts/Minecraftia.ttf'
		self.menu_font = self.temp_path + 'fonts/8_BIT_WONDER.TTF'
		self.game_font = self.temp_path + 'fonts/River Adventurer.ttf'
		self.font_size = 32
		self.BLACK, self.WHITE = (0,0,0), (255,255,255)
		self.holidayname = ''
		self.holiday = ''
		self.check_holidays()
		self.generate_splash()
		self.press_start = PressStart(self)
		self.main_menu = MainMenu(self)
		self.options = OptionsMenu(self)
		self.volumemenu = VolumeMenu(self)
		self.controls = ControlsMenu(self)
		self.credits = CreditsMenu(self)
		self.mode_menu = ModeMenu(self)
		self.curr_menu = self.press_start
		self.volume = 1
		self.musicvol = 1
		self.soundvol = 1
		self.mode()

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
		'The snake can die by touching the border in the angry mode!',
		'May the Queen be with you.',
		'Press {0} for the Queen\'s help :p'.format(pygame.key.name(self.X_BIND).upper()),
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
				'SANTA IS FAKE!',
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
			self.splashes = [
				'Welcome to Sneky!',
				'No holiday today... :(',
				'Happy [Holiday Name Here]',
				'Have a great non-holiday!',
				'I wish today was a holiday.'
				]
		if random.randint(0, 1) == 0 and not self.holidayname:
			self.curr_splash = self.global_splashes[random.randint(0, len(self.splashes) - 1)]
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

	def draw_text(self, text, size, x, y, color = None, font_name = None, screen = None):
		if color == None:
			color = self.WHITE
		if font_name == None:
			font_name = self.menu_font
		if screen == None:
			screen = self.display
		font = pygame.font.Font(font_name, int(size))
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.center = (x,y)
		screen.blit(text_surface, text_rect)


	def game_loop(self):
		self.new_game()
		self.game_over()
		while self.playing:
			self.check_events()
			self.test()
			self.reset_keys()
			if self.g_over:
				self.draw_game_screen()
			
			self.window.blit(self.display, (0,0))

			if self.paused or self.newmode:
				self.game_over()

			pygame.display.update()
		
		self.game_over()

	def init_intros(self):
		self.snake_instinct_intro = 'certain amount of apples. Let\'s use the snake\'s powers to win!'
		self.apple_bag_intro = [
		'Multiple apples are spawning! Will the snake eat them or be hungry?',
		''
		]
		self.portal_border_intro = ''
		self.angry_apple_intro = [
		'You are the apple! You\'re tired of the snake eating all of your mates,',
		'so you try to escape the snake by running out of the playfield!',
		'Escape the snake to get points. You\'ll get faster, but so does the snake.',
		]
		self.classic_intro = [
		'Eat the apple, and don\'t bump into yourself or the border!',
		'Simple.'
		]
		if self.holidayname:
			if self.holidayname == 'christmas':
				self.snake_instinct_intro = 'certain amount of candy cones. Let\'s use the snake\'s powers to win!'
				self.apple_bag_intro = [
				'Santa\'s giving out more candy cones! The snake doesn\'t hesitate',
				'to eat \'em!'
				]
				self.portal_border_intro = 'Time to get some treats from Santa!'
				self.angry_apple_intro = [
				'You are a candy cone! You see that the snake has eaten too much cones',
				'and isn\'t stopping! He\'s gonna get fat at this rate. So you try to',
				'escape the snake! You\'ll get a point and you and the snake will speed up.',
				]
				self.classic_intro = [
				'It\'s Christmas! The snake wants the candy cones! Eat \'em and don\'t',
				'touch yourself or the border, or you\'ll die!'
				]


	def game_over(self):
		
		if self.g_over:
			self.draw_game_screen()

			# fade diplay
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

			# gameover text
			self.gamemus.stop()
			if self.win:
				self.draw_text('YOU WIN!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				if self.ai_snake == 0:
					logger.log('Player ' + self.playername + ' won!')
				else:
					if self.angry_apple == 0:
						logger.log('Oh Yeah Can I Collect Bananas Now')
					else:
						logger.log('You Will Pay For This')
						self.GSdie.play()
				self.GSwin.play()
			else:
				self.draw_text('YOU DIED!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				if self.ai_snake == 0:
					logger.log('Player ' + self.playername + ' died!')
					self.GSdie.play()
				else:
					if self.angry_apple == 0:
						logger.log('Oh Noes Why Did I Die')
						self.GSdie.play()
					else:
						logger.log('Yum Yum')
						self.SMB2down.play()
			self.draw_text('{0}: New Game'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.game_font, screen = self.window)
			self.draw_text('{0}/{1}: Quit'.format(pygame.key.name(self.BACK_BIND).upper(), pygame.key.name(self.MENU_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.game_font, screen = self.window)

			# self.window.blit(self.over_text, self.over_rect)
			pygame.display.update()

			while self.g_over:

				# check input
				self.check_events()
				if self.BACK_KEY or self.MENU_KEY:
					self.g_over = False
				if self.SPACE_KEY:
					self.playing = True
					self.g_over = False
					self.reset_keys()
					logger.log('Player ' + self.playername + ' decided to play again!')
					self.gamemus.play(-1)
					self.game_loop()
				self.reset_keys()

		elif self.paused:
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

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
			self.draw_text('INTRODUCTION', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
			if self.portal_border == 1 and self.curled_up == 1 and self.apple_bag == 1:
				self.draw_text('The Debug Mode of Sneky. Like cheating? This is for you!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text('You can walk through yourself, turn around, and walk through the', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
				self.draw_text('portal borders!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 4, font_name = self.menu2_font, screen = self.window)
			elif self.snake_instinct == 1:
				self.draw_text('The snake switches color and power every time you collect a', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.snake_instinct_intro, self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
			elif self.apple_bag == 1:
				self.draw_text(self.apple_bag_intro[0], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.apple_bag_intro[1], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
			elif self.portal_border == 1:
				self.draw_text('The border turns into a portal to go to the other side of the playfield!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.portal_border_intro, self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
			elif self.angry_apple == 1:
				self.draw_text(self.angry_apple_intro[0], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.angry_apple_intro[1], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.angry_apple_intro[2], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 4, font_name = self.menu2_font, screen = self.window)
				self.draw_text('If the snake dies, you win! But if it eats you, you die!', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 5, font_name = self.menu2_font, screen = self.window)
			else:
				self.draw_text(self.classic_intro[0], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.menu2_font, screen = self.window)
				self.draw_text(self.classic_intro[1], self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.menu2_font, screen = self.window)

			self.draw_text('{0}: Start'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 7, font_name = self.game_font, screen = self.window)
			self.draw_text('{0}/{1}: Quit'.format(pygame.key.name(self.BACK_BIND).upper(), pygame.key.name(self.MENU_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 8, font_name = self.game_font, screen = self.window)

			# self.window.blit(self.over_text, self.over_rect)
			pygame.display.update()

			while self.show_instructions:

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

			# new mode message
			self.draw_text('NEW MODE UNLOCKED!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
			self.draw_text('Do you want to try it out?', self.font_size *1/2, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size, font_name = self.menu2_font, screen = self.window)

			self.draw_text('{0}: Yes, please'.format(pygame.key.name(self.BACK_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 3, font_name = self.game_font, screen = self.window)
			self.draw_text('{0}: No thanks, continue playing'.format(pygame.key.name(self.SPACE_BIND).upper()), self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 4, font_name = self.game_font, screen = self.window)

			pygame.mixer.pause()
			self.DRsnd_won.play()
			# self.window.blit(self.over_text, self.over_rect)
			pygame.display.update()

			self.save_settings()

			while self.newmode:

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
			self.NAPSR.play(-1)

	def draw_game_screen(self):
		# white BG
		self.display.fill(self.WHITE)

		# speed
		if not self.turbo:
			pygame.time.delay(int(self.speed))
			# delay
			#self.show_delay()
		else:
			if self.angry_apple == 0:
				pygame.time.delay(0)
				self.draw_text('TURBO MODE IS ON', 25, self.DISPLAY_W / 2 - 50, 30, self.red, self.game_font)
			else:
				pygame.time.delay(100)
				if self.speed < 100:
					self.draw_text('YOU AND THE SNAKE SLOWED DOWN!', 15, self.DISPLAY_W / 2 - 50, 30, self.red, self.game_font)
				else:
					self.draw_text('YOU AND THE SNAKE SPED UP!', 15, self.DISPLAY_W / 2 - 50, 30, self.red, self.game_font)

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
					self.snakepos0 = self.snake_head[0]
				else:
					self.snakepos0 = snakepos0
				if snakepos1 == None:
					self.snakepos1 = self.snake_head[1]
				else:
					self.snakepos1 = snakepos1

				if self.direction == 'RIGHT':
					self.display.blit(self.imgHead_hat,pygame.Rect(self.snakepos0, self.snakepos1 - self.cell_size, self.cell_size, self.cell_size))
				if self.direction == 'LEFT':
					self.display.blit(self.imgHead_hat,pygame.Rect(self.snakepos0, self.snakepos1 - self.cell_size, self.cell_size, self.cell_size))
				if self.direction == 'UP':
					self.display.blit(self.imgHead_hat,pygame.Rect(self.snakepos0, self.snakepos1 - (self.cell_size + 3), self.cell_size, self.cell_size))
				if self.direction == 'DOWN':
					self.display.blit(self.imgHead_hat,pygame.Rect(self.snakepos0, self.snakepos1 - (self.cell_size + 3), self.cell_size, self.cell_size))

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

		# if self.UP_KEY:
		# 	self.apple_List[0][1] -= self.cell_size
		# elif self.DOWN_KEY:
		# 	self.apple_List[0][1] += self.cell_size
		# elif self.RIGHT_KEY:
		# 	self.apple_List[0][0] += self.cell_size
		# elif self.LEFT_KEY:
		# 	self.apple_List[0][0] -= self.cell_size

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
			while True:
				# generate 1 apple
				apple_x = random.randrange(self.border_x,self.DISPLAY_W-self.border_x,20)
				apple_y = random.randrange(self.border_y,self.DISPLAY_H-self.border_y,20)
				self.apple = [apple_x, apple_y]
				if self.apple not in self.snake:
					self.apple_List.insert(-1,self.apple)
					break

	def test(self):

		self.turbo = False
		# check function input
		if self.BACK_KEY:
			self.paused = True
		elif self.MENU_KEY:
			self.playing = False


		key_pressed = pygame.key.get_pressed()
		if key_pressed[self.X_BIND]:
			if self.angry_apple == 0:
				if self.ai_snake:
					logger.log('OK I Will Let You Play Now')
				else:
					logger.log('It Seems Like AI Snake Is On So I Will Play For You')
				self.ai_snake = not self.ai_snake
			else:
				logger.log('Oh Sorry I Am Controlling The Snake Now Haha')


		if key_pressed[self.CTRL_BIND]:
			self.turbo = True

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
			if (self.snake_head[0] >= Game().DISPLAY_W - 20
			or self.snake_head[0] <= self.border_x - 10
			or self.snake_head[1] >= Game().DISPLAY_H - 20
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
		if self.score == 20 and self.portal_border == 0 and self.curled_up == 0 and self.apple_bag == 1 and not self.allowmode1 and not self.newmoded:
			self.newmode = True
			self.allowmode1 = True
		if self.score == 20 and self.portal_border == 1 and self.curled_up == 0 and self.apple_bag == 0 and not self.allowmode2 and not self.newmoded:
			self.newmode = True
			self.allowmode2 = True
		if self.score == 20 and self.snake_instinct == 1 and not self.allowmode3 and not self.newmoded:
			self.newmode = True
			self.allowmode3 = True
		if self.score == 20 and self.angry_apple == 1 and not self.allowmode4 and not self.newmoded:
			self.newmode = True
			self.allowmode4 = True

		# if no more apples are left, auto win
		if self.apple_List == []:
			self.playing = False
			self.g_over = True
			self.win = True

	def mode(self, portal_border = 0, curled_up = 0, apple_bag = 0, break_border = 0, snake_instinct = 0, angry_apple = 0):
		# size each cell
		self.cell_size = 20

		#load image
		self.imgLoad = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/loading.png'), (self.DISPLAY_W, self.DISPLAY_H))
		self.imgGWE = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/GWE.png'), (512, 438))
		self.imgSJ = pygame.image.load(self.temp_path + 'images/SJ.png')
		self.imgPG = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/pygame.png'), (512, 144))
		self.imgSJ_rect, self.imgGWE_rect, self.imgPG_rect = self.imgSJ.get_rect(), self.imgGWE.get_rect(), self.imgPG.get_rect()
		self.imgSJ_rect.center, self.imgGWE_rect.center, self.imgPG_rect.center = (self.DISPLAY_W / 2, self.DISPLAY_H / 2), (self.DISPLAY_W / 2, self.DISPLAY_H / 2), (self.DISPLAY_W / 2, self.DISPLAY_H / 2)
		self.imgMenu = pygame.transform.scale(pygame.image.load(self.temp_path +  'images/' + self.holiday + 'menu.png'), (self.DISPLAY_W, self.DISPLAY_H))
		self.imgMenuBG = pygame.transform.scale(pygame.image.load(self.temp_path + 'images/' + self.holiday + 'menubg.png'), (self.DISPLAY_W, self.DISPLAY_H))

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

		# 0: unhook snake speed from framerate
		# 1: tie snake speed to framerate (uses a set FPS)
		self.delta_type = 0

		# FPS for delta type 1
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
		self.apple = [300,300]

		# list apple
		#if self.apple_bag == 1:
		self.apple_List = []
		self.apple_List.insert(-1,self.apple)

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

	def game_over_old(self):
		self.over_font = pygame.font.Font("fonts/8_BIT_WONDER.otf", 30)
		self.over_text = self.over_font.render("Game over! Press Space to replay - Press Escape to exit", True, self.white)
		self.over_rect = self.over_text.get_rect()
		self.over_rect.midtop = (Game().DISPLAY_W//2 , Game().DISPLAY_H//2)

		self.display2 = pygame.Surface((Game().DISPLAY_W - self.border_x - 20, Game().DISPLAY_H - self.border_y - 20))
		self.display2.set_alpha(int(255 / 100 * self.alpha_percentage))
		self.display2.fill(self.black)
		self.display.blit(self.display2, (self.border_x, self.border_y))
		self.display.blit(self.over_text, self.over_rect)
		pygame.display.flip()

		while True:
			pygame.event.get()
			key_pressed = pygame.key.get_pressed()
			if key_pressed[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()
			elif key_pressed[pygame.K_SPACE]:
				self.game_loop()

	def show_score(self):
		self.draw_text('Score: {0}'.format(self.score), 25, 100, 30, self.gray, self.game_font)

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

	def show_delay(self):
		# speed percent
		delay = self.speed
		self.draw_text('Delay: {:.2f}'.format(delay), 25, self.DISPLAY_W / 2 - 50, 30, self.gray, self.game_font)

	def run(self):
		#mode_playing = True
		#while mode_playing:
		# background
		self.display.fill(self.white)
		for x in range(self.border_x, self.DISPLAY_W - 20, 40):
			for y in range(self.border_y, self.DISPLAY_H - 20, 40):
				pygame.draw.rect(self.display,(170, 215, 81),(x,y,self.cell_size,self.cell_size))
				pygame.draw.rect(self.display,(162, 209, 72),(x + 20,y,self.cell_size,self.cell_size))
			for y in range(self.border_y + 20, self.DISPLAY_H - 20, 40):
				pygame.draw.rect(self.display,(170, 215, 81),(x + 20,y,self.cell_size,self.cell_size))
				pygame.draw.rect(self.display,(162, 209, 72),(x,y,self.cell_size,self.cell_size))

		# speed
		if self.delta_type == 0:
			pygame.time.delay(int(self.speed))
		else:
			self.clock.tick(self.FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_UP]:
			self.direction = 'UP'
		if key_pressed[pygame.K_DOWN]:
			self.direction = 'DOWN'
		if key_pressed[pygame.K_RIGHT]:
			self.direction = 'RIGHT'
		if key_pressed[pygame.K_LEFT]:
			self.direction = 'LEFT'
		if key_pressed[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()

		if self.direction == 'RIGHT':
			self.snake_head[0] += self.cell_size
		if self.direction == 'LEFT':
			self.snake_head[0] -= self.cell_size
		if self.direction == 'UP':
			self.snake_head[1] -= self.cell_size
		if self.direction == 'DOWN':
			self.snake_head[1] += self.cell_size


		# snake moving
		self.snake.insert(0, list(self.snake_head))

		if self.apple_bag == 0:
			if self.snake_head == self.apple:
				self.score += 1

				if int(self.speed) > 0:
					self.speed *= 0.97
				else:
					self.speed -= 0.5
				while True:
					apple_x = random.randrange(self.border_x,Game().DISPLAY_W-self.border_x,20)
					apple_y = random.randrange(self.border_y,Game().DISPLAY_H-self.border_y,20)
					self.apple = [apple_x, apple_y]
					if self.apple not in self.snake:
						break
				# draw apple color
			else:
				self.snake.pop()

		else:
			if self.snake_head in self.apple_List:
				self.apple_List.remove(self.snake_head)
				# plus score
				self.score += 1
				# move faster
				if int(self.speed) > 0:
					self.speed *= 0.97
				else:
					self.speed -= 0.5
				for i in range(self.score):
					apple_x = random.randrange(self.border_x,Game().DISPLAY_W-20,20)
					apple_y = random.randrange(self.border_y,Game().DISPLAY_H-20,20)
					apple = [apple_x, apple_y]
					if apple not in self.apple_List and apple not in self.snake:
						self.apple_List.insert(-1,apple)
			else:
				self.snake.pop()

		# draw snake color
		for s in self.snake:
			pygame.draw.rect(self.display,self.green,(s[0],s[1],self.cell_size,self.cell_size))
		# draw snake head
		if self.direction == 'RIGHT':
			self.display.blit(self.imgHead_r,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
		if self.direction == 'LEFT':
			self.display.blit(self.imgHead_l,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
		if self.direction == 'UP':
			self.display.blit(self.imgHead_u,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
		if self.direction == 'DOWN':
			self.display.blit(self.imgHead_d,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))

		# draw apple
		if self.apple_bag == 0:
			pygame.draw.rect(self.display, self.red, (self.apple[0], self.apple[1], self.cell_size, self.cell_size))
		else:
			for a in self.apple_List:
				pygame.draw.rect(self.display, self.red, (a[0], a[1], self.cell_size, self.cell_size))


		#border
		pygame.draw.rect(self.display,self.gray,(self.border_x,self.border_y,Game().DISPLAY_W - self.border_x - 20,Game().DISPLAY_H - self.border_y - 20),10)


		#score
		self.show_score()

		# delay
		self.show_delay()

		# hit border
		if (self.snake_head[0] >= Game().DISPLAY_W - 20
		or self.snake_head[0] <= self.border_x - 10
		or self.snake_head[1] >= Game().DISPLAY_H - 20
		or self.snake_head[1] <= self.border_y - 10):
			if self.curled_up == 1:
				self.display.blit(self.imgHead_die,pygame.Rect(self.snake_head[0],self.snake_head[1],self.cell_size,self.cell_size))
				self.playing = False
				self.g_over = True
				#self.game_over()
			else:

				#score = score + (len(snake))

				if self.snake_head[0] <= self.border_x - 15:
					self.snake_head[0] = Game().DISPLAY_W - 2 * self.cell_size
				elif self.snake_head[0] >= Game().DISPLAY_W - self.cell_size:
					self.snake_head [0] = self.border_x
				elif self.snake_head[1] >= Game().DISPLAY_H - self.cell_size:
					self.snake_head[1] = self.border_y
				elif self.snake_head[1] <= self.border_y - 15:
					self.snake_head[1] = Game().DISPLAY_H - 2 * self.cell_size


			#update
			pygame.display.flip()

	def change_volume(self):
			# set volume (MUST SET FOR ALL SOUNDS)
			self.NAPSR.set_volume(self.musicvol * self.volume)
			self.gamemus.set_volume(self.musicvol * self.volume)

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
		self.NAPSR = pygame.mixer.Sound(self.temp_path + 'audio/' + self.holiday + 'napsr.mp3')
		self.gamemus = pygame.mixer.Sound(self.temp_path + 'audio/' + self.holiday + 'bg_music_1.mp3')

	def logo_screen(self):
		#self.draw_text('Loading...', self.font_size, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.menu2_font)
		#self.window.blit(self.display, (0,0))
		#pygame.display.update()
		
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
		f = open(os.getenv('LOCALAPPDATA') + '\\Sneky\\settings.py', 'w', encoding = 'utf8')
		f.write('# WARNING! This script is auto-generated by Sneky.\n# You should NOT modify it in any way!\n\n')
		f.write('# master volume\nvolume = {0}\n\n'.format(self.volume))
		f.write('# music volume\nmusicvol = {0}\n\n'.format(self.musicvol))
		f.write('# sound volume\nsoundvol = {0}\n\n'.format(self.soundvol))
		f.write('# key binds\nCTRL_BIND = {0}\n'.format(self.CTRL_BIND))
		f.write('START_BIND = {0}\n'.format(self.START_BIND))
		f.write('BACK_BIND = {0}\n'.format(self.BACK_BIND))
		f.write('MENU_BIND = {0}\n'.format(self.MENU_BIND))
		f.write('SPACE_BIND = {0}\n'.format(self.SPACE_BIND))
		f.write('UP_BIND = {0}\n'.format(self.UP_BIND))
		f.write('DOWN_BIND = {0}\n'.format(self.DOWN_BIND))
		f.write('LEFT_BIND = {0}\n'.format(self.LEFT_BIND))
		f.write('RIGHT_BIND = {0}\n'.format(self.RIGHT_BIND))
		f.write('X_BIND = {0}\n\n'.format(self.X_BIND))
		f.write('# allows modes to be playable or not\nallowmode0 = {0}\n'.format(self.allowmode0))
		f.write('allowmode1 = {0}\n'.format(self.allowmode1))
		f.write('allowmode2 = {0}\n'.format(self.allowmode2))
		f.write('allowmode3 = {0}\n'.format(self.allowmode3))
		f.write('allowmode4 = {0}\n'.format(self.allowmode4))
		f.close()

if __name__ == '__main__':
	print('Please run main.py to start the game!')