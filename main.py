#!/usr/bin/python

from pygame import camera
import pygame
import time
from HeadsUpDisplay import HUD, Locations

def main_loop():
	camera.init()
	cam = camera.Camera(camera.list_cameras()[0])

	(width, height) = cam.get_size()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Webcam Thing')
	pygame.init()
	cam.start()

	clock = pygame.time.Clock()
	hud = HUD((width, height))

	countdown = -1

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
					break
				elif event.key == pygame.K_SPACE:
					countdown = int(time.time()) + 3
					print 'set countdown to {t}'.format(t=countdown)
		
		now = time.time()

		cam_surf = cam.get_image()
		screen.blit(cam_surf, (0,0))
		if countdown > 0:
			hud.blit_to_surface(screen)
		pygame.display.flip()

		if countdown > now:
			hud.set_text(Locations.TOPCENTER, str(countdown - int(time.time())))
		elif countdown > -1:
			filename = 'images/webcam_{t}.png'.format(t=time.time())
			print 'saving image "{f}"'.format(f=filename)
			countdown = -1
			pygame.image.save(cam_surf, filename)

		clock.tick(30)
	
	cam.stop()
	pygame.quit()
	exit()

if __name__ == '__main__':
	main_loop()

