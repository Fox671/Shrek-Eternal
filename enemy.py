from settings import *
import numpy

class Enemy:
	def __init__(self) -> None:
		self.x = numpy.random.uniform(MAP_WIDTH)
		self.y = numpy.random.uniform(MAP_HEIGHT)
		self.speed = numpy.random.uniform(1.8, 2.2)

		self.health =numpy.random.randint(7, 9)
		self.index = numpy.random.randint(3)

		self.angle_difference = 0.0
		self.distance = 0.0
	
	def animate(self, fps: float) -> None:
		self.index += 2 / fps
		if self.index >= 3:
			self.index = 0

	def move(self) -> None:
		pass

	def update(self, fps: float) -> None:
		self.animate(fps)
		self.move()