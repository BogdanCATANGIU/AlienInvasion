import pygame
from pygame.sprite import Sprite 

class Star(Sprite):
	"""A class to manage a grid of stars"""
	def __init__(self, screen):
		super().__init__()
		self.screen = screen

		# Load the star image and set its rect attribute
		self.image = pygame.image.load('images/star.bmp')
		self.rect = self.image.get_rect()

		# Start each new star near the bottom left of the screen
		self.rect.bottom = self.rect.width
		self.rect.y = self.rect.height

		# Store the alien's exact position
		self.x = float(self.rect.x)

	def blitme(self):
		"""Draw the star to it's current location."""
		self.screen.blit(self.image, self.rect)