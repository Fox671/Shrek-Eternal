from numba import njit
from settings import *
from player import Player
from enemy import Enemy
import pygame
import numpy

@njit
def _display(player_x: float, player_y: float, player_angle: float, textures: numpy.ndarray, map: numpy.ndarray, frame: numpy.ndarray) -> numpy.ndarray:
	for vert_ray in range(VERT_NUM_RAYS):
		angle = player_angle + numpy.deg2rad(vert_ray / FOV - 30)

		sin = numpy.sin(angle)
		cos = numpy.cos(angle)
		fov_cos = numpy.cos(numpy.deg2rad(vert_ray / FOV - 30))

		x, y = player_x, player_y
		while not map[int(x)][int(y)]:
			x, y = x + cos * 0.02, y + sin * 0.02

		n = abs((x - player_x) / cos)
		height = int(HOR_NUM_RAYS / (fov_cos * n + 0.0001))

		xx = int(x * 2 % 1 * (TEXTURE_RES - 1))
		if x % 1 < 0.02 or x % 1 > 0.98:
			xx = int(y * 2 % 1 * (TEXTURE_RES - 1))
		yy = numpy.linspace(0, (TEXTURE_RES - 1) * 2, height * 2) % (TEXTURE_RES - 1)

		shade = 0.3 + (height / HOR_NUM_RAYS) * 0.7
		if shade > 1: shade = 1

		for k in range(height * 2):
			if HOR_NUM_RAYS - height + k >= 0 and HOR_NUM_RAYS - height + k < HOR_NUM_RAYS * 2:
				frame[vert_ray][HOR_NUM_RAYS - height + k] = shade * textures[1][xx][int(yy[k])]

		for hor_ray in range(HOR_NUM_RAYS - height):
			n = (HOR_NUM_RAYS / (HOR_NUM_RAYS - hor_ray)) / fov_cos
			x, y = player_x + cos * n, player_y + sin * n
			xx, yy = int(x * 2 % 1 * (TEXTURE_RES - 1)), int(y * 2 % 1 * (TEXTURE_RES - 1))
			shade = 0.2 + 0.8 * (1 - hor_ray / HOR_NUM_RAYS)

			frame[vert_ray][HOR_NUM_RAYS * 2 - hor_ray - 1] = shade * textures[0][xx][yy]
			frame[vert_ray][hor_ray] = shade * textures[2][xx][yy]

	return frame

def display(player: Player, enemies: list[Enemy], wall_textures: numpy.ndarray, enemy_textures: numpy.ndarray, map: numpy.ndarray, screen: pygame.Surface) -> numpy.ndarray:
	frame = numpy.empty((VERT_NUM_RAYS, HOR_NUM_RAYS * 2, 3))
	frame = _display(player.x, player.y, player.angle, wall_textures, map, frame)

	surface = pygame.surfarray.make_surface(frame * 255)
	surface = pygame.transform.scale(surface, RES)

	screen.blit(surface, (0, 0))

	for enemy in enemies:
		enemy_angle = numpy.arctan((enemy.y - player.y) / (enemy.x - player.x))
		if abs(player.x + numpy.cos(enemy_angle) - enemy.x) > abs(player.x - enemy.x):
			enemy_angle = (enemy_angle - numpy.pi) % (numpy.pi * 2)
		angle_difference = (player.angle - enemy_angle) % (numpy.pi * 2)

		if angle_difference > numpy.pi * 11 / 6 or angle_difference < numpy.pi / 6:
			distance = numpy.sqrt((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2)
			enemy.angle_difference, enemy.distance = angle_difference, 1 / distance

			# cos, sin = 0.01 * (player.x - enemy.x) / distance, 0.01 * (player.y - enemy.y) / distance
			# for _ in range(int(distance / 0.01)):
			# 	x, y = enemy.x + cos, enemy.y + sin
			# 	if map[int(x)][int(y)]:
			# 		enemy.distance = 999
		else:
			enemy.distance = 999
	
	enemies = sorted(enemies, key = lambda enemy: enemy.distance)
	for index, enemy in enumerate(enemies):
		if enemy.distance > MAP_SIZE:
			break

		scaling = min(enemy.distance, 2) / numpy.cos(enemy.angle_difference)
		x = HALF_WIDTH - WIDTH * numpy.sin(enemy.angle_difference) - TEXTURE_RES * scaling / 2
		y = HALF_HEIGHT + HALF_HEIGHT * scaling - TEXTURE_RES * scaling / 2
		surface = pygame.transform.scale(enemy_textures[int(enemy.index)], (TEXTURE_RES * scaling, TEXTURE_RES * scaling))

		screen.blit(surface, (x, y))
		
		if player.shooting_state:
			if x < HALF_WIDTH < x + TEXTURE_RES * scaling:
				enemy.health -= 1
				if enemy.health <= 0:
					enemies = numpy.delete(enemies, index)
				player.shooting_state = False
	player.shooting_state = False
	
	return enemies