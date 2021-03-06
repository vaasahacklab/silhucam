import pygame
import pygame.camera
from pygame.transform import scale
import os, sys
import time

from PIL import Image, ImageEnhance
from subprocess import call

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

cam = None
pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[-1])
cam.start()

def loop(should_save=False):
	global cam
	
	# Get image from webcam and convert for Pillow
	img = cam.get_image()
	imgstr = pygame.image.tostring(img, 'RGB')
	im = Image.frombytes('RGB', img.get_size(), imgstr)

	# ENHANCE!
	#color_enhancer = ImageEnhance.Color(im)
	#im = color_enhancer.enhance(0.0)
	contrast_enhancer = ImageEnhance.Contrast(im)
	im = contrast_enhancer.enhance(10.0)

	# Convert to monochrome and back
	im = im.convert(mode='1', dither=Image.NONE)
	im = im.convert(mode='RGB')

	# Convert image for PyGame
	raw_str = im.tobytes("raw", 'RGB')
	img = pygame.image.fromstring(raw_str, im.size, 'RGB')

	# Disply image
	img_to_screen = scale(img, screen.get_size())
	screen.blit(img_to_screen,(0,0))

	pygame.display.flip()

	if should_save:
		# Setup variables
		current_path = os.path.dirname(os.path.abspath(__file__))
		timestring = time.strftime("%Y-%m-%d_%H-%M-%S_")
		bitmap_filename = os.path.join(current_path, timestring + 'snap.bmp')
		vector_filename = os.path.join(current_path, timestring + 'snap.svg')

		# Save image
		im.save(bitmap_filename, 'BMP')

		# Trace image to SVG
		call(["potrace", "-o", vector_filename, "-s", bitmap_filename])

		# Open Inkscape if not disabled
		if '--no-inkscape' not in sys.argv:
			call(["inkscape", vector_filename])

		# Small delay feels good
		pygame.time.wait(200)

def main():
	should_exit = False

	while should_exit == False:
		should_save = False

		# Handle key and other events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				should_exit = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					should_exit = True
				if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
					should_save = True
			if event.type == pygame.VIDEORESIZE:
				# TODO Scaling fails randomly after resize, investigate
				screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

		# TODO limit framerate?
		loop(should_save)

if __name__ == "__main__":
	main()
