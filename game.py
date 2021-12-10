import pygame
import os
from menu import *
import logger
import random
import time
import sys
from decimal import *
from pygame import mixer

class Game():
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Sneky")
		# game version
		self.gamestatus = 'beta'
		self.gameversion = '1.0.4'

		self.running, self.playing, self.inmenu = True, False, True
		self.reset_keys()
		self.CTRL_KEY = False
		# self.START_KEY, self.BACK_KEY, self.SPACE_KEY, self.CTRL_KEY = False, False, False, False
		# self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False
		self.DISPLAY_W, self.DISPLAY_H = 800, 600
		self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
		self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
		self.arrow_font = 'fonts/MinecraftRegular.ttf'
		self.menu2_font = 'fonts/Minecraftia.ttf'
		self.menu_font = 'fonts/8_BIT_WONDER.ttf'
		self.game_font = 'fonts/River Adventurer.TTF'
		self.font_size = 32
		self.BLACK, self.WHITE = (0,0,0), (255,255,255)
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
				if event.key == pygame.K_RETURN:
					self.START_KEY = True
				if event.key == pygame.K_ESCAPE:
					self.BACK_KEY = True
				if event.key == pygame.K_BACKSPACE:
					self.MENU_KEY = True
				if event.key == pygame.K_SPACE:
					self.SPACE_KEY = True
				if event.key == pygame.K_LCTRL:
					self.CTRL_KEY = not self.CTRL_KEY

				if event.key == pygame.K_UP:
					self.UP_KEY = True
				if event.key == pygame.K_DOWN:
					self.DOWN_KEY = True
				if event.key == pygame.K_LEFT:
					self.LEFT_KEY = True
				if event.key == pygame.K_RIGHT:
					self.RIGHT_KEY = True

	def reset_keys(self):
		self.START_KEY, self.BACK_KEY, self.MENU_KEY, self.SPACE_KEY = False, False, False, False
		self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False
		
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
		while self.playing:
			self.check_events()
			self.test()
			self.reset_keys()
			if self.g_over and self.angry_apple:
				self.draw_game_screen()
			self.window.blit(self.display, (0,0))
			pygame.display.update()

			if self.paused:
				self.game_over()

		self.game_over()

	def game_over(self):
		
		if self.g_over:
			# fade diplay
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

			# gameover text
			if self.win:
				self.draw_text('YOU WIN!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				if self.ai_snake == 0:
					logger.log('Player ' + os.getenv('USERNAME') + ' has won!')
				else:
					if self.angry_apple == 0:
						logger.log('Oh Yeah Can I Collect Bananas Now')
					else:
						logger.log('You Will Pay For This')
				self.GSwin.play()
			else:
				self.draw_text('Game Over!', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
				if self.ai_snake == 0:
					logger.log('Player ' + os.getenv('USERNAME') + ' has died!')
					self.GSdie.play()
				else:
					if self.angry_apple == 0:
						logger.log('Oh Noes Why Did I Die')
						self.GSdie.play()
					else:
						logger.log('Yum Yum')
						self.SMB2down.play()
			self.draw_text('SPACE: New Game', self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.game_font, screen = self.window)
			self.draw_text('ESCAPE/BACKSPACE: Quit', self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.game_font, screen = self.window)

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
					logger.log('Player ' + os.getenv('USERNAME') + ' decides to play again!')
					self.game_loop()
				self.reset_keys()

		elif self.paused:
			self.fadeBg = pygame.Surface((self.DISPLAY_W - self.border_x - 20, self.DISPLAY_H - self.border_y - 20))
			self.fadeBg.set_alpha(int(255 / 100 * self.alpha_percentage))
			self.fadeBg.fill(self.black)
			self.window.blit(self.fadeBg, (self.border_x, self.border_y))

			# gameover text
			self.draw_text('GAME PAUSED', self.font_size * 2, self.DISPLAY_W/2, self.DISPLAY_H/2, font_name = self.game_font, screen = self.window)
			logger.log('Player ' + os.getenv('USERNAME') + ' paused the game!')
			self.draw_text('ESC: Resume Game', self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2 + self.font_size * 2, font_name = self.game_font, screen = self.window)
			self.draw_text('BACKSPACE: Quit', self.font_size *2/3, self.DISPLAY_W/2, self.DISPLAY_H/2  + self.font_size * 3, font_name = self.game_font, screen = self.window)

				# self.window.blit(self.over_text, self.over_rect)
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
					logger.log('Player ' + os.getenv('USERNAME') + ' unpaused the game!')
					return

		if not self.inmenu:
			logger.log('Player ' + os.getenv('USERNAME') + ' has quitted!')
			self.inmenu = True

	def draw_game_screen(self):
		# speed
		if not self.turbo:
			pygame.time.delay(int(self.speed))
			# delay
			#self.show_delay()
		else:
			if self.angry_apple == 0:
				pygame.time.delay(5)
				self.draw_text('TURBO MODE IS ON', 25, 350, 30, self.red, self.game_font)
			else:
				pygame.time.delay(150)
				self.draw_text('THE SNAKE SLOWED DOWN!', 15, 350, 30, self.red, self.game_font)

		#score
		self.show_score()

		# speed
		self.show_speed()

		# apple pos
		#self.draw_text('Apple: {0}, {1}'.format(self.apple[0], self.apple[1]), 25, 100, 30, self.gray, self.game_font)

		# snake pos
		#self.draw_text('Snake: {0}, {1}'.format(self.snake_head[0], self.snake_head[1]), 25, 350, 30, self.gray, self.game_font)

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

		#border
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
			if self.angry_apple == 0:
				self.display.blit(self.imgHead_die,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
			elif self.angry_apple == 1 or self.win:
				self.display.blit(self.imgHead_win,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
		else:
			if self.direction == 'RIGHT':
				self.display.blit(self.imgHead_r,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
			if self.direction == 'LEFT':
				self.display.blit(self.imgHead_l,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
			if self.direction == 'UP':
				self.display.blit(self.imgHead_u,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))
			if self.direction == 'DOWN':
				self.display.blit(self.imgHead_d,pygame.Rect(self.snake_head[0], self.snake_head[1], self.cell_size, self.cell_size))


	def test(self):
		# white BG
		self.display.fill(self.white)

		self.turbo = False
		# check function input
		if self.BACK_KEY:
			self.paused = True
		elif self.MENU_KEY:
			self.playing = False

		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_x]:
			if self.angry_apple == 0:
				if self.ai_snake:
					logger.log('OK I Will Let You Play Now')
				else:
					logger.log('It Seems Like AI Snake Is On So I Will Play For You')
				self.ai_snake = not self.ai_snake
			else:
				logger.log('Oh Sorry I Am Controlling The Snake Now Haha')
		if key_pressed[pygame.K_LCTRL]:
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
					self.draw_game_screen()
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
			if self.UP_KEY:
				self.apple_List[0][1] -= self.cell_size
			elif self.DOWN_KEY:
				self.apple_List[0][1] += self.cell_size
			elif self.RIGHT_KEY:
				self.apple_List[0][0] += self.cell_size
			elif self.LEFT_KEY:
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
				while True:
					# generate 1 apple
					apple_x = random.randrange(self.border_x,self.DISPLAY_W-self.border_x,20)
					apple_y = random.randrange(self.border_y,self.DISPLAY_H-self.border_y,20)
					self.apple = [apple_x, apple_y]
					if self.apple not in self.snake:
						self.apple_List.insert(-1,self.apple)
						break

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
				self.snake.pop()
			else:
				self.disallowpopping = False

		# if no more apples are left, auto win
		if self.apple_List == []:
			self.playing = False
			self.g_over = True
			self.win = True
			self.draw_game_screen()

	def mode(self, portal_border = 0, curled_up = 0, apple_bag = 0, break_border = 0, snake_instinct = 0, angry_apple = 0):
		# size each cell
		self.cell_size = 20

		#load image
		self.imgLoad = pygame.transform.scale(pygame.image.load('images/loading.png'), (self.DISPLAY_W, self.DISPLAY_H))
		self.imgMenu = pygame.transform.scale(pygame.image.load('images/menu.png'), (self.DISPLAY_W, self.DISPLAY_H))

		self.body_default = pygame.transform.scale(pygame.image.load('images/body_default.png'),(self.cell_size,self.cell_size))

		self.imgHead_r = pygame.transform.scale(pygame.image.load('images/head_r.png'),(self.cell_size,self.cell_size))
		self.imgHead_l = pygame.transform.scale(pygame.image.load('images/head_l.png'),(self.cell_size,self.cell_size))
		self.imgHead_u = pygame.transform.scale(pygame.image.load('images/head_u.png'),(self.cell_size,self.cell_size))
		self.imgHead_d = pygame.transform.scale(pygame.image.load('images/head_d.png'),(self.cell_size,self.cell_size))
		self.imgHead_die = pygame.transform.scale(pygame.image.load('images/head_die.png'),(self.cell_size,self.cell_size))
		self.imgHead_win = pygame.transform.scale(pygame.image.load('images/head_win.png'),(self.cell_size,self.cell_size))
		self.imgTail_r = pygame.transform.scale(pygame.image.load('images/tail_r.png'),(self.cell_size,self.cell_size))
		self.imgTail_l = pygame.transform.rotate(self.imgTail_r, 180)
		self.imgTail_u = pygame.transform.rotate(self.imgTail_r, 90)
		self.imgTail_d = pygame.transform.rotate(self.imgTail_r, 270)

		self.imgApple = pygame.transform.scale(pygame.image.load('images/apple.png'),(self.cell_size,self.cell_size))

		# Load audio
		self.DRsnd_menumove = pygame.mixer.Sound('audio/dr.snd_menumove.wav')
		self.DRsnd_select = pygame.mixer.Sound('audio/dr.snd_select.wav')
		self.DRsnd_cantselect = pygame.mixer.Sound('audio/dr.snd_cantselect.wav')

		self.GSmove_u = pygame.mixer.Sound('audio/ggsnake.move_up.wav')
		self.GSmove_d = pygame.mixer.Sound('audio/ggsnake.move_down.wav')
		self.GSmove_l = pygame.mixer.Sound('audio/ggsnake.move_left.wav')
		self.GSmove_r = pygame.mixer.Sound('audio/ggsnake.move_right.wav')
		self.GSeatapple = pygame.mixer.Sound('audio/ggsnake.eatapple.wav')
		self.GSportal = pygame.mixer.Sound('audio/ggsnake.portal.wav')
		self.GSwin = pygame.mixer.Sound('audio/ggsnake.win.wav')
		self.GSdie = pygame.mixer.Sound('audio/ggsnake.die.wav')

		self.SMB2down = pygame.mixer.Sound('audio/smb2.down.ogg')

		self.BAcorrect = pygame.mixer.Sound('audio/brainage.correct.wav')

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
				self.draw_text('Snake Speed: 0.00%', 25, 600, 30, self.gray, self.game_font)
				self.draw_text('TEMPORARY!'.format(29 / 30 * 100), 13, 600, 50, self.red, self.game_font)
			else:
				if speed_percent >= 100:
					self.draw_text('Snake Speed: 100.00%', 25, 600, 30, self.gray, self.game_font)
					self.draw_text('MAX!'.format(29 / 30 * 100), 13, 600, 50, self.red, self.game_font)
				else:
					self.draw_text('Snake Speed: {:.2f}%'.format(speed_percent), 25, 600, 30, self.gray, self.game_font)
		else:
			if self.turbo:
				self.draw_text('Speed: {:.2f}%'.format(29 / 30 * 100), 25, 600, 30, self.gray, self.game_font)
				self.draw_text('TEMPORARY!'.format(29 / 30 * 100), 13, 600, 50, self.red, self.game_font)
			else:
				if speed_percent >= 100:
					self.draw_text('Speed: 100.00%', 25, 600, 30, self.gray, self.game_font)
					self.draw_text('MAX!'.format(29 / 30 * 100), 13, 600, 50, self.red, self.game_font)
				else:
					self.draw_text('Speed: {:.2f}%'.format(speed_percent), 25, 600, 30, self.gray, self.game_font)

	def show_delay(self):
		# speed percent
		delay = self.speed
		self.draw_text('Delay: {:.2f}'.format(delay), 25, 350, 30, self.gray, self.game_font)

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

			self.DRsnd_menumove.set_volume(self.soundvol * self.volume)
			self.DRsnd_select.set_volume(self.soundvol * self.volume)
			self.DRsnd_cantselect.set_volume(self.soundvol * self.volume)

			self.GSmove_u.set_volume(self.soundvol * self.volume)
			self.GSmove_d.set_volume(self.soundvol * self.volume)
			self.GSmove_l.set_volume(self.soundvol * self.volume)
			self.GSmove_r.set_volume(self.soundvol * self.volume)
			self.GSeatapple.set_volume(self.soundvol * self.volume)
			self.GSportal.set_volume(self.soundvol * self.volume)
			self.GSwin.set_volume(self.soundvol * self.volume)
			self.GSdie.set_volume(self.soundvol * self.volume)

			self.SMB2down.set_volume(self.soundvol * self.volume)

			self.BAcorrect.set_volume(self.soundvol * self.volume)

	def load_music(self):
		self.display.blit(self.imgLoad, (0, 0))
		self.window.blit(self.display, (0,0))
		pygame.display.update()
		self.NAPSR = pygame.mixer.Sound('audio/napsr.mp3')

		pygame.time.delay(2000)
		self.display.fill(self.BLACK)
		self.window.blit(self.display, (0,0))
		pygame.display.update()
		pygame.time.delay(100)

if __name__ == '__main__':
	print('Please run main.py to start the game!')