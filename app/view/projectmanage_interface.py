# coding:utf-8
from random import random

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QStackedWidget
from qfluentwidgets import (FluentIcon, FlowLayout, SmoothScrollArea, ToolButton, SubtitleLabel,
                            TitleLabel, ProgressBar, MessageBoxBase, LineEdit, InfoBar, InfoBarPosition,
                            RoundMenu, Action, MenuAnimationType, CardWidget, setCustomStyleSheet,
                            TabBar, TabCloseButtonDisplayMode, PushButton, StrongBodyLabel)

from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class CustomMessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.addItmeInterface = QFrame(self)
        self.viewLayout.addWidget(self.addItmeInterface)

        self.batchLayout = QVBoxLayout()
        self.batchLayout.setSpacing(10)
        self.batchLayout.setSpacing(15)
        self.batchLayout.setContentsMargins(0, 0, 0, 0)
        self.addItmeInterface.setLayout(self.batchLayout)

        self.Title = SubtitleLabel()
        self.Title.setText('添加项目')
        self.projectName = LineEdit(self)
        self.projectName.setPlaceholderText('项目名称')
        self.projectName.setClearButtonEnabled(True)

        self.addItmeInterface.layout().addWidget(self.Title)
        self.addItmeInterface.layout().addWidget(self.projectName)

        self.yesButton.setText('添加')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.projectName.textChanged.connect(self._validateUrl)

    def _validateUrl(self):
        dormText = self.projectName.text()
        self.yesButton.setEnabled(not not dormText)


class IconCardView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tabCount = 1

        self.db = None
        self.db_connect()

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.stackedWidget.setStyleSheet("background-color: rgba(0,0,0,0);border: 0px solid white;")

        self.windowMask = QWidget(self)
        self.windowMask.setStyleSheet(f'background:rgba(39, 39, 39, 1);border-radius: 20px;')
        icon = PushButton()
        icon.setText("添加项目")
        icon.setIcon(FluentIcon.ADD.icon(color='#BDBDBD'))
        layout = QVBoxLayout(self.windowMask)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)
        icon.clicked.connect(self.addTab)

        self.__initialTab()
        self.__initWidget()

    def resizeEvent(self, e):
        self.windowMask.resize(self.size())

    def db_connect(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./yutest.db')
        self.db.setUserName('root')
        self.db.setPassword('xl123')
        if not self.db.open():
            QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())
        query = QSqlQuery(self.db)
        query.exec("""
            CREATE TABLE IF NOT EXISTS projects (  
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                project_name TEXT NOT NULL UNIQUE  
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS modules (  
                module_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                module_name TEXT NOT NULL,  
                project_id INTEGER,  
                FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS test_case (
                test_case_id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_case_name TEXT NOT NULL,
                module_id INTEGER,
                data TEXT,
                config TEXT,
                FOREIGN KEY(module_id) REFERENCES modules(module_id)
            )
        """)

    def __initWidget(self):
        self.__initLayout()
        self.tabBar.setScrollable(True)
        self.tabBar.setTabShadowEnabled(True)
        self.tabBar.setTabSelectedBackgroundColor(QColor(243, 243, 243), QColor(32, 32, 32))
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.tabCloseRequested.connect(self.removeTab)
        self.__initialData()

    def __initialData(self):
        projectQuery = QSqlQuery(self.db)
        if projectQuery.exec("SELECT project_id, project_name FROM projects"):
            while projectQuery.next():
                scrollArea = SmoothScrollArea(self)
                flowLayout = FlowLayout(scrollArea, needAni=False)
                flowLayout.setVerticalSpacing(8)
                flowLayout.setHorizontalSpacing(8)
                flowLayout.setContentsMargins(10, 10, 10, 10)
                modulesQuery = QSqlQuery(self.db)
                modulesQuery.prepare("SELECT module_id, module_name, project_id FROM modules WHERE project_id = :project_id")
                modulesQuery.bindValue(':project_id', projectQuery.value(0))
                if modulesQuery.exec():
                    while modulesQuery.next():
                        self.addItem(flowLayout, modulesQuery.value(0), modulesQuery.value(1), modulesQuery.value(2))
                self.addModuleBtn(flowLayout)
                self.addSubInterface(scrollArea, str(projectQuery.value(0)), projectQuery.value(1))
            self.__initialTab()

    def addItem(self, flowLayout, modules_id, modules_name, project_id):
        card = CardWidget(self)
        card.setMinimumSize(196, 110)
        card.setObjectName(f'card_{modules_id}')
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        card.setLayout(layout)
        card.setBorderRadius(5)
        Titlelabel = TitleLabel()
        Titlelabel.setText(f"{modules_name}")
        Titlelabel.setFont(QFont("黑体", 22))
        Titlelabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ran = random()
        # gress = ProgressBar()
        # gress.setValue(min(int(ran * 100), 100))
        # gress.setUseAni(False)

        # if ran > 0.7:
        #     gress.setCustomBarColor(QColor(255, 48, 48), QColor(255, 48, 48))
        # elif 0.7 > ran > 0.5:
        #     gress.setCustomBarColor(QColor(255, 99, 71), QColor(255, 99, 71))
        # elif 0.5 > ran > 0.3:
        #     gress.setCustomBarColor(QColor(0, 191, 255), QColor(0, 191, 255))
        # else:
        #     gress.setCustomBarColor(QColor(30, 144, 255), QColor(30, 144, 255))

        layout.addWidget(Titlelabel)
        # layout.addWidget(gress)
        card.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        card.customContextMenuRequested.connect(lambda event: self.showCustomContextMenu(event, card, modules_id, modules_name, project_id))
        card.mouseDoubleClickEvent = lambda event: self.editMode(modules_id, modules_name, 0)
        flowLayout.addWidget(card)

    def __initLayout(self):
        self.tabBar.setTabMaximumWidth(150)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

    def __initialTab(self):
        if (len(self.tabBar.itemMap)) <= 0:
            self.windowMask.show()
        else:
            self.windowMask.hide()

    def addModuleBtn(self, layout: FlowLayout):
        icon = ToolButton(FluentIcon.ADD.icon(color='#BDBDBD'))
        icon.clicked.connect(lambda: self.addModule(layout))
        icon.setMinimumSize(200, 110)
        layout.addWidget(icon)

    def removeModule(self, card, modules_id, modules_name, project_id):
        tip = CustomMessageBox(self)
        tip.Title.setText('删除模块')
        tip.projectName.hide()
        tip.yesButton.setEnabled(True)
        tip.yesButton.setText('删除')
        qss = '''
            PushButton{background-color: #E53935; border-color: #E53935; color: #FFFFFF}
            PushButton::hover{background-color: #EF5350; border-color: #EF5350}
        '''
        setCustomStyleSheet(tip.yesButton, qss, qss)

        if tip.exec():
            card.parent().layout().takeAllWidgets()
            modulesQuery = QSqlQuery(self.db)
            modulesQuery.prepare("SELECT module_id, module_name FROM modules WHERE project_id = :project_id")
            modulesQuery.bindValue(':project_id', project_id)
            projectsQuery = QSqlQuery(self.db)
            projectsQuery.prepare("DELETE FROM modules WHERE module_id = :id")
            projectsQuery.bindValue(":id", modules_id)
            if projectsQuery.exec():
                if modulesQuery.exec():
                    while modulesQuery.next():
                        self.addItem(card.parent().layout(), modulesQuery.value(0), modulesQuery.value(1), project_id)
            self.addModuleBtn(card.parent().layout())

    def addModule(self, flowLayout):
        tip = CustomMessageBox(self)
        tip.Title.setText('添加模块')
        tip.projectName.setPlaceholderText("模块名称")
        if tip.exec():
            query = QSqlQuery(self.db)
            query.prepare("INSERT INTO modules (module_name, project_id) VALUES (:name, :project_id)")
            query.bindValue(":name", tip.projectName.text())
            query.bindValue(":project_id", self.tabBar.currentTab().routeKey())
            if query.exec():
                self.addItem(flowLayout, query.lastInsertId(), tip.projectName.text(), self.tabBar.currentTab().routeKey())
                flowLayout.removeWidget(flowLayout.parent().findChild(ToolButton))
                flowLayout.parent().findChild(ToolButton).deleteLater()
                self.addModuleBtn(flowLayout)

    def showCustomContextMenu(self, event, card, modules_id, modules_name, project_id):
        menu = RoundMenu(self)
        editSubmenu = RoundMenu("编辑", self)
        editSubmenu.setIcon(FIF.EDIT)
        editSubmenu.addActions([
            Action(FIF.CALENDAR, 'UI测试'),
            Action(FIF.CODE, '接口测试'),
            Action(FIF.SPEED_HIGH, '性能测试')
        ])
        editSubmenu.actions()[0].triggered.connect(lambda: self.editMode(modules_id, modules_name, 0))
        editSubmenu.actions()[1].triggered.connect(lambda: self.editMode(modules_id, modules_name, 1))
        editSubmenu.actions()[2].triggered.connect(lambda: self.editMode(modules_id, modules_name, 2))
        menu.addMenu(editSubmenu)
        # menu.addSeparator()
        playSubmenu = RoundMenu("运行", self)
        playSubmenu.setIcon(FIF.PLAY)
        playSubmenu.addActions([
            Action(FIF.PLAY_SOLID, 'UI自动化'),
            Action(FIF.PLAY_SOLID, '接口自动化'),
        ])
        menu.addMenu(playSubmenu)
        menu.addAction(Action(FIF.DELETE, '删除模块'))
        # menu.actions()[0].triggered.connect(lambda: self.selectDormitory(dormitory_name))
        # menu.actions()[1].triggered.connect(lambda: self.selectRepair(dormitory_name))
        # menu.actions()[2].triggered.connect(lambda: self.reviseBedNub(dormitory_name))
        menu.actions()[0].triggered.connect(lambda: self.removeModule(card, modules_id, modules_name, project_id))
        menu.exec(card.mapToGlobal(event), aniType=MenuAnimationType.DROP_DOWN)

    def editMode(self, modules_id, modules_name, index):
        mainWindow = self.parent().parent().parent().parent().parent().parent()
        mainWindow.setSelectedModules(modules_id, modules_name)
        mainWindow.uiTestManageInterface.initData(modules_id)
        if index == 0:
            mainWindow.switchTo(mainWindow.uiTestManageInterface)
        elif index == 1:
            mainWindow.switchTo(mainWindow.ioTestManageInterface)
        elif index == 2:
            mainWindow.switchTo(mainWindow.perforTestManageInterface)

    def addTab(self):
        tip = CustomMessageBox(self)
        if tip.exec():
            text = tip.projectName.text()
            query = QSqlQuery(self.db)
            query.prepare("INSERT INTO projects (project_name) VALUES (:name)")
            query.bindValue(":name", text)
            if query.exec():
                scrollArea = SmoothScrollArea(self)
                flowLayout = FlowLayout(scrollArea, needAni=False)
                flowLayout.setVerticalSpacing(8)
                flowLayout.setHorizontalSpacing(8)
                flowLayout.setContentsMargins(10, 10, 10, 10)
                self.addSubInterface(scrollArea, str(query.lastInsertId()), text)
                self.addModuleBtn(flowLayout)
                self.__initialTab()
            else:
                InfoBar.warning(title='重复输入', content="", isClosable=False, position=InfoBarPosition.BOTTOM_RIGHT,
                                duration=4000, parent=self)

    def removeTab(self, index):
        tip = CustomMessageBox(self)
        tip.yesButton.setText('删除')
        tip.projectName.hide()
        tip.Title.setText('删除项目')
        label = StrongBodyLabel()
        label.setText('将会删除相关联模块')
        tip.addItmeInterface.layout().addWidget(label)
        qss = '''
                PushButton{background-color: #E53935; border-color: #E53935; color: #FFFFFF}
                PushButton::hover{background-color: #EF5350; border-color: #EF5350}
                '''
        setCustomStyleSheet(tip.yesButton, qss, qss)
        tip.yesButton.setEnabled(True)
        if tip.exec():
            projectsQuery = QSqlQuery(self.db)
            projectsQuery.prepare("DELETE FROM projects WHERE project_id = :id")
            projectsQuery.bindValue(":id", self.tabBar.items[index].routeKey())
            if projectsQuery.exec():
                modulesQuery = QSqlQuery(self.db)
                modulesQuery.prepare("DELETE FROM modules WHERE project_id = :id")
                modulesQuery.bindValue(":id", self.tabBar.items[index].routeKey())
                if modulesQuery.exec():
                    item = self.tabBar.tabItem(index)
                    widget = self.findChild(SmoothScrollArea, item.routeKey())
                    self.stackedWidget.removeWidget(widget)
                    self.tabBar.removeTab(index)
                    widget.deleteLater()
                    self.__initialTab()

    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )


class ProjectManage(GalleryInterface):
    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.icons,
            subtitle="qfluentwidgets.common.icon",
            parent=parent
        )
        self.setObjectName('projectManageInterface')

        self.iconView = IconCardView(self)
        self.vBoxLayout.addWidget(self.iconView)
