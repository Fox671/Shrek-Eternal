from settings import *
import numpy
import pygame

class Player:
	def __init__(self) -> None:
		self.x, self.y = 3, 3

		self.movement_speed = 2.0
		self.rotation_speed = 0.0005
		self.angle = 0
	
	# movement function
	def move(self, fps: float) -> None:
		mouse_pressed = pygame.mouse.get_pressed()
		if mouse_pressed[2]:
			x = self.x + numpy.cos(self.angle) * self.movement_speed / fps
			y = self.y + numpy.sin(self.angle) * self.movement_speed / fps

			if not (map[int(x - 0.1)][int(y)] or map[int(x + 0.1)][int(y)] or map[int(x)][int(y - 0.1)] or map[int(x)][int(y + 0.1)]):
				self.x, self.y = x, y
			if not (map[int(self.x - 0.1)][int(y)] or map[int(self.x + 0.1)][int(y)] or map[int(self.x)][int(y - 0.1)] or map[int(self.x)][int(y + 0.1)]):
				self.y = y
			if not (map[int(x - 0.1)][int(self.y)] or map[int(x + 0.1)][int(self.y)] or map[int(x)][int(self.y - 0.1)] or map[int(x)][int(self.y + 0.1)]):
				self.x = x

	# rotation function
	def rotate(self, screen: pygame.surface.Surface) -> None:
		mouse_pos = pygame.mouse.get_pos()
		if screen.get_rect().collidepoint(mouse_pos):
			pygame.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)

		mouse_rel = pygame.mouse.get_rel()
		if mouse_rel[0] != 0:
			self.angle += mouse_rel[0]*self.rotation_speed

	def update(self, screen: pygame.surface.Surface, fps: float) -> None:
		self.move(fps)
		self.rotate(screen)