import os
import threading
import time

import pygame
import RPi.GPIO as GPIO


SOUNDS_DIR = os.path.expanduser('~/Data/star_wars_sound_effects')


def run_leds_sequence(leds):
	t = threading.currentThread()
	seq_idx = 0
	sequence = [[leds['top'], leds['bottom']],
				[leds['top']],
				[leds['bottom']],
				[leds['middle'], leds['bottom']],
				[leds['middle']],
				[leds['top'], leds['middle']],
				[leds['top'], leds['middle'], leds['bottom']]]
	while getattr(t, "do_run", True):
		list_leds = sequence[seq_idx % len(sequence)]
		seq_idx += 1
		turn_off(leds['top'])
		turn_off(leds['middle'])
		turn_off(leds['bottom'])
		for led in list_leds:
			turn_on(led)
		time.sleep(2)
	print("Stopping thread")


def turn_off(led):
	print("LED {} off".format(led))
	GPIO.output(led, GPIO.LOW)
	

def turn_on(led):
	print("LED {} on".format(led))
	GPIO.output(led, GPIO.HIGH)

 
def start():
	print("Starting...")
	
	print("RPi initialization...")
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	# LEDs
	top_led = 11
	middle_led = 9
	bottom_led = 10
	GPIO.setup(top_led, GPIO.OUT)
	GPIO.setup(middle_led, GPIO.OUT)
	GPIO.setup(bottom_led, GPIO.OUT)
	GPIO.setup(22, GPIO.OUT)
	# Buttons
	GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	print("pygame initialization...")
	pygame.init()
	pygame.mixer.init()
	
	### Sound
	# Create separate channel
	# Ref.: stackoverflow.com/a/59742418
	channel1 = pygame.mixer.Channel(0)
	channel1.set_volume(0.2)
	channel2 = pygame.mixer.Channel(1)
	channel3 = pygame.mixer.Channel(3)
	
	print("Loading songs...")
	
	# Darth Vader breathing sound
	print(os.path.join(SOUNDS_DIR, 'darth_vader_breathing_GOOD.ogg'))
	breathing_sound = pygame.mixer.Sound(
		os.path.join(SOUNDS_DIR, 'darth_vader_breathing_GOOD.ogg'))
	channel1.play(breathing_sound, -1)  # loop indefinitely
	
	# Lightsaber sounds
	lightsaber_open_sound = pygame.mixer.Sound(
		os.path.join(SOUNDS_DIR, 'lightsaber_darth_vader_opening.ogg'))
	lightsaber_running_sound = pygame.mixer.Sound(
		os.path.join(SOUNDS_DIR, 'lightsaber_darth_vader_running.ogg'))
	lightsaber_close_sound = pygame.mixer.Sound(
		os.path.join(SOUNDS_DIR, 'lightsaber_darth_vader_retraction.ogg'))
	
	# Imperial March song
	#imperial_march_song = pygame.mixer.Sound(
	#	os.path.join(SOUNDS_DIR, 'song_the_imperial_march.ogg'))
	
	# Darth Vader quotes
	quotes = [
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_i_am_your_father_1.ogg')),
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_i_am_your_father_2_with_music_at_the_end.ogg')),
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_dont_make_me_destroy_you.ogg')),
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_give_yourself_to_the_dark_side.ogg')),
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_if_you_only_knew_the_power_of_the_dark_side.ogg')),
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_nooooo.ogg')),
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_there_is_no_escape.ogg')),
		pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'quote_your_lack_of_faith_is_disturbing.ogg'))]
	
	leds = {'top': top_led, 'middle': middle_led, 'bottom': bottom_led}
	th = threading.Thread(target=run_leds_sequence, args=(leds,))
	th.start()
	
	print("Press any button")
	pressed_lightsaber = False
	quote_idx = 0
	try:
		while True:
			if not GPIO.input(23):
				print("Button 23 pressed...")
				if pressed_lightsaber:
					pressed_lightsaber = False
					channel3.play(lightsaber_close_sound)
					time.sleep(0.3)
					turn_off(22)
				else:
					pressed_lightsaber = True
					channel3.play(lightsaber_open_sound)
					channel3.play(lightsaber_running_sound, -1)
					time.sleep(0.3)
					turn_on(22)
				time.sleep(0.2)
			elif not GPIO.input(24):
				print("Button 24 pressed...")
				channel2.play(imperial_march_song)
				time.sleep(0.2)
			elif not GPIO.input(25):
				print("Button 25 pressed...")
				quote = quotes[quote_idx % len(quotes)]
				quote_idx += 1
				channel2.play(quote)
				time.sleep(0.2)		
	except Exception as e:
		print("Error: ", e)
		print("\nExiting...")
	except KeyboardInterrupt:
		print("\nExiting...")
		
	print("Cleanup...")
	th.do_run = False
	th.join()
	turn_off(top_led)
	turn_off(middle_led)
	turn_off(bottom_led)
	turn_off(22)
	GPIO.cleanup()
	channel1.stop()
	channel2.stop()
	channel3.stop()

start()
