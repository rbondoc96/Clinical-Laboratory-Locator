#pylint: disable=no-name-in-module

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

import traceback, sys

class SearchWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class SearchWorker(QRunnable):
    def __init__(self, obj, *args, **kwargs): 
        super(SearchWorker, self).__init__()

        self.object = obj
        self.args = args
        self.limit = kwargs.pop("limit", 100)
        self.kwargs = kwargs
        self.signals = SearchWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            search = self.object(*self.args, **self.kwargs)
            result = search.search(limit=self.limit)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit() 