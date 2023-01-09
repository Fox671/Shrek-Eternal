from settings import *
from raycasting import display
from player import Player
from enemy import Enemy
import numpy
import pygame

# game init
pygame.init()
pygame.display.set_caption("Doom")
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode(RES, pygame.FULLSCREEN, vsync=True)
clock = pygame.time.Clock()

enemies = numpy.array([Enemy() for _ in range(ENEMIES)])
player = Player()

wall_textures = numpy.array([
	pygame.surfarray.array3d(pygame.image.load("assets/floor.png").convert()) / 255,
	pygame.surfarray.array3d(pygame.image.load("assets/wall.png").convert()) / 255,
	pygame.surfarray.array3d(pygame.image.load("assets/ceiling.png").convert()) / 255,
])

enemy_textures = numpy.array([
	pygame.image.load("assets/shrek1.png").convert_alpha(),
	pygame.image.load("assets/shrek2.png").convert_alpha(),
	pygame.image.load("assets/shrek3.png").convert_alpha()
])

try:
	sound = pygame.mixer.Sound("assets/allstar.mp3")
	sound.play(loops = True)
except pygame.error:
	pass

# game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	fps = clock.get_fps()
	if fps != 0:
		player.update(screen, fps)
		[enemy.update(fps) for enemy in enemies]
		
		screen.fill((0, 0, 0))
		enemies = display(player, enemies, wall_textures, enemy_textures, map, screen)

	pygame.display.update()
	clock.tick(FPS)