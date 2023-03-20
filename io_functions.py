import platform
import os

from typing import List


if "windows" in platform.system().lower():
    def clear_console():
        os.system('cls')
    K_RIGHT = b'M'
    K_LEFT  = b'K'
    K_UP    = b'H'
    K_DOWN  = b'P'
    K_ENTER = b'\r'
    K_Q     = b'q'
    K_B     = b'b'
    K_Y     = b'y'
    K_N     = b'n'
else:
    def clear_console():
        os.system('clear')
    K_RIGHT = b'[C'
    K_LEFT  = b'[D'
    K_UP  = b'[A'
    K_DOWN  = b'[B'
    K_ENTER = b'???'
    K_Q     = b'???'
    K_B     = b'???'


def read_key():
    try:
        # POSIX system: Create and return a getch that manipulates the tty
        import termios
        import sys, tty
        def getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

        # Read arrow keys correctly
        def getKey():
            firstChar = getch()
            return firstChar

    except ImportError:
        # Non-POSIX: Return msvcrt's (Windows') getch
        from msvcrt import getch

        # Read arrow keys correctly
        def getKey():
            input_char = getch()
            if input_char == b'\x00':
                input_char = getch()
            return input_char

    return getKey()

def get_casual_input(possible_options: List[bytes]) -> bytes:
    key = b""
    while key not in possible_options:
        key = read_key()
    return key


def get_selection_input() -> bytes:
    return get_casual_input([K_UP, K_DOWN, K_ENTER, K_B, K_Q])


def get_yes_no_input() -> bytes:
    return get_casual_input([K_Y, K_N])