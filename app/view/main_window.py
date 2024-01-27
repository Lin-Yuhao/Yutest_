# coding: utf-8
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import NavigationItemPosition, SplashScreen, MSFluentWindow, HorizontalSeparator, InfoBar, \
    InfoBarPosition, setCustomStyleSheet, StateToolTip
from qfluentwidgets import FluentIcon as FIF

from .projectmanage_interface import ProjectManage
from .uitestmanage_interface import UiTestManage
from .setting_interface import SettingInterface
from ..common.config import cfg
from ..common.translator import Translator
from ..common import resource


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        self._selectedModules = None

        self.stateTooltip = StateToolTip(title='正在加载浏览器驱动', content='加载中...', parent=self)
        self.stateTooltip.closeButton.hide()
        self.stateTooltip.move(20, 20)
        self.stateTooltip.show()

        self.projectManageInterface = ProjectManage(self)
        self.uiTestManageInterface = UiTestManage(self)

        self.ioTestManageInterface = QWidget(self)
        self.ioTestManageInterface.setObjectName('ioTestManageInterface')
        self.perforTestManageInterface = QWidget(self)
        self.perforTestManageInterface.setObjectName('perforTestManageInterface')
        self.autoTestManageInterface = QWidget(self)
        self.autoTestManageInterface.setObjectName('autoTestManageInterface')
        self.settingInterface = SettingInterface(self)

        self.separator = HorizontalSeparator()

        self.initNavigation()
        self.splashScreen.finish()

        self.selectedModulesTip = InfoBar(title=f'模块:{str(self._selectedModules)}', content="", isClosable=True,
                                          position=InfoBarPosition.TOP,
                                          duration=-1, parent=self, icon=FIF.PIN)
        # print(self.selectedModulesTip.children())
        self.selectedModulesTip.setStyleSheet("")
        qss = 'QFrame{background-color: rgba(0,0,0,0);border: 0px solid white}'
        setCustomStyleSheet(self.selectedModulesTip, qss, qss)
        self.selectedModulesTip.contentLabel.hide()
        self.selectedModulesTip.close()
        self.selectedModulesTip.closeButton.clicked.connect(self.closeMode)
        self.setSelectedModules(None, None)

    def closeMode(self):
        self.setSelectedModules(None, None)
        self.switchTo(self.projectManageInterface)

    def initNavigation(self):
        t = Translator()
        self.addSubInterface(self.projectManageInterface, FIF.TILES, self.tr('项目管理'))
        self.addSubInterface(self.uiTestManageInterface, FIF.CALENDAR, self.tr('UI测试'))
        self.addSubInterface(self.ioTestManageInterface, FIF.CODE, self.tr('接口测试'))
        self.addSubInterface(self.perforTestManageInterface, FIF.SPEED_HIGH, self.tr('性能测试'))
        self.addSubInterface(self.autoTestManageInterface, FIF.UPDATE, self.tr('自动化'))
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('设置'),
                             position=NavigationItemPosition.BOTTOM)

    def getSelectedModules(self):
        return self._selectedModules

    def setSelectedModules(self, modules_id, modules_name):
        self._selectedModules = (modules_id, modules_name)
        self.selectedModulesTip.title = f'模块：{str(self._selectedModules[1])}'
        if self._selectedModules[1]:
            self.selectedModulesTip.show()
            self.navigationInterface.items['projectManageInterface'].setEnabled(False)
            self.navigationInterface.items['uiTestManageInterface'].setEnabled(True)
            self.navigationInterface.items['ioTestManageInterface'].setEnabled(True)
            self.navigationInterface.items['perforTestManageInterface'].setEnabled(True)
            self.navigationInterface.items['autoTestManageInterface'].setEnabled(True)
        else:
            self.selectedModulesTip.hide()
            self.navigationInterface.items['projectManageInterface'].setEnabled(True)
            self.navigationInterface.items['uiTestManageInterface'].setEnabled(False)
            self.navigationInterface.items['ioTestManageInterface'].setEnabled(False)
            self.navigationInterface.items['perforTestManageInterface'].setEnabled(False)
            self.navigationInterface.items['autoTestManageInterface'].setEnabled(False)

    def initWindow(self):
        self.resize(900, 600)
        self.setMinimumWidth(760)
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())
