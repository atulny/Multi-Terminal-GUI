from threading import Thread


class PThread(Thread):
    # Daemon by default thus will not hold app open upon main thread closing
    def __init__(self, call_back, call_back_args, is_daemon=True):
        super().__init__(target=call_back, args=call_back_args, daemon=is_daemon)
