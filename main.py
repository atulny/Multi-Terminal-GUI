import time
import random

import log
from config import load_config
from window import Window


def _start():
    log.info("Started")


def _restart():
    log.info("Restarted")


def _stop():
    log.info("Stopped")


def main():
    wn = Window("GUI")
    wn.start(run_callback=_run, run_callback_args=(wn,))


def _run(wn):
    terminal_manager = wn.get_terminal_manger()

    for i in range(8):
        terminal_manager.add_terminal("Terminal: %d" % i)

    terminal_manager.set_terminal_attribute("Terminal: 0", "start_callback", _start)
    terminal_manager.set_terminal_attribute("Terminal: 0", "restart_callback", _restart)
    terminal_manager.set_terminal_attribute("Terminal: 0", "stop_callback", _stop)

    while True:
        i = random.randint(0, 7)
        terminal_manager.append_to_terminal("Terminal: %d" % i, "test" + str(i))
        terminal_manager.set_terminal_attribute("Terminal: %d" % i, "status", random.randint(0, 3))
        time.sleep(1/100)


if __name__ == '__main__':
    log.info("Loading Config Settings")
    load_config()
    log.info("Config Settings Loaded")

    log.init()

    main()
