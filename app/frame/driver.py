from PySide6.QtCore import QThread, Signal
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager


class ChromeDriver(QThread):
    finished = Signal(dict)

    def run(self):
        try:
            chrome = ChromeDriverManager().install()
            self.finished.emit({"Chrome": chrome})
        except:
            self.finished.emit({"Chrome": 0})


class EdgeDriver(QThread):
    finished = Signal(dict)

    def run(self):
        try:
            edge = EdgeChromiumDriverManager().install()
            self.finished.emit({"Edge": edge})
        except:
            self.finished.emit({"Edge": 0})


class FirefoxDriver(QThread):
    finished = Signal(dict)

    def run(self):
        try:
            firefox = GeckoDriverManager().install()
            self.finished.emit({"Firefox": firefox})
        except:
            self.finished.emit({"Firefox": 0})


class IEDriver(QThread):
    finished = Signal(dict)

    def run(self):
        try:
            ie = IEDriverManager().install()
            self.finished.emit({"IE": ie})
        except:
            self.finished.emit({"IE": 0})


class OperaDriver(QThread):
    finished = Signal(dict)

    def run(self):
        try:
            opera = OperaDriverManager().install()
            self.finished.emit({"Opera": opera})
        except:
            self.finished.emit({"Opera": 0})