import sys
import pygame
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to key presses."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up =True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullets(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()
		

def check_keyup_events(event, ship):
	"""Respond to key releases."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False

def check_events(ai_settings, screen, ship, bullets):
	"""Respond to keypresses and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
				
def update_screen(ai_settings, screen, ship, aliens, bullets, stars):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)

	stars.draw(screen)

	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	# Make the most recently drawn screen visible
	pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
	"""Update position of bullets and get rid of old bullets"""
	# Update bullet positions.
	bullets.update()

	# Get rid of bullets that have dissapeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
	"""Respond to bullet-alien collision"""
	# Check for any bullets that have hit an alien.
	# If so, get rid of the bullet and the alien.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if len(aliens) == 0:
		# Destory existinf bullet and create new fleet.
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)

def fire_bullets(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet"""
	# Create a new bullet and add it to the bullets group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit the screen"""
	available_space_y = (ai_settings.screen_height - 
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row."""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a ful fleet of aliens"""
	# Create an alien and find the number of aliens in a row.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)
	
	# Create the first row of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
	"""Respond appropiately if any aliens have reached an edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, aliens):
	"""
	Check if the fleet is at an edge,
		and then update the position of all aliens in the fleet.
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

def get_number_stars_x(ai_settings, star_width):
	"""Determine the number of stars that fit in a row"""
	available_space_x = ai_settings.screen_width - 2 * star_width
	number_stars_x = int(available_space_x / (2 * star_width))
	return number_stars_x

def get_number_rows_star(ai_settings, star_height):
	"""Determine the number of rows of stars that fit the screen"""
	available_space_y = ai_settings.screen_height - 2 * star_height
	number_rows = int(available_space_y / (2 * star_height))
	return number_rows

def create_star(screen, stars, star_number, row_number):
	"""Create an alien and place it in the row."""
	star = Star(screen)
	star_width = star.rect.width
	random_number = randint(-15, 15)
	star.x = star_width + random_number * star_width * star_number
	star.rect.x = star.x
	star.rect.y = star.rect.height + random_number * star.rect.height * row_number
	stars.add(star)


def create_grid(ai_settings, screen, stars):
	"""Create a ful grid of stars"""
	# Create a star and find the number of stars in a row.
	star = Star(screen)
	number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
	number_rows = get_number_rows_star(ai_settings, star.rect.height)
	
	# Create the first row of stars.
	for row_number in range(number_rows):
		for star_number in range(number_stars_x):
			create_star(screen, stars, star_number, row_number)
