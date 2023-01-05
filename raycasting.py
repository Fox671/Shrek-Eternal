from numba import njit
from settings import *
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
		while map[int(x)][int(y)] == 0:
			x, y = x + cos * 0.02, y + sin * 0.02

		n = abs((x - player_x) / cos)
		height = int(HOR_NUM_RAYS / (fov_cos * n + 0.0001))

		xx = int(x * 2 % 1 * (WALL_TEXTURE_RES - 1))
		if x % 1 < 0.02 or x % 1 > 0.98:
			xx = int(y * 2 % 1 * (WALL_TEXTURE_RES - 1))
		yy = numpy.linspace(0, (WALL_TEXTURE_RES - 1) * 2, height * 2) % (WALL_TEXTURE_RES - 1)

		shade = 0.3 + (height / HOR_NUM_RAYS) * 0.7
		if shade > 1: shade = 1

		for k in range(height * 2):
			if HOR_NUM_RAYS - height + k >= 0 and HOR_NUM_RAYS - height + k < HOR_NUM_RAYS * 2:
				frame[vert_ray][HOR_NUM_RAYS - height + k] = shade * textures[1][xx][int(yy[k])]

		for hor_ray in range(HOR_NUM_RAYS - height):
			n = (HOR_NUM_RAYS / (HOR_NUM_RAYS - hor_ray)) / fov_cos
			x, y = player_x + cos * n, player_y + sin * n
			xx, yy = int(x * 2 % 1 * (WALL_TEXTURE_RES - 1)), int(y * 2 % 1 * (WALL_TEXTURE_RES - 1))
			shade = 0.2 + 0.8 * (1 - hor_ray / HOR_NUM_RAYS)

			frame[vert_ray][HOR_NUM_RAYS * 2 - hor_ray - 1] = shade * textures[0][xx][yy]
			frame[vert_ray][hor_ray] = shade * textures[2][xx][yy]

	return frame

def display(player_x: float, player_y: float, player_angle: float, enemy_x: numpy.ndarray, enemy_y: numpy.ndarray, enemy_index: numpy.ndarray, wall_textures: numpy.ndarray, enemy_textures: numpy.ndarray, map: numpy.ndarray, screen: pygame.Surface) -> numpy.ndarray:
	frame = numpy.empty((VERT_NUM_RAYS, HOR_NUM_RAYS * 2, 3))
	frame = _display(player_x, player_y, player_angle, wall_textures, map, frame)

	surface = pygame.surfarray.make_surface(frame * 255)
	surface = pygame.transform.scale(surface, RES)

	screen.blit(surface, (0, 0))
	
	for enemy_x, enemy_y, enemy_index in zip(enemy_x, enemy_y, enemy_index):
		enemy_angle = numpy.arctan((enemy_x - player_x) / (enemy_y - player_y))

		if abs(player_x + numpy.cos(enemy_angle) - enemy_x) > abs(player_x - enemy_x):
			enemy_angle = (enemy_angle - numpy.pi) % (numpy.pi * 2)
		angle_difference = (player_angle - enemy_angle) % (numpy.pi * 2)

		if angle_difference > numpy.pi * 11 / 6 or angle_difference < numpy.pi / 6:
			distance = numpy.sqrt((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2)
			cos = numpy.cos(angle_difference)
			scaling = min(1 / distance, 2) / cos

			x = WIDTH // 2 - WIDTH * numpy.sin(angle_difference) - ENEMY_TEXTURE_RES * scaling / 2
			y = HEIGHT // 2 + HEIGHT // 2 * scaling - ENEMY_TEXTURE_RES * scaling / 2
			surface = pygame.transform.scale(enemy_textures[enemy_index], (ENEMY_TEXTURE_RES * scaling, ENEMY_TEXTURE_RES * scaling))
	
			screen.blit(surface, (x, y))