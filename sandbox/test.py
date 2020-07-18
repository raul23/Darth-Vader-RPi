class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


import multiprocessing
import sys
import threading
import time


def check_keyboard():
    t = threading.currentThread()
    getch = _Getch()
    while getattr(t, "do_run", True):
        val = getch()
        print(val)
    print("Stopping thread: check_keyboard()")


def check_keyboard_mp():
    p = multiprocessing.current_process()
    getch = _Getch()
    while getattr(p, "do_run", True):
        val = getch()
        print(val)
    print("Stopping process: check_keyboard()")


keyboard_th = threading.Thread(target=check_keyboard, args=())
keyboard_th.start()
# multiprocessing.set_start_method('spawn')
# keyboard_mp = multiprocessing.Process(target=check_keyboard_mp(), args=())
# keyboard_mp.daemon = True
# keyboard_mp.start()

print("Sleeping...")
time.sleep(1)
print("Waking uo")
print("Waiting for thread....")

keyboard_th.do_run = False
keyboard_th.join(1)
# keyboard_mp.do_run = False
# keyboard_mp.join(1)
# keyboard_mp.terminate()
print("Ending")
sys.exit(1)
