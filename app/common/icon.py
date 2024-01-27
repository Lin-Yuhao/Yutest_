# coding: utf-8
from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):

    ALERT = "Alert"
    BAR = "Bar"
    COOKIE = "Cookie"
    FRAME = "Frame"
    TAB = "Tab"
    FUNNEL = "Funnel"
    URL = "Url"
    JS = "JS"
    WINDOW = "Window"
    WINDOWSIZE = "WindowSize"
    WINDOWSWITCH = "WindowSwitch"
    MAXIMIZE = "MaxImize"
    MINIMIZE = "MinImize"
    TABSWITCH = "TabSwitch"
    FULLSCREEN = "FullScreen"
    GHOST = "Ghost"
    LAZY = "Lazy"

    def path(self, theme=Theme.AUTO):
        return f":/gallery/images/icons/{self.value}_{getIconColor(theme)}.svg"


class ChartIcon(FluentIconBase, Enum):
    """ Chart icon """

    MENU = "Menu"
    TEXT = "Text"
    GRID = "Grid"
    FUNNEL = "Funnel"
    BOXPLOT = "Boxplot"
    BAR = "Bar"
    SCATTER = "Scatter"
    GAUGE = "Gauge"
    LINE = "Line"
    RADAR = "Radar"
    FIRE = "Fire"

    def path(self, theme=Theme.AUTO):
        return f":/gallery/images/icons/{self.value}_{getIconColor(theme)}.svg"
