# coding: utf-8
from PySide6.QtCore import QFile, QUrl
from PySide6.QtGui import QDesktopServices
from json import loads


def loadJsonData(fileName: str):
    """ load json data from file """
    file = QFile(f":/gallery/chart/{fileName}.json")
    if not file.open(QFile.OpenModeFlag.ReadOnly):
        print(f"`{fileName}` 不存在")

    data = loads(str(file.readAll(), encoding='utf-8'))
    file.close()

    return data

def openUrl(url: str):
    QDesktopServices.openUrl(QUrl(url))