"""Module for activating a Darth Vader figurine by turning on LEDs on his suit
and playing sounds, all done via a Raspberry Pi (RPi).

The LEDs illuminate Darth Vader's lightsaber and the three slots in the chest
control box. 3 push buttons control the following sounds and LEDs:

1. Some of his famous quotes
2. The Imperial march theme song
3. The lightsaber drawing, hum and retraction sounds
4. The lightsaber illumination (3 LEDs)

His iconic breathing sound plays in the background indefinitely almost as soon
as the RPi is run with the script.

.. URLs

.. default_main_cfg
.. _gpio_channels: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L11
.. _main config file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json

"""
import logging
import os
import threading
import time
from logging import NullHandler

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from darth_vader_rpi.utils import add_spaces_to_msg, SoundWrapper
from darth_vader_rpi.ledutils import turn_on_led, turn_off_led, turn_on_slot_leds

GPIO = None

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


class ExceptionThread(threading.Thread):
    """A subclass from :class:`threading.Thread` that defines threads that can
    catch errors if their target functions raise an exception.

    Parameters
    ----------
    verbose : bool, optional
        If `True`, print the traceback when there is an exception. Otherwise,
        print just a one-line error message, e.g. ``KeyError: 'test'``
    args : tuple, optional
        Positional arguments given to the thread's target function.
    kwargs : dict, optional
        Keyword arguments given to the thread's target function.

    Attributes
    ----------
    exc: :class:`Exception`
        Represents the exception raised by the target function.

    References
    ----------
    * `stackoverflow <https://stackoverflow.com/a/51270466>`__

    """

    def __init__(self, verbose=False, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.verbose = verbose
        self.exc = None

    def run(self):
        """Method representing the thread’s activity.

        Overridden from the base class :class:`threading.Thread`. This method
        invokes the callable object passed to the object’s constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        It also saves and logs any error that the target function might raise.

        """
        try:
            self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
            if self.verbose:
                logger.exception(add_spaces_to_msg("Error: {}".format(e)))
            else:
                # TODO: add next line in a utility function
                err_msg = "{}: {}".format(str(e.__class__).split("'")[1], e)
                logger.error(add_spaces_to_msg(err_msg))


class DarthVader:
    """Class for activating a Darth Vader figurine by turning on LEDs on his
    suit and playing sounds, all done via a Raspberry Pi (RPi).

    The `main config file`_ is used to setup the script :mod:`start_dv`, such
    as the GPIO pins and the sound files.

    Parameters
    ----------
    main_cfg : dict
        Dictionary containing the configuration data to setup the script
        :mod:`start_dv`, such as the GPIO pins and the sound files. See
        `main config file`_ for a detailed look into its content.

    Attributes
    ----------
    th_slot_leds : start_dv.ExceptionThread
        Thread responsible for turning on the three slot LEDs in a precise
        sequence.

        Its target function is :meth:`ledutils.turn_on_slot_leds`.

    """

    def __init__(self, main_cfg):
        self.main_cfg = main_cfg
        self.th_slot_leds = None

    def activate(self):
        """Activate a Darth Vader figurine by turning on LEDs on his suit and
        playing sounds, all done via an RPi.

        While the method waits for a pressed button, you can exit by pressing
        ``ctr`` + ``c``.

        Returns
        -------
        retcode: int
            If the method is run without any :exc:`Exception`, the return code is
            0. Otherwise, it is 1.

            Also, even if there is an :exc:`Exception`, the method will try to
            clean up before exiting.

        """
        retcode = 0
        gpio_channels = {}
        loaded_sounds = {}
        try:
            logger.debug("pygame mixer initialization")
            pygame.mixer.init()
            logger.debug("RPi initialization")
            logger.debug("")
            # Set the numbering system used to identify the I/O pins on an RPi
            modes = {'BOARD': GPIO.BOARD, 'BCM': GPIO.BCM}
            GPIO.setmode(modes[self.main_cfg['mode'].upper()])
            GPIO.setwarnings(False)
            # Setup LEDs and buttons
            for gpio_ch in self.main_cfg['gpio_channels']:
                # TODO: IMPORTANT add channel_type in main_cfg so you don't
                # have to check '_led'
                if gpio_ch['channel_id'].endswith("_led"):
                    # LEDs
                    GPIO.setup(gpio_ch['channel_number'], GPIO.OUT)
                else:
                    # Buttons
                    GPIO.setup(gpio_ch['channel_number'], GPIO.IN,
                               pull_up_down=GPIO.PUD_UP)
                gpio_channels[gpio_ch['channel_id']] = {
                    'channel_number': gpio_ch['channel_number'],
                    'channel_name': gpio_ch['channel_name'],
                    'key': gpio_ch.get('key'),
                    'led_symbol': gpio_ch.get('led_symbols')
                }

            ### Sound
            # Create separate channel
            # Ref.: stackoverflow.com/a/59742418
            audio_channels = self.main_cfg['audio_channels']
            for ch_dict in audio_channels:
                channel = pygame.mixer.Channel(ch_dict['channel_id'])
                channel.set_volume(ch_dict['volume'])

            sounds_dir = self.main_cfg['sounds_directory']
            # Load sounds from cfg
            logger.info('Loading sounds...')
            logger.info("")
            for sound_type in ['quotes', 'songs', 'sound_effects']:
                logger.debug('Loading {}'.format(sound_type.replace("_", " ")))
                for sound in self.main_cfg[sound_type]:
                    sound_id = sound['id']
                    sound_name = sound['name']
                    filepath = os.path.join(sounds_dir, sound['filename'])
                    logger.debug('Loading "{}": {}'.format(sound_name, filepath))
                    sw = SoundWrapper(
                        sound_id=sound_id,
                        sound_name=sound_name,
                        sound_filepath=filepath,
                        channel_id=sound['audio_channel_id'],
                        mute=sound.get('mute', False))
                    if sound_type == "quotes":
                        loaded_sounds.setdefault("quotes", {})
                        loaded_sounds['quotes'].setdefault(sound_id, sw)
                    else:
                        loaded_sounds.setdefault(sound_id, sw)
                    if sw.sound_id == 'breathing_sound' and not sw.mute:
                        loops = sound.get('loops', 0)
                        loaded_sounds[sound_id].play(loops)
                logger.debug("")
            quotes = list(loaded_sounds['quotes'].values())

            self.th_slot_leds = ExceptionThread(
                name="thread_slot_leds",
                target=turn_on_slot_leds,
                verbose=self.main_cfg['verbose'],
                kwargs=dict(
                    top_led=gpio_channels['top_led']['channel_number'],
                    middle_led=gpio_channels['middle_led']['channel_number'],
                    bottom_led=gpio_channels['bottom_led']['channel_number'],
                    leds_sequence=self.main_cfg['slot_leds']['sequence'],
                    delay_between_steps=self.main_cfg['slot_leds']['delay_between_steps'],
                    time_per_step=self.main_cfg['slot_leds']['time_per_step']))
            """
                args=(gpio_channels['top_led']['channel_number'],
                      gpio_channels['middle_led']['channel_number'],
                      gpio_channels['bottom_led']['channel_number'],
                      self.main_cfg['slot_leds']['sequence'],
                      self.main_cfg['slot_leds']['delay_between_steps'],
                      self.main_cfg['slot_leds']['time_per_step']))
            """
            self.th_slot_leds.start()
            logger.info("")
            logger.info(add_spaces_to_msg("Press buttons"))
            pressed_lightsaber = False
            quote_idx = 0

            while True:
                if not GPIO.input(gpio_channels['lightsaber_button']['channel_number']):
                    # logger.debug("\n\nButton {} pressed...".format(
                        # lightsaber_button))
                    if pressed_lightsaber:
                        pressed_lightsaber = False
                        loaded_sounds['lightsaber_retraction_sound'].play()
                        time.sleep(0.1)
                        turn_off_led(22)
                    else:
                        pressed_lightsaber = True
                        loaded_sounds['lightsaber_drawing_sound'].play()
                        loaded_sounds['lightsaber_hum_sound'].play(-1)
                        time.sleep(0.1)
                        turn_on_led(gpio_channels['lightsaber_led']['channel_number'])
                    time.sleep(0.2)
                elif not GPIO.input(gpio_channels['song_button']['channel_number']):
                    # logger.debug("\n\nButton {} pressed...".format(song_button))
                    loaded_sounds['imperial_march_song'].play()
                    time.sleep(0.2)
                elif not GPIO.input(gpio_channels['quotes_button']['channel_number']):
                    """
                    logger.debug("\n\nButton {} pressed...".format(
                        gpio_channels['quotes_button']['channel_name']))
                    """
                    quote = quotes[quote_idx % len(quotes)]
                    quote_idx += 1
                    quote.play()
                    time.sleep(0.2)
                elif not self.th_slot_leds.is_alive():
                    retcode = 1
                    logger.info(add_spaces_to_msg("Exiting..."))
                    break
        except Exception as e:
            retcode = 1
            if self.main_cfg['verbose']:
                logger.exception(add_spaces_to_msg("Error: {}".format(e)))
            else:
                # logger.error(add_spaces_to_msg(e.__repr__()))
                # TODO: add next line in a utility function
                err_msg = "{}: {}".format(str(e.__class__).split("'")[1], e)
                logger.error(add_spaces_to_msg(err_msg))
        except KeyboardInterrupt:
            logger.info(add_spaces_to_msg("Exiting..."))
            closing_sound = loaded_sounds.get('closing_sound')
            if closing_sound and not closing_sound.mute:
                closing_sound.play()
                time.sleep(1)
        finally:
            self.cleanup(gpio_channels)
            return retcode

    def cleanup(self, gpio_channels):
        """Clean up any resources such as threads and GPIO channels.

        The cleanup consists in the following actions:

        * turn off each LED
        * stop the thread ``th_slot_leds``
        * stop each audio channel
        * call ``RPi.GPIO.cleanup()`` which will return all GPIO channels back
          to inputs with no pull up/down

          * If in simulation mode, :obj:`SimulRPi.GPIO.cleanup` is called to
            stop the threads among other things

        Parameters
        ----------
        gpio_channels : dict
            Dictionary mapping channel id (:obj:`str`) to channel attributes
            (:obj:`dict`). The channel attributes consist in the following:

                * ``channel_number``
                * ``channel_name``
                * ``key``
                * ``led_symbols``

            .. note::

                These channel attributes are those found in the setting
                `gpio_channels`_ from the main configuration file.

        """
        if hasattr(GPIO, "setprinting"):
            GPIO.setprinting(False)
        time.sleep(0.1)
        if gpio_channels:
            for channel_id, channel_info in gpio_channels.items():
                if channel_id.endswith("_led"):
                    turn_off_led(channel_info['channel_number'])
        logger.info(add_spaces_to_msg("Cleanup..."))
        if self.th_slot_leds:
            self.th_slot_leds.do_run = False
            self.th_slot_leds.join()
            logger.debug(add_spaces_to_msg("Thread stopped: {}".format(
                self.th_slot_leds.name)))
        for ch in self.main_cfg['audio_channels']:
            pygame.mixer.Channel(ch['channel_id']).stop()
        GPIO.cleanup()
