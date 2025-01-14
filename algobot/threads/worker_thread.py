"""
Worker thread file used for basic threading operations across the GUI.
"""

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

import algobot


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    restore = pyqtSignal()
    started = pyqtSignal()
    finished = pyqtSignal(object)
    error = pyqtSignal(str)


class Worker(QRunnable):
    """
    Worker thread inherited from QRunnable to handler worker thread setup, signals and wrap-up.

    :param function: The function callback to run on this worker thread. Supplied args and kwargs will be passed through
      to the runner.
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """
    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        try:
            self.signals.started.emit()
            result = self.function(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            algobot.MAIN_LOGGER.exception(repr(e))
            self.signals.error.emit(str(e))
        finally:
            self.signals.restore.emit()
