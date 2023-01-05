from settings import *
import numpy

class Enemy:
	def __init__(self) -> None:
		self.x = numpy.random.uniform(MAP_WIDTH)
		self.y = numpy.random.uniform(MAP_HEIGHT)

		self.index = numpy.random.randint(3)
		self.speed = numpy.random.uniform(1.8, 2.2)

	def update(self, fps: float) -> None:
		self.x, self.y = self.x, self.y