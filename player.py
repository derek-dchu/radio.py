__author__ = 'DerekHu'

import time
import subprocess
from asyncproc import Process
import threading
try:
    from shlex import quote
except ImportError:  # Python < 3.3
    from pipes import quote


class MPC(object):

    def __init__(self, timeout=15):
        self.timeout = timeout
        command = ['mpc', '-q']
        self.p = Process(command)
        self.t = None
        self.write_lock = threading.Lock()

    def _send_command(self, command, *args):
        """Send a command to mpc's stdin in a thread safe way. The function
        handles all necessary locking and automatically handles line breaks and
        string formatting.

        Args:
            command:
                The basic mpc command, like "play" or "add", without
                a newline character.  This can contain new-style string
                formatting syntax like ``{}``.
            *args:
                Provide as many formatting arguments as you like. They are
                automatically ``quote()``d for security and passed to the
                string formatting function (printf-style).

        """
        with self.write_lock:
            safe_args = [quote(str(arg)) for arg in args]
            self.p.write(command.format(*safe_args) + '\n')

    def _stop_background_thread(self, blocking=True):
        """Abort the background thread by setting the ``self.t_stop`` event. If
        ``blocking`` is set, wait for it to finish."""
        if self.t is not None and self.t.is_alive():
            self.t_stop.set()
            if blocking:
                self.t.join()

    ## Add a stream url and play it
    def add(self, streamurl):
        self._stop_background_thread()

        self._send_command('add {}', streamurl)
        return self.p.read()

    def stop(self):
        """Stop playback."""
        self._send_command('clear')
        self._stop_background_thread()

    def terminate(self):
        """Shut down mpc and replace the reference to the async process
        with a dummy instance that raises a :class:`RuntimeError` on any method
        call."""
        if hasattr(self, 'p') and hasattr(self.p, 'terminate'):
            self._stop_background_thread()
            self.p.terminate()
            self.p = None

    def __del__(self):
        """Destructor. Calls ``self.terminate()``."""
        self.terminate()