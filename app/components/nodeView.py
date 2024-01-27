import json

import requests
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QListWidgetItem, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QHeaderView
from qfluentwidgets import FluentIcon as FIF, FlowLayout, SimpleCardWidget, Action, LineEdit, \
    IconWidget, SegmentedWidget, TableWidget, RoundMenu, MenuAnimationType, CompactSpinBox, TextEdit, InfoLevel

from qfluentwidgetspro import TransparentComboBox, RoundedRectSkeletonItem, Skeleton, ToolBox, FilledToolButton

from app.common.icon import Icon
from app.components.jsHighlighter import JsHighlighter


class GetLocation(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.url = None

    def run(self):
        if self.url:
            try:
                requests.get(self.url)
            except Exception as e:
                self.error.emit('error')
            else:
                self.finished.emit('finished')
        else:
            self.error.emit('error')

class ListItem(QListWidgetItem):
    def __init__(self, text=None, data=None, testCaseId=None, config=None):
        super().__init__()
        self.setText(text)
        self.itemData = data
        self.testCaseId = testCaseId
        self.config = config


class NodeView(FlowLayout):
    def __init__(self, databese):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        self.item = None
        self.databese = databese
        self.lastdata = None

    def changeData(self, data=None):
        self.takeAllWidgets()
        if data:
            for item in range(len(data)):
                for key in data[item]:
                    if hasattr(self, key):
                        method = getattr(self, key)
                        if callable(method):
                            method(data[item][key])
                        else:
                            print(f"{key} is not a method in this class.")
                    else:
                        print(f"The method {key} does not exist in this class.")
        self.lastdata = data

    def addNode(self, data):
        if data:
            for key in data:
                if hasattr(self, key):
                    method = getattr(self, key)
                    if callable(method):
                        method(*data[key])
                        self.item.itemData.append(data)
                        query = QSqlQuery(self.databese)
                        query.prepare("UPDATE test_case SET data = :data WHERE test_case_id = :test_case_id")
                        query.bindValue(":test_case_id", self.item.testCaseId)
                        query.bindValue(":data", json.dumps(self.item.itemData))
                        query.exec()
                    else:
                        print(f"{key} is not a method in this class.")
                else:
                    print(f"The method {key} does not exist in this class.")

    def operationOpen(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Url = LineEdit()
        Url.setText(data[0])
        Url.setPlaceholderText('Url')
        Title = IconWidget()
        Title.setIcon(Icon.URL)
        Title.setFixedSize(20, 20)
        loadButton = FilledToolButton(FIF.QUESTION.icon())
        loadButton.setLevel(InfoLevel.INFOAMTION)
        loadButton.setFixedSize(32, 32)
        nodeCard.layout().addWidget(Title)
        nodeCard.layout().addWidget(Url)
        nodeCard.layout().addWidget(loadButton)

        thread = GetLocation()
        thread.finished.connect(lambda message: self.on_loadurl_finished(loadButton))
        thread.error.connect(lambda message: self.on_loadurl_error(loadButton))

        Url.editingFinished.connect(lambda: self.loadUrl(Url.text(), loadButton, thread))
        Url.editingFinished.connect(lambda: self.changeParameter(nodeCard, Url.text(), 0))
        nodeCard.setFixedSize(self.parent().parent().width()-20, 50)
        self.addWidget(nodeCard)

    def loadUrl(self, url, loadButton, thread):
        loadButton.setLevel(InfoLevel.ATTENTION)
        loadButton.setIcon(FIF.QUESTION.icon())
        thread.url = url
        thread.start()

    def on_loadurl_finished(self, loadButton):
        loadButton.setLevel(InfoLevel.SUCCESS)
        loadButton.setIcon(FIF.ACCEPT.icon())

    def on_loadurl_error(self, loadButton):
        loadButton.setLevel(InfoLevel.ERROR)
        loadButton.setIcon(FIF.CLOSE.icon())

    def operationClick(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(FIF.LABEL)
        Title.setFixedSize(20, 20)
        Mode = TransparentComboBox()
        Mode.setPrefix("定位策略:")
        Mode.addItems(['ID', 'Class名称', 'CSS选择器', 'Name', '链接文本', '部分链接文本', '标签名称', 'XPath'])
        Mode.setCurrentIndex(data[0])
        Locator = LineEdit()
        Locator.setPlaceholderText('定位')
        Locator.setText(data[1])
        nodeCard.layout().addWidget(Title)
        nodeCard.layout().addWidget(Mode)
        nodeCard.layout().addWidget(Locator)
        Mode.currentIndexChanged.connect(lambda: self.changeParameter(nodeCard, Mode.currentIndex(), 0))
        Locator.editingFinished.connect(lambda: self.changeParameter(nodeCard, Locator.text(), 1))
        nodeCard.setFixedSize(self.parent().parent().width()-20, 50)
        self.addWidget(nodeCard)

    def operationEdit(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(FIF.EDIT)
        Title.setFixedSize(20, 20)
        Mode = TransparentComboBox()
        Mode.setPrefix("定位策略:")
        Mode.addItems(['ID', 'Class名称', 'CSS选择器', 'Name', '链接文本', '部分链接文本', '标签名称', 'XPath'])
        Mode.setCurrentIndex(data[0])
        Locator = LineEdit()
        Locator.setPlaceholderText('定位')
        Locator.setText(data[1])
        Content = LineEdit()
        Content.setPlaceholderText('内容')
        Content.setText(data[2])
        nodeCard.layout().addWidget(Title)
        nodeCard.layout().addWidget(Mode)
        nodeCard.layout().addWidget(Locator)
        nodeCard.layout().addWidget(Content)
        Mode.currentIndexChanged.connect(lambda: self.changeParameter(nodeCard, Mode.currentIndex(), 0))
        Locator.editingFinished.connect(lambda: self.changeParameter(nodeCard, Locator.text(), 1))
        Content.editingFinished.connect(lambda: self.changeParameter(nodeCard, Content.text(), 2))
        nodeCard.setFixedSize(self.parent().parent().width()-20, 50)
        self.addWidget(nodeCard)

    def operationClear(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(FIF.DELETE)
        Title.setFixedSize(20, 20)
        Mode = TransparentComboBox()
        Mode.setPrefix("定位策略:")
        Mode.addItems(['ID', 'Class名称', 'CSS选择器', 'Name', '链接文本', '部分链接文本', '标签名称', 'XPath'])
        Mode.setCurrentIndex(data[0])
        Locator = LineEdit()
        Locator.setPlaceholderText('定位')
        Locator.setText(data[1])
        nodeCard.layout().addWidget(Title)
        nodeCard.layout().addWidget(Mode)
        nodeCard.layout().addWidget(Locator)
        Mode.currentIndexChanged.connect(lambda: self.changeParameter(nodeCard, Mode.currentIndex(), 0))
        Locator.editingFinished.connect(lambda: self.changeParameter(nodeCard, Locator.text(), 1))
        nodeCard.setFixedSize(self.parent().parent().width()-20, 50)
        self.addWidget(nodeCard)

    def operationWindow(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(Icon.WINDOW)
        Title.setFixedSize(20, 20)
        Mode = TransparentComboBox()
        Mode.setPrefix("操作")
        Mode.addItems(['新增标签', '新增窗口', '下标进入窗口', '关闭窗口'])
        Mode.setCurrentIndex(data[0])
        Index = CompactSpinBox()
        Index.setFixedWidth(100)
        Index.setValue(data[1])
        if Mode.currentIndex() != 2:
            Index.hide()
        nodeCard.layout().addWidget(Title)
        nodeCard.layout().addWidget(Mode)
        nodeCard.layout().addWidget(Index)
        Mode.currentIndexChanged.connect(lambda: self.modeChangeIndex(nodeCard, Mode, Index))
        Index.valueChanged.connect(lambda: self.changeParameter(nodeCard, Index.value(), 1))
        nodeCard.setFixedSize(self.parent().parent().width() - 20, 50)
        self.addWidget(nodeCard)

    def modeChangeIndex(self, nodeCard, mode, index):
        self.changeParameter(nodeCard, mode.currentIndex(), 0)
        if mode.currentIndex() == 2:
            index.show()
        else:
            index.hide()

    def operationSize(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(Icon.WINDOWSIZE)
        Title.setFixedSize(20, 20)
        nodeCard.layout().addWidget(Title)
        Tab = SegmentedWidget()
        Tab.addItem('MaxImize', '最大化', icon=Icon.MAXIMIZE.icon())
        Tab.addItem('FullScreen', '全屏', icon=Icon.FULLSCREEN.icon())
        Tab.addItem('MinImize', '最小化', icon=Icon.MINIMIZE.icon())
        Tab._currentRouteKey = list(Tab.items.keys())[data[0]]
        nodeCard.layout().addWidget(Tab)
        for i in Tab.items: Tab.items[i].itemClicked.connect(
            lambda: self.changeParameter(nodeCard, list(Tab.items.keys()).index(Tab._currentRouteKey), 0)
        )
        nodeCard.setFixedSize(self.parent().parent().width() - 20, 50)
        self.addWidget(nodeCard)

    def operationNav(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(Icon.TAB)
        Title.setFixedSize(20, 20)
        nodeCard.layout().addWidget(Title)
        Tab = SegmentedWidget()
        Tab.addItem('back', '后退', icon=FIF.LEFT_ARROW.icon())
        Tab.addItem('refresh', '刷新', icon=FIF.ROTATE.icon())
        Tab.addItem('forward', '前进', icon=FIF.RIGHT_ARROW.icon())
        Tab._currentRouteKey = list(Tab.items.keys())[data[0]]
        nodeCard.layout().addWidget(Tab)
        for i in Tab.items:
            Tab.items[i].itemClicked.connect(lambda:
                 self.changeParameter(nodeCard, list(Tab.items.keys()).index(Tab._currentRouteKey), 0)
            )
        nodeCard.setFixedSize(self.parent().parent().width()-20, 50)
        self.addWidget(nodeCard)

    def operationAlert(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(Icon.ALERT)
        Title.setFixedSize(20, 20)
        nodeCard.layout().addWidget(Title)
        Tab = SegmentedWidget()
        Tab.addItem('accept', '确定', icon=FIF.ACCEPT.icon())
        Tab.addItem('dismiss', '取消', icon=FIF.CLOSE.icon())
        Tab._currentRouteKey = list(Tab.items.keys())[data[0]]
        nodeCard.layout().addWidget(Tab)
        for i in Tab.items:
            Tab.items[i].itemClicked.connect(
                lambda: self.changeParameter(nodeCard, list(Tab.items.keys()).index(Tab._currentRouteKey), 0)
            )
        nodeCard.layout().addWidget(Tab)
        nodeCard.setFixedSize(self.parent().parent().width()-20, 50)
        self.addWidget(nodeCard)

    def operationCookie(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        nodeCard.layout().setContentsMargins(0, 0, 0, 0)
        Table = TableWidget()
        Table.setColumnCount(2)
        Table.setRowCount(len(data))
        Table.setFixedSize(self.parent().parent().width()-40, 200)
        Table.setHorizontalHeaderLabels(['Key', 'Value'])
        Table.setColumnWidth(0, 100)
        for i in range(1, Table.columnCount()):
            Table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        Table.setBorderVisible(True)
        Table.verticalHeader().hide()
        Table.setBorderRadius(8)
        Table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        Table.customContextMenuRequested.connect(lambda pos: self.showCustomContextMenu(pos, Table))
        # Table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        for index, (key, value) in enumerate(data.items()):
            Table.setItem(index, 0, QTableWidgetItem(key))
            Table.setItem(index, 1, QTableWidgetItem(value))

        Table.cellChanged.connect(lambda: self.tableChange(Table, nodeCard))

        Box = ToolBox()
        Box.addItem(Table, "Cookie")
        Box.setItemIcon(0, Icon.COOKIE)
        Box.layout().setContentsMargins(0, 0, 0, 0)
        Box.setFixedWidth(self.parent().parent().width()-20)
        nodeCard.layout().addWidget(Box)

        self.addWidget(nodeCard)

    def tableChange(self, table: TableWidget, nodeCard):
        data_dict = {}
        row_count = table.rowCount()
        for row in range(row_count):
            if table.item(row, 0): key = table.item(row, 0).text()
            else: key = ''
            if table.item(row, 1): value = table.item(row, 1).text()
            else: value = ''
            data_dict[key] = value
        self.changeParameter(nodeCard, data_dict)

    def showCustomContextMenu(self, pos, Table):
        index = Table.indexAt(pos)
        if not index.isValid():
            menu = RoundMenu(self)
            menu.addActions([Action(FIF.DELETE, '新增')])
            menu.actions()[0].triggered.connect(lambda: Table.insertRow(Table.rowCount()))
            menu.exec(Table.mapToGlobal(pos), aniType=MenuAnimationType.DROP_DOWN)
            return
        menu = RoundMenu(self)
        menu.addActions([Action(FIF.DELETE, '新增'), Action(FIF.EDIT, '修改'), Action(FIF.DELETE, '删除')])
        menu.actions()[0].triggered.connect(lambda: Table.insertRow(Table.rowCount()))
        menu.actions()[1].triggered.connect(lambda: Table.edit(index))
        menu.actions()[2].triggered.connect(lambda: Table.removeRow(index.row()))
        menu.exec(Table.mapToGlobal(pos), aniType=MenuAnimationType.DROP_DOWN)

    def operationFrames(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QHBoxLayout(nodeCard)
        Title = IconWidget()
        Title.setIcon(Icon.FRAME)
        Title.setFixedSize(20, 20)
        Mode = TransparentComboBox()
        Mode.setPrefix("操作")
        Mode.addItems(['ID进入iFrame', 'Name进入iFrame', '下标进入iFrame', '离开iFrame'])
        Mode.setCurrentIndex(data[0])
        Value = LineEdit()
        Value.setPlaceholderText('ID')
        Value.setText(data[1])
        Index = CompactSpinBox()
        Index.setFixedWidth(100)
        Index.setValue(data[2])
        if Mode.currentIndex() == 0:
            Value.setPlaceholderText('ID')
            Index.hide()
        elif Mode.currentIndex() == 1:
            Value.setPlaceholderText('Name')
            Index.hide()
        elif Mode.currentIndex() == 2:
            Value.hide()
        elif Mode.currentIndex() == 3:
            Value.hide()
            Index.hide()
        nodeCard.layout().addWidget(Title)
        nodeCard.layout().addWidget(Mode)
        nodeCard.layout().addWidget(Value)
        nodeCard.layout().addWidget(Index)
        Mode.currentIndexChanged.connect(lambda: self.modeChange(Mode.currentIndex(), Value, Index, nodeCard, Mode.currentIndex(), 0))
        Value.editingFinished.connect(lambda: self.changeParameter(nodeCard, Value.text(), 1))
        Index.valueChanged.connect(lambda: self.changeParameter(nodeCard, Index.value(), 2))
        nodeCard.setFixedSize(self.parent().parent().width()-20, 50)
        self.addWidget(nodeCard)

    def operationJS(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        QVBoxLayout(nodeCard)
        nodeCard.layout().setContentsMargins(0, 0, 0, 0)
        Edit = TextEdit()
        Edit.setPlaceholderText("Java Script")
        Edit.setFontFamily("Arial")
        Edit.setFontWeight(QFont.Weight.DemiBold)
        Edit.setText(data[0])
        Edit.setFixedHeight(200)
        JsHighlighter(Edit.document())
        # nodeCard.layout().addWidget(Edit)
        # nodeCard.layout().setContentsMargins(0, 0, 0, 0)
        Box = ToolBox()
        Box.setStyleSheet("background-color: rgba(0,0,0,0);border: 0px solid white")
        Box.addItem(Edit, "Java Script")
        Box.setItemIcon(0, Icon.JS)
        Box.layout().setContentsMargins(0, 0, 0, 0)
        Box.setFixedWidth(self.parent().parent().width() - 20)
        Edit.focusOutEvent = lambda e: self.changeParameter(nodeCard, Edit.toPlainText(), 0)
        nodeCard.layout().addWidget(Box)
        self.addWidget(nodeCard)

    def modeChange(self, modeSelected, Value: LineEdit, Index: CompactSpinBox, nodeCard, data, index=None):
        if modeSelected == 0:
            Value.setPlaceholderText('ID')
            Value.show()
            Index.hide()
        elif modeSelected == 1:
            Value.setPlaceholderText('Name')
            Value.show()
            Index.hide()
        elif modeSelected == 2:
            Index.show()
            Value.hide()
        elif modeSelected == 3:
            Index.hide()
            Value.hide()
        self.changeParameter(nodeCard, data, index)

    def insertCard(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        nodeCard.setBorderRadius(0)
        QHBoxLayout(nodeCard)
        Skl = Skeleton()
        Skl.hBoxLayout = QHBoxLayout()
        Skl.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        vBoxLayout = QVBoxLayout()
        rect = RoundedRectSkeletonItem(8, 8)
        vBoxLayout.addWidget(rect)
        Skl.hBoxLayout.setSpacing(14)
        Skl.hBoxLayout.addLayout(vBoxLayout)
        nodeCard.layout().addWidget(Skl)
        nodeCard.layout().setContentsMargins(2, 2, 2, 2)
        nodeCard.setFixedSize(self.parent().parent().width() - 20, 50)
        self.addWidget(nodeCard)

    def insertCardExample(self, data):
        nodeCard = SimpleCardWidget(self.parent().parent())
        nodeCard.setBorderRadius(0)
        nodeCard.setFixedSize(self.parent().parent().width() - 20, 50)
        self.addWidget(nodeCard)

    def changeParameter(self, nodeCard, data, index=None):
        row = self.indexOf(nodeCard)
        fcName = list(self.item.itemData[row])
        if index is not None:
            self.item.itemData[row][fcName[0]][index] = data
        else:
            self.item.itemData[row][fcName[0]] = data
        query = QSqlQuery(self.databese)
        query.prepare("UPDATE test_case SET data = :new_data WHERE test_case_id = :test_case_id")
        query.bindValue(":test_case_id", self.item.testCaseId)
        query.bindValue(":new_data", json.dumps(self.item.itemData))
        query.exec()
