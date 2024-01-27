# coding:utf-8
import json

from PySide6.QtCore import Qt, QPoint, QMimeData, QByteArray, Slot
from PySide6.QtGui import QColor, QCursor, QDrag
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QFrame, QMessageBox, QVBoxLayout, QSpacerItem, QApplication, QSizePolicy
from qfluentwidgets import (FluentIcon as FIF, Action, PushButton, setCustomStyleSheet, SimpleCardWidget,
                            MessageBoxBase,
                            SubtitleLabel, LineEdit, RoundMenu, HorizontalSeparator, TransparentTogglePushButton,
                            TableWidget, isDarkTheme, IndeterminateProgressRing, InfoBarPosition)
from qfluentwidgets.components.settings.expand_setting_card import HeaderSettingCard
from qfluentwidgetspro import ToolBox, Toast

from ..common.icon import Icon
from ..frame.uiTest import UiTest
from ..frame.driver import ChromeDriver, EdgeDriver, FirefoxDriver, IEDriver
from ..interface.ui_TestManageInterface import Ui_Frame
from ..common.style_sheet import StyleSheet
from ..components.nodeView import NodeView, ListItem


class CustomMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Title = SubtitleLabel()
        self.caseLineEdit = LineEdit(self)
        self.caseLineEdit.setPlaceholderText('用例名称')
        self.viewLayout.addWidget(self.Title)
        self.viewLayout.addWidget(self.caseLineEdit)
        self.viewLayout.setSpacing(15)
        self.yesButton.setText('添加')
        self.cancelButton.setText('取消')
        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.caseLineEdit.textChanged.connect(self._validateUrl)

    def _validateUrl(self):
        self.yesButton.setEnabled(self.caseLineEdit.text() is not None)


class UiTestManage(Ui_Frame, QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName('uiTestManageInterface')

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./yutest.db')
        self.db.setUserName('root')
        self.db.setPassword('xl123')
        if not self.db.open():
            QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())

        self.lastSelecdCase = None
        self.dragData = None
        self.insertData = None
        self.drag_start_position = None
        self.selecedNode = None
        self.lastDelete = None
        self.lastDeleteRow = None
        self.dragValue = None
        self.yesButton = None
        self.butdrag = None
        self.nodeView = NodeView(self.db)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.nodeView)
        self.scrollAreaWidgetContents.setLayout(layout)
        self.SmoothScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents.setAcceptDrops(True)
        self.scrollAreaWidgetContents.mousePressEvent = self.nodeMousePressEvent
        self.scrollAreaWidgetContents.mouseMoveEvent = self.nodeMouseMoveEvent
        self.scrollAreaWidgetContents.dragEnterEvent = self.onDragEnterEvent
        self.scrollAreaWidgetContents.dragMoveEvent = self.onDragMoveEvent
        self.scrollAreaWidgetContents.dragLeaveEvent = self.onDragLeaveEvent
        self.scrollAreaWidgetContents.dropEvent = self.onDropEvent

        self.uiThread = UiTest()
        self.uiThread.finished.connect(self.on_thread_finished)
        self.uiThread.errorrow.connect(self.on_thread_errorrow)
        self.uiThread.errorbrowser.connect(self.on_thread_errorbrowser)

        self.chromedrivermanager = ChromeDriver()
        self.edgedrivermanager = EdgeDriver()
        self.firefoxdrivermanager = FirefoxDriver()
        self.iedrivermanager = IEDriver()

        self.chromedrivermanager.finished.connect(self.on_driver_finished)
        self.edgedrivermanager.finished.connect(self.on_driver_finished)
        self.firefoxdrivermanager.finished.connect(self.on_driver_finished)
        self.iedrivermanager.finished.connect(self.on_driver_finished)

        self.chromedrivermanager.start()
        self.edgedrivermanager.start()
        self.firefoxdrivermanager.start()
        self.iedrivermanager.start()

        self.drivelist = {}

        self.__inteWindow()
        self.__initCommandBar()
        self.CommandBar.actions()[0].setEnabled(False)
        self.SimpleCardWidget_2.setEnabled(False)

    @Slot(dict)
    def on_driver_finished(self, message):
        self.drivelist.update(message)
        if len(self.drivelist) == 4:
            path = []
            for key, value in self.drivelist.items():
                path.append(value)
                if value != 0:
                    self.TransparentComboBox.addItem(key)

            stateTooltip = self.parent().parent().parent().stateTooltip
            if all(x == 0 for x in path):
                stateTooltip.setTitle('请检查网络连接')
                stateTooltip.setContent('未找到浏览器驱动')
                stateTooltip.rotateTimer.stop()
                stateTooltip.closeButton.show()
                qss = "QWidget{background-color: rgba(255,0,0,1)}"
                setCustomStyleSheet(stateTooltip, qss, qss)
            else:
                stateTooltip.setContent('加载完成')
                stateTooltip.setState(True)
                stateTooltip = None
                self.CommandBar.actions()[0].setEnabled(True)

    def start_thread(self):
        if self.nodeView.item.itemData:
            if not self.uiThread.isRunning():
                for key, value in self.drivelist.items():
                    if key == self.TransparentComboBox.currentText():
                        self.uiThread.datapath = {key: value}

                self.uiThread.data = self.nodeView.item.itemData
                self.uiThread.config = [int(self.ghost.isChecked()), int(self.lazy.isChecked())]
                self.uiThread.stop_event = False
                self.uiThread.start()

                run = MessageBoxBase(self)
                run.viewLayout.setContentsMargins(20, 20, 20, 20)
                run.viewLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                run.setStyleSheet(f'background:rgba(0, 0, 0, 0)')
                run.viewLayout.addWidget(IndeterminateProgressRing())
                run.cancelButton.hide()
                run.buttonLayout.setContentsMargins(0, 0, 0, 0)
                run.buttonGroup.setContentsMargins(0, 0, 0, 0)
                run.buttonGroup.setFixedHeight(32)
                run.yesButton.setText('中止')
                self.yesButton = run.yesButton
                c = 0 if isDarkTheme() else 255
                run.windowMask.setStyleSheet(f'background:rgba({c}, {c}, {c}, 0.5)')
                if run.exec():
                    pass
        else:
            Toast.info(
                title='无操作',
                content=self.tr(""),
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

    @Slot(str)
    def on_thread_errorbrowser(self, message):
        Toast.error(
            title='未发现浏览器驱动',
            content=self.tr(""),
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
        pass

    @Slot(int)
    def on_thread_errorrow(self, row):
        item = self.nodeView._items[row].widget()
        if isinstance(item, SimpleCardWidget):
            item.setBackgroundColor(QColor(104, 43, 44))
        self.yesButton.click()

    @Slot(str)
    def on_thread_finished(self, message):
        Toast.success(
            title='用例完成',
            content=self.tr(""),
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
        self.yesButton.click()

    def nodeMousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            item = self.scrollAreaWidgetContents.childAt(event.pos())
            if item:
                while not (isinstance(item, SimpleCardWidget) or isinstance(item, ToolBox)):
                    item = item.parent()
                self.selecedNode = self.nodeView.indexOf(item)
                self.lastDeleteRow = None

    def nodeMouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        if self.selecedNode is not None:
            item = self.scrollAreaWidgetContents.childAt(event.pos())
            if item:
                byte_array = QByteArray(''.encode('utf-8'))
                mime_data = QMimeData()
                mime_data.setData("text/plain", byte_array)
                drag = QDrag(self)
                drag.setMimeData(mime_data)
                drag.exec_(Qt.DropAction.CopyAction)

    def onDragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/json'):
            insertData = self.lastSelecdCase.itemData.copy()
            insertData.insert(len(insertData), {"insertCard": []})
            self.nodeView.changeData(insertData)
            event.accept()
        if event.mimeData().hasFormat('text/plain'):
            if self.lastDeleteRow is not None:
                dragData = self.lastSelecdCase.itemData.copy()
                dragData.insert(self.lastDeleteRow, self.lastDelete)
                self.dragValue = dragData
                self.nodeView.changeData(dragData)
                self.lastSelecdCase.itemData = dragData
            event.accept()

    def onDragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/json'):
            byte_array = event.mimeData().data('application/json')
            json_str = byte_array.data().decode('utf-8')
            data_dict = json.loads(json_str)
            item = self.scrollAreaWidgetContents.childAt(event.pos())
            if item and (isinstance(item, SimpleCardWidget) or isinstance(item, HeaderSettingCard)):
                for index in range(len(self.nodeView._items)):
                    while not (isinstance(item, SimpleCardWidget)):
                        item = item.parent()
                    if self.nodeView._items[index].widget() == item:
                        itemIndex = index
                        dragData = self.lastSelecdCase.itemData.copy()
                        insertData = self.lastSelecdCase.itemData.copy()
                        dragData.insert(itemIndex, data_dict)
                        insertData.insert(itemIndex, {"insertCard": []})
                        if self.insertData != insertData:
                            self.nodeView.changeData(insertData)
                        self.dragData = dragData
                        self.insertData = insertData
            elif len(self.nodeView._items) == 0:
                if self.lastSelecdCase.itemData:
                    dragData = self.lastSelecdCase.itemData.copy()
                    dragData.insert(0, data_dict)
                    insertData = self.lastSelecdCase.itemData.copy()
                    insertData.insert(0, {"insertCard": []})
                    self.nodeView.changeData(insertData)
                    self.dragData = dragData
                else:
                    dragData = []
                    dragData.insert(0, data_dict)
                    insertData = []
                    insertData.insert(0, {"insertCard": []})
                    self.nodeView.changeData(insertData)
                    self.dragData = dragData
        if event.mimeData().hasFormat('text/plain'):
            index = self.selecedNode
            moveitem = self.scrollAreaWidgetContents.childAt(event.pos())
            dragData = self.lastSelecdCase.itemData.copy()
            if moveitem and self.selecedNode != moveitem:
                while not (isinstance(moveitem, SimpleCardWidget)):
                    moveitem = moveitem.parent()
                moveindex = self.nodeView.indexOf(moveitem)
                if dragData and moveindex != -1 and index != -1:
                    dragData[index], dragData[moveindex] = dragData[moveindex], dragData[index]
                    self.lastSelecdCase.itemData = dragData
                    example = dragData.copy()
                    example[moveindex] = {"insertCardExample": []}
                    self.nodeView.changeData(example)
                    query = QSqlQuery(self.db)
                    query.prepare("UPDATE test_case SET data = :new_data WHERE test_case_id = :test_case_id")
                    query.bindValue(":test_case_id", self.ListWidget.currentItem().testCaseId)
                    query.bindValue(":new_data", json.dumps(self.lastSelecdCase.itemData))
                    query.exec()
                self.selecedNode = moveindex

    def onDragLeaveEvent(self, event):
        if self.selecedNode is not None:
            dragData = self.lastSelecdCase.itemData.copy()
            if dragData:
                self.lastDelete = dragData[self.selecedNode]
                self.lastDeleteRow = self.selecedNode
                dragData.pop(self.selecedNode)
                self.nodeView.changeData(dragData)
                self.lastSelecdCase.itemData = dragData
                query = QSqlQuery(self.db)
                query.prepare("UPDATE test_case SET data = :new_data WHERE test_case_id = :test_case_id")
                query.bindValue(":test_case_id", self.ListWidget.currentItem().testCaseId)
                query.bindValue(":new_data", json.dumps(dragData))
                query.exec()
        else:
            self.nodeView.changeData(self.lastSelecdCase.itemData)
            self.butdrag = False

    def onDropEvent(self, event):
        self.selecedNode = None
        if event.mimeData().hasFormat('application/json'):
            self.lastSelecdCase.itemData = self.dragData
            self.nodeView.changeData(self.dragData)
            query = QSqlQuery(self.db)
            query.prepare("UPDATE test_case SET data = :new_data WHERE test_case_id = :test_case_id")
            query.bindValue(":test_case_id", self.ListWidget.currentItem().testCaseId)
            query.bindValue(":new_data", json.dumps(self.dragData))
            query.exec()
            event.accept()
        if event.mimeData().hasFormat('text/plain'):
            dragData = self.lastSelecdCase.itemData.copy()
            self.nodeView.changeData(dragData)
            query = QSqlQuery(self.db)
            query.prepare("UPDATE test_case SET data = :new_data WHERE test_case_id = :test_case_id")
            query.bindValue(":test_case_id", self.ListWidget.currentItem().testCaseId)
            query.bindValue(":new_data", json.dumps(dragData))
            query.exec()
            event.accept()

    def initData(self, modules_id):
        self.ListWidget.clear()
        caseQuery = QSqlQuery(self.db)
        caseQuery.prepare(
            "SELECT test_case_id, test_case_name, data, config FROM test_case WHERE module_id = :modules_id")
        caseQuery.bindValue(':modules_id', modules_id)
        if caseQuery.exec():
            while caseQuery.next():
                item = ListItem(
                    text=caseQuery.value('test_case_name'),
                    testCaseId=caseQuery.value('test_case_id'),
                )
                item.itemData = json.loads(caseQuery.value('data'))
                item.config = json.loads(caseQuery.value('config'))
                self.ListWidget.addItem(item)

    def __inteWindow(self):
        self.SimpleCardWidget.layout().setSpacing(8)
        self.SimpleCardWidget.setEnabled(False)
        self.SimpleCardWidget_2.setEnabled(False)
        self.ListWidget.currentItemChanged.connect(self.dataChange)
        self.ListWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ListWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.ListWidget.itemSelectionChanged.connect(self.required)
        self.SmoothScrollArea.setStyleSheet("background-color: rgba(0,0,0,0);border: 0px solid white")
        self.TransparentPushButton.clicked.connect(self.addCase)
        self.TransparentPushButton.setText("添加用例")
        self.TransparentPushButton.setIcon(FIF.ADD.icon())

    def showContextMenu(self, pos: QPoint):
        item = self.ListWidget.itemAt(pos)
        self.ListWidget.setCurrentItem(item)
        if item:
            menu = RoundMenu(parent=self)
            menu.addActions([
                Action(FIF.DELETE, '删除'),
            ])
            menu.actions()[0].triggered.connect(lambda: self.removeTestCase(item))
            # menu.addSeparator()
            menu.exec(QCursor.pos())

    def removeTestCase(self, item: ListItem):
        tip = CustomMessageBox(self)
        tip.Title.setText('删除用例')
        tip.caseLineEdit.hide()
        tip.yesButton.setEnabled(True)
        tip.yesButton.setText('删除')
        qss = '''
            PushButton{background-color: #E53935; border-color: #E53935; color: #FFFFFF}
            PushButton::hover{background-color: #EF5350; border-color: #EF5350}
        '''
        setCustomStyleSheet(tip.yesButton, qss, qss)
        if tip.exec():
            query = QSqlQuery(self.db)
            query.prepare("DELETE FROM test_case WHERE test_case_id = :testCaseId")
            query.bindValue(":testCaseId", item.testCaseId)
            if query.exec():
                self.ListWidget.takeItem(self.ListWidget.currentIndex().row())

    def addCase(self):
        tip = CustomMessageBox(self)
        tip.Title.setText('添加用例')
        if tip.exec():
            query = QSqlQuery(self.db)
            query.prepare(
                "INSERT INTO test_case (test_case_name, data, config, module_id) VALUES (:test_case_name, :data, :config, :module_id)"
            )
            query.bindValue(":test_case_name", tip.caseLineEdit.text())
            query.bindValue(":module_id", self.parent().parent().parent().getSelectedModules()[0])
            query.bindValue(":data", json.dumps([]))
            query.bindValue(":config", json.dumps([0, 0, 0]))
            if query.exec():
                item = ListItem(text=tip.caseLineEdit.text(), testCaseId=query.lastInsertId())
                item.itemData = []
                item.config = [0, 0, 0]
                self.ListWidget.addItem(item)
                self.ListWidget.setCurrentItem(item)

    def dataChange(self, item):
        self.nodeView.item = item
        if self.nodeView.item:
            self.SimpleCardWidget.setEnabled(True)
            self.SimpleCardWidget_2.setEnabled(True)
            self.nodeView.changeData(item.itemData)
            data = item.config
            self.ghost.setChecked(data[0])
            self.lazy.setChecked(data[1])
        else:
            self.SimpleCardWidget.setEnabled(False)
            self.SimpleCardWidget_2.setEnabled(False)
            self.nodeView.takeAllWidgets()

    def __initCommandBar(self):
        self.CommandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.ghost = TransparentTogglePushButton()
        self.ghost.setText('幽灵模式')
        self.ghost.setIcon(Icon.GHOST.icon())
        # self.ghost.clicked.connect(self.changeParameter)
        self.lazy = TransparentTogglePushButton()
        self.lazy.setText('懒加载模式')
        self.lazy.setIcon(Icon.LAZY.icon())
        # self.lazy.clicked.connect(self.changeParameter)
        self.CommandBar.addWidget(self.ghost)
        self.CommandBar.addWidget(self.lazy)
        self.CommandBar.addActions([
            Action(FIF.PLAY, self.tr('运行')),
        ])

        self.CommandBar.actions()[0].triggered.connect(self.start_thread)

        but = [
            (Icon.URL, self.tr('访问'), {"operationOpen": ['']}),
            (FIF.LABEL, self.tr('点击'), {"operationClick": [0, '']}),
            (FIF.EDIT, self.tr('编辑'), {"operationEdit": [0, '', '']}),
            (FIF.DELETE, self.tr('清空'), {"operationClear": [0, '']}),
            0,
            (Icon.WINDOW, self.tr('窗口'), {"operationWindow": [0, 0]}),
            (Icon.WINDOWSIZE, self.tr('控制'), {"operationSize": [0]}),
            (Icon.TAB, self.tr('导航'), {"operationNav": [0]}),
            (Icon.ALERT, self.tr('弹窗'), {"operationAlert": [0]}),
            (Icon.COOKIE, self.tr('Cookies'), {"operationCookie": {}}),
            (Icon.FRAME, self.tr('Frames'), {"operationFrames": [0, '', 0]}),
            (Icon.JS, self.tr('JavaScript'), {"operationJS": ['']}),
        ]
        for i in but:
            if i:
                button = PushButton()
                button.setIcon(i[0].icon())
                button.setText(i[1])
                button.mousePressEvent = lambda e, data=i[2]: self.onMousePressEvent(e, data)
                button.mouseMoveEvent = lambda e, data=i[2]: self.onMouseMoveEvent(e, data)
                button.mouseReleaseEvent = lambda e, data=i[2]: self.onMouseReleaseEvent(e, data)
                self.SimpleCardWidget.layout().addWidget(button)
            else:
                self.SimpleCardWidget.layout().addWidget(HorizontalSeparator())
        self.SimpleCardWidget.layout().addItem(QSpacerItem(20, 40, QSizePolicy.Expanding))
        self.SimpleCardWidget.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

    def onMousePressEvent(self, event, data):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def onMouseMoveEvent(self, event, data):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        self.drag_start_position = event.pos()
        json_str = json.dumps(data)
        byte_array = QByteArray(json_str.encode('utf-8'))
        mime_data = QMimeData()
        mime_data.setData('application/json', byte_array)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.DropAction.CopyAction)

    def onMouseReleaseEvent(self, event, data):
        dragData = self.lastSelecdCase.itemData.copy()
        dragData.append(data)
        self.nodeView.changeData(dragData)
        self.lastSelecdCase.itemData = dragData

    def required(self):
        if self.ListWidget.selectedItems():
            self.lastSelecdCase = self.ListWidget.selectedItems()[0]
        else:
            if self.nodeView.item:
                self.ListWidget.setCurrentItem(self.lastSelecdCase)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        for i in (self.scrollAreaWidgetContents.findChildren(SimpleCardWidget)
                  + self.scrollAreaWidgetContents.findChildren(ToolBox)):
            i.setFixedWidth(self.SmoothScrollArea.width() - 20)

        for l in (self.scrollAreaWidgetContents.findChildren(TableWidget)):
            l.setFixedWidth(self.SmoothScrollArea.width() - 40)

    # def changeParameter(self):
    #     data = [int(self.ghost.isChecked()), int(self.lazy.isChecked())]
    #     self.lastSelecdCase.config = data
    #     query = QSqlQuery(self.db)
    #     query.prepare("UPDATE test_case SET config = :new_data WHERE test_case_id = :test_case_id")
    #     query.bindValue(":test_case_id", self.lastSelecdCase.testCaseId)
    #     query.bindValue(":new_data", json.dumps(data))
    #     query.exec()
