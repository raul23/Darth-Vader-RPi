import argparse
import codecs
import json
import logging
import os
import threading
import time

# import ipdb

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from logging import NullHandler

from darth_vader_rpi import __name__ as package_name, __version__, configs


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
SOUNDS_DIR = ""


class SoundWrapper:
    def __init__(self, name, filename, channel_obj):
        self.name = name
        self.filename = filename
        self.filepath = os.path.join(SOUNDS_DIR, filename)
        self.channel_obj = channel_obj
        # Load sound file
        self.pygame_sound = pygame.mixer.Sound(self.filepath)

    def play(self, loops=0):
        self.channel_obj.play(self.pygame_sound, loops)

    def stop(self):
        self.channel_obj.stop()


# TODO: use load_json() from pyutils
def load_json(filepath, encoding='utf8'):
    try:
        with codecs.open(filepath, 'r', encoding) as f:
            data = json.load(f)
    except OSError:
        raise
    else:
        return data


def msg_with_spaces(msg, nb_spaces=20):
    return "{}{}".format(msg, " " * nb_spaces)


def run_led_sequence(led_channels):
    # TODO: assert led_channels, i.e. keys (top, ...)
    t = threading.currentThread()
    seq_idx = 0
    sequence = [[led_channels['top'], led_channels['bottom']],
                [led_channels['top']],
                [led_channels['bottom']],
                [led_channels['middle'], led_channels['bottom']],
                [led_channels['middle']],
                [led_channels['top'], led_channels['middle']],
                [led_channels['top'], led_channels['middle'], led_channels['bottom']]]
    while getattr(t, "do_run", True):
        leds_step = sequence[seq_idx % len(sequence)]
        seq_idx += 1
        turn_off_led(led_channels['top'])
        turn_off_led(led_channels['middle'])
        turn_off_led(led_channels['bottom'])
        for channel in leds_step:
            turn_on_led(channel)
        time.sleep(2)
    logger.info("Stopping thread: run_leds_sequence()")


def setup_argparser():
    # Setup the parser
    parser = argparse.ArgumentParser(
        # usage="%(prog)s [OPTIONS]",
        prog=package_name,
        description='''\
    WRITEME''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # ===============
    # General options
    # ===============
    parser.add_argument("--version", action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Enable quiet mode, i.e. nothing will be print.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print various debugging information, e.g. print "
                             "traceback when there is an exception."),
    parser.add_argument("-d", "--debug", action="store_true",
                        help="WRITEME.")
    return parser.parse_args()


def turn_off_led(channel):
    # logger.debug("LED {} off".format(led))
    GPIO.output(channel, GPIO.LOW)


def turn_on_led(channel):
    # logger.debug("LED {} on".format(led))
    GPIO.output(channel, GPIO.HIGH)

 
def start(main_cfg):
    logger.info("Starting")

    logger.info("RPi initialization")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # LEDs
    top_led = main_cfg['GPIO']['top_led']
    middle_led = main_cfg['GPIO']['middle_led']
    bottom_led = main_cfg['GPIO']['bottom_led']
    lightsaber_led = main_cfg['GPIO']['lightsaber_led']
    GPIO.setup(top_led, GPIO.OUT)
    GPIO.setup(middle_led, GPIO.OUT)
    GPIO.setup(bottom_led, GPIO.OUT)
    GPIO.setup(lightsaber_led, GPIO.OUT)
    # Buttons
    lightsaber_button = main_cfg['GPIO']['lightsaber_button']
    song_button = main_cfg['GPIO']['song_button']
    quotes_button = main_cfg['GPIO']['quotes_button']
    GPIO.setup(lightsaber_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(song_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(quotes_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    ### Sound
    # Create separate channel
    # Ref.: stackoverflow.com/a/59742418
    channel1 = pygame.mixer.Channel(0)  # Breathing sound
    channel2 = pygame.mixer.Channel(1)  # Song
    channel3 = pygame.mixer.Channel(2)  # Lightsaber sound
    channels = {1: channel1, 2: channel2, 3: channel3}
    # Set volume
    channels[1].set_volume(main_cfg['channel1_volume'])
    channels[2].set_volume(main_cfg['channel2_volume'])
    channels[3].set_volume(main_cfg['channel3_volume'])

    loaded_sounds = {}
    logger.info("Loading sound effects")

    def load_sounds(sounds):
        for i, s in enumerate(sounds):
            if s.get('quotes'):
                for quote in s['quotes']:
                    logger.info("Loading {}...".format(quote['name']))
                    loaded_sounds.setdefault('quotes', [])
                    channel_obj = channels[quote['channel']]
                    loaded_sounds['quotes'].append(
                        SoundWrapper(quote['name'], quote['filename'], channel_obj))
            else:
                if s.get('imperial_march_song'):
                    s_list = [s]
                else:
                    s_list = s['sound_effects']
                for s in s_list:
                    sound = s.popitem()
                    sound_name = sound[0]
                    sound_info = sound[1]
                    logger.info("Loading {}...".format(sound[0]))
                    channel_obj = channels[sound_info['channel']]
                    loaded_sounds.setdefault(sound_name,
                                             SoundWrapper(sound_name,
                                                          sound_info['filename'],
                                                          channel_obj))
                    if sound_info.get('play'):
                        loops = sound_info.get('loops', -1)
                        loaded_sounds[sound_name].play(loops)

    sounds = [{"quotes": main_cfg['quotes']},
              {"imperial_march_song": main_cfg['imperial_march_song']},
              {"sound_effects": main_cfg['sound_effects']}]
    load_sounds(sounds)
    quotes = loaded_sounds['quotes']

    led_channels = {'top': top_led, 'middle': middle_led, 'bottom': bottom_led}
    th = threading.Thread(target=run_led_sequence, args=(led_channels,))
    th.start()

    logger.info("")
    logger.info(msg_with_spaces("Press any button"))
    pressed_lightsaber = False
    quote_idx = 0

    try:
        while True:
            if not GPIO.input(lightsaber_button):
                logger.debug("\n\nButton {} pressed...".format(lightsaber_button))
                if pressed_lightsaber:
                    pressed_lightsaber = False
                    loaded_sounds['lightsaber_close_sound'].play()
                    time.sleep(0.3)
                    turn_off_led(22)
                else:
                    pressed_lightsaber = True
                    loaded_sounds['lightsaber_open_sound'].play()
                    loaded_sounds['lightsaber_running_sound'].play(-1)
                    time.sleep(0.3)
                    turn_on_led(lightsaber_led)
                time.sleep(0.2)
            elif not GPIO.input(song_button):
                logger.debug("\n\nButton {} pressed...".format(song_button))
                loaded_sounds['imperial_march_song'].play()
                time.sleep(0.2)
            elif not GPIO.input(quotes_button):
                logger.debug("\n\nButton {} pressed...".format(quotes_button))
                quote = quotes[quote_idx % len(quotes)]
                quote_idx += 1
                quote.play()
                time.sleep(0.2)
    except Exception as e:
        logger.exception(msg_with_spaces("Error: {}".format(e)))
        logger.info(msg_with_spaces("Exiting..."))
        # logger.info("Error: {}".format(e))
        # logger.info("Exiting...")
    except KeyboardInterrupt:
        logger.info(msg_with_spaces("Exiting..."))
        # logger.info("Exiting...")

    logger.info(msg_with_spaces("Cleanup..."))
    # logger.info("Cleanup...")
    turn_off_led(top_led)
    turn_off_led(middle_led)
    turn_off_led(bottom_led)
    turn_off_led(lightsaber_led)
    GPIO.cleanup()
    th.do_run = False
    th.join()
    channel1.stop()
    channel2.stop()
    channel3.stop()


if __name__ == '__main__':
    args = setup_argparser()
    main_cfg_filepath = os.path.join(configs.__path__[0], "main_cfg.json")
    main_cfg_dict = load_json(main_cfg_filepath)
    SOUNDS_DIR = os.path.expanduser(main_cfg_dict['sounds_directory'])
    logging_filepath = os.path.join(configs.__path__[0], "logging.json")
    # log_dict = load_json(logging_filepath)

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # Setup console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("pygame initialization...")
    pygame.init()
    pygame.mixer.init()

    if args.debug:
        import SimulRPi.GPIO as GPIO
        logger.info("Debug mode enabled")
    else:
        import RPi.GPIO as GPIO

    start(main_cfg_dict)
