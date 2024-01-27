# coding: utf-8
from PySide6.QtCore import QObject


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.text = self.tr('Text')
        self.view = self.tr('View')
        self.charts = self.tr("Charts")
        self.menus = self.tr('Menus & toolbars')
        self.icons = self.tr('Icons')
        self.layout = self.tr('Layout')
        self.dialogs = self.tr('Dialogs & flyouts')
        self.scroll = self.tr('Scrolling')
        self.material = self.tr('Material')
        self.dateTime = self.tr('Date & time')
        self.navigation = self.tr('Navigation')
        self.basicInput = self.tr('Basic input')
        self.statusInfo = self.tr('Status & info')
        self.price = self.tr("Price plan")

class ChartTranslator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.line = self.tr("Line")
        self.bar = self.tr("Bar")
        self.pie = self.tr("Pie")
        self.funnel = self.tr("Funnel")
        self.scatter = self.tr("Scatter")
        self.gauge = self.tr("Gauge")
        self.radar = self.tr("Radar")
        self.boxplot = self.tr("Boxplot")
        self.heatmap = self.tr("Heatmap")
        self.graph = self.tr("Graph")
        self.calendar = self.tr("Calendar")
        self.candlestick = self.tr("Candlestick")
