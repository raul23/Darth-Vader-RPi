"""Collection of LEDs-related utilities for the *Darth-Vader-RPi* project.
"""
import logging
import threading
import time
from logging import NullHandler

from darth_vader_rpi.utils import add_spaces_to_msg
from darth_vader_rpi.slot_leds_sequences import ACTION, CALM

try:
    import RPi.GPIO as GPIO
except ImportError:
    import SimulRPi.GPIO as GPIO

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

_DEFAULT_SEQ = {'action': ACTION, 'calm': CALM}


def turn_off_led(channel):
    """Turn off a LED from a given channel.

    Parameters
    ----------
    channel : int
        Channel number associated with a LED which will be turned off.

    """
    # logger.debug("LED {} off".format(led))
    GPIO.output(channel, GPIO.LOW)


def turn_on_led(channel):
    """Turn on a LED from a given channel.

    Parameters
    ----------
    channel : int
        Channel number associated with a LED which will be turned on.

    """
    # logger.debug("LED {} on".format(led))
    GPIO.output(channel, GPIO.HIGH)


def turn_on_slot_leds(top_led, middle_led, bottom_led, leds_sequence="action",
                      delay_between_steps=0.5, time_per_step=0.5):
    """A thread's **target function** that turns on the three slot LEDs in a
    precise sequence.

    These three LEDs are associated with Darth Vader's three slots located on
    his chest control box. These LEDs are labeled as '`top`', '`middle`', and
    '`bottom`', respectively.

    The three LEDs are turned on according to a default or custom sequence
    which repeats itself. The accepted values for ``leds_sequence`` are
    '`action`' and '`calm`' which represent Darth Vader's physiological state
    as a sequence of LEDs blinking in a particular order.

    The user can also provide its own ``leds_sequence`` by using a list of LED
    labels {'`top`', '`midddle`', '`bottom`'} arranged in a sequence specifying
    the order the slot LEDs should turn on/off, e.g. ``[['top', 'bottom'], [],
    ['middle'], []]`` will turn on/off the slot LEDs in this order::

        1. top + bottom LEDs turned on
        2. All LEDs turned off
        3. middle LED turned on
        4. All LEDs turned off

    Each step in the sequence will last for ``time_per_step`` seconds.

    There will be a delay of ``delay_between_steps`` seconds between
    each step in the previous example.

    The default sequences of slot LEDs were obtained from this
    `YouTube video`_.

    Parameters
    ----------
    top_led : int
        Channel number associated with the `Top` slot LED.
    middle_led : int
        Channel number associated with the `Middle` slot LED.
    bottom_led : int
        Channel number associated with the `Bottom` slot LED.
    leds_sequence : str or list, optional
        Sequence of slot LEDs on Darth Vader's chest box.

        If ``leds_sequence`` is a string, then it takes on one of these values
        which represent Darth Vader's physiological state: {'*action*',
        '*calm*'}.

        If ``leds_sequence`` is a list, then it must be a list of slot LED
        labels {'`top`', '`middle`', '`bottom`'} arranged in a sequence as to
        specify the order the slot LEDs should turn on/off, e.g.
        ``[['top', 'bottom'], [], ['middle'], []]`` will turn on/off the slot
        LEDs in this order::

            1. top + bottom LEDs turn on
            2. All LEDs turn off
            3. middle LED turn on
            4. All LEDs turn off

    delay_between_steps : float, optional
        Delay in seconds between each step in the sequence. The default value
        is 0.5 second.
    time_per_step : float, optional
        Time in seconds each step in the sequence will last. The default value
        is 0.5 second.

        .. important::

            This also affects the time all LEDs will remain turned off if a
            step in ``leds_sequence`` is an empty list.


    .. important::

        :meth:`turn_on_slot_leds` should be run by a thread and eventually
        stopped from the main program by setting its ``do_run`` attribute to
        `False` to let the thread exit from its target function.

        **For example**:

        .. code-block:: python

            th = threading.Thread(target=turn_on_slot_leds,
                                  args=(leds_channels))
            th.start()

            # Your other code ...

            # Time to stop thread
            th.do_run = False
            th.join()

    """
    # LED labels to Channel numbers Mapping (LCM)
    lcm = dict((('top', top_led), ('middle', middle_led), ('bottom', bottom_led)))
    if isinstance(leds_sequence, str):
        leds_sequence = leds_sequence.lower()
        assert leds_sequence in _DEFAULT_SEQ.keys(), \
            "Wrong type of leds_sequence: '{}' (choose from {})".format(
                leds_sequence, ", ".join(_DEFAULT_SEQ.keys()))
        leds_sequence = _DEFAULT_SEQ[leds_sequence]
    else:
        assert isinstance(leds_sequence, list), \
            "leds_sequence should be a string ({}) or a list: '{}'".format(
                ", ".join(_DEFAULT_SEQ.keys()), leds_sequence)
    th = threading.currentThread()
    subseq_idx = 0
    # TODO: use SimulRPi API to get LEDs states
    leds_states = dict(zip(lcm.keys(), [GPIO.LOW]*len(lcm)))
    while getattr(th, "do_run", True):
        leds_subsequence = leds_sequence[subseq_idx % len(leds_sequence)]
        subseq_idx += 1
        for channel_label, channel in lcm.items():
            cur_state = leds_states[channel_label]
            if channel_label in leds_subsequence:
                if cur_state != GPIO.HIGH:
                    leds_states[channel_label] = GPIO.HIGH
                    turn_on_led(channel)
            else:
                if cur_state != GPIO.LOW:
                    leds_states[channel_label] = GPIO.LOW
                    turn_off_led(channel)
        time.sleep(time_per_step+delay_between_steps)
    logger.debug(add_spaces_to_msg("Stopping thread: {}".format(th.name)))
