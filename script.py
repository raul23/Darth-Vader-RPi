import os
import threading
import time

import pygame
import RPi.GPIO as GPIO


SOUNDS_DIR = os.path.expanduser('~/Data/star_wars_sound_effects/ogg')


class SoundWrapper:
    def __init__(self, name, filename, channel):
        self.name = name
        self.filename = filename
        self.filepath = os.path.join(SOUNDS_DIR, filename)
        self.channel = channel
        # Load sound file
        self.pygame_sound = pygame.mixer.Sound(self.filepath)

    def play(self, loops=0):
        self.channel.play(self.pygame_sound, loops)

    def stop(self):
        self.channel.stop()


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
    channel1 = pygame.mixer.Channel(0)  # Breathing sound
    channel1.set_volume(0.2)
    channel2 = pygame.mixer.Channel(1)  # Song
    channel3 = pygame.mixer.Channel(2)  # Lightsaber sound

    sounds_to_load = [
        ('breathing_sound', 'darth_vader_breathing_GOOD.ogg',
         channel1, True, -1),
        ('lightsaber_open_sound', 'lightsaber_darth_vader_opening.ogg',
         channel3, False),
        ('lightsaber_running_sound', 'lightsaber_darth_vader_running.ogg',
         channel3, False),
        ('lightsaber_close_sound', 'lightsaber_darth_vader_retraction.ogg',
         channel3, False),
        # ('imperial_march_song', 'song_the_imperial_march.ogg', channel2, False),
        {'quotes': [
            ('i_am_your_father',
             'quote_i_am_your_father_2_with_music_at_the_end.ogg',
             channel2),
            ('dont_make_me_destroy_you', 'quote_dont_make_me_destroy_you.ogg',
             channel2),
            ('give_yourself_to_the_dark_side',
             'quote_give_yourself_to_the_dark_side.ogg', channel2),
            ('if_you_only_knew_the_power_of_the_dark_side',
             'quote_if_you_only_knew_the_power_of_the_dark_side.ogg', channel2),
            ('nooooo', 'quote_nooooo.ogg', channel2),
            ('there_is_no_escape', 'quote_there_is_no_escape.ogg', channel2),
            ('your_lack_of_faith_is_disturbing',
             'quote_your_lack_of_faith_is_disturbing.ogg', channel2)]
         }
    ]
    loaded_sounds = {}
    print("Loading sound effects...")
    for s in sounds_to_load:
        if isinstance(s, tuple):
            print("Loading {}...".format(s[0]))
            loaded_sounds.setdefault(s[0], SoundWrapper(s[0], s[1], s[2]))
            if s[3]:
                loaded_sounds[s[0]].play(s[4])
        else:
            for quote in s['quotes']:
                print("Loading {}...".format(quote[0]))
                loaded_sounds.setdefault('quotes', [])
                loaded_sounds['quotes'].append(
                    SoundWrapper(quote[0], quote[1], quote[2]))
    quotes = loaded_sounds['quotes']
    ipdb.set_trace()

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
                    loaded_sounds['lightsaber_close_sound'].play()
                    time.sleep(0.3)
                    turn_off(22)
                else:
                    pressed_lightsaber = True
                    loaded_sounds['lightsaber_open_sound'].play()
                    loaded_sounds['lightsaber_running_sound'].play(-1)
                    time.sleep(0.3)
                    turn_on(22)
                time.sleep(0.2)
            elif not GPIO.input(24):
                print("Button 24 pressed...")
                loaded_sounds['imperial_march_song'].play()
                time.sleep(0.2)
            elif not GPIO.input(25):
                print("Button 25 pressed...")
                quote = quotes[quote_idx % len(quotes)]
                quote_idx += 1
                quote.play()
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


if __name__ == '__main__':
    start()
