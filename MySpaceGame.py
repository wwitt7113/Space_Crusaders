import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('graphics/ship_1.png').convert_alpha()
		self.rect = self.image.get_rect(center = (640, 360))

	def player_input(self):
		keys = pygame.key.get_pressed()

		# Movement controls (WASD)
		if keys[pygame.K_w] and self.rect.top > 0:
			self.rect.y -= 8
		if keys[pygame.K_a] and self.rect.left > 0:
			self.rect.x -= 8
		if keys[pygame.K_s] and self.rect.bottom < 720:
			self.rect.y += 8
		if keys[pygame.K_d] and self.rect.right < 1280:
			self.rect.x += 8

	def update(self):
		self.player_input()

class Alien(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('graphics/mine_1.png').convert_alpha()
		self.rect = self.image.get_rect(center = (randint(16, 1264), -100))

	def update(self):
		self.rect.y += 4
		self.destroy()

	def destroy(self):
		if self.rect.y >= 800:
			self.kill()

class Projectile(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('graphics/projectile_1.png').convert_alpha()
		self.image = pygame.transform.rotozoom(self.image, 0, 4)
		#self.start_pos = pos
		self.rect = self.image.get_rect(center = pos)

	def update(self):
		self.rect.y -= 32
		self.destroy()

	def destroy(self):
		if self.rect.y < 0:
			self.kill()

def collision_player():
	if pygame.sprite.spritecollide(player.sprite, aliens, False):
		aliens.empty()
		return False
	else: return True

def collision_aliens(score):
	#pygame.sprite.groupcollide(aliens, projectiles, True, True, collided = None) -> Sprite_Dict
	collided_aliens = pygame.sprite.groupcollide(aliens, projectiles, False, False)
	for target, hits in collided_aliens.items():
		for hit in hits:
			score += 1
			target.kill()
	#pygame.sprite.groupcollide(aliens, projectiles, True, True, pygame.sprite.collide_mask)
	return score 
	
# Initialization
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Space Crusaders')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
aliens = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Background
bg = pygame.image.load('graphics/space_2.png').convert_alpha()
bg = pygame.transform.rotozoom(bg, 0, 4)

# Main Screen
player_ship = pygame.image.load('graphics/ship_1.png')
player_ship = pygame.transform.rotozoom(player_ship, 0, 2)
player_ship_rect = player_ship.get_rect(center = (640, 360))

game_name = font.render('Space Crusaders', False, 'White')
game_name_rect = game_name.get_rect(center = (640, 180))

game_message = font.render('Press space to start', False, 'White')
game_message_rect = game_message.get_rect(center = (640, 520))

# Timer 
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1000)

# Game Loop
while True:
	# Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if game_active:
			# event triggers
			if event.type == spawn_timer:
				aliens.add(Alien())
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					projectiles.add(Projectile(player.sprite.rect.center))

		else: 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
						game_active = True
						start_time = int(pygame.time.get_ticks()/1000)
						score = 0
	
	if game_active:
		# Background
		screen.blit(bg, (0,0))

		# Player
		player.draw(screen)
		player.update()

		# Aliens
		aliens.draw(screen)
		aliens.update()

		# Projectiles
		projectiles.draw(screen)
		projectiles.update()

		# Collisions
		game_active = collision_player()
		score = collision_aliens(score)

	else:
		screen.fill('Black')
		screen.blit(player_ship, player_ship_rect)

		score_message = font.render(f'Final score: {score}', False, 'White')
		score_message_rect = score_message.get_rect(center = (640, 520))
		screen.blit(game_name,game_name_rect)

		if score == 0:
			screen.blit(game_message,game_message_rect)
		else:
			screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)