import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QBrush, QFont, QColor


class JsHighlighter(QSyntaxHighlighter):
    keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'delete', 'else', 'except',
                'finally', 'for', 'from', 'function', 'if', 'import', 'in', 'is', 'let', 'module', 'new',
                'null', 'return', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void', 'while',
                'with', 'yield']

    functions = ['document', 'window']

    keywordFormat = QTextCharFormat()
    keywordFormat.setFontFamily("Arial")
    keywordFormat.setFontWeight(QFont.Weight.Bold)
    keywordFormat.setForeground(QBrush(QColor(174, 148, 249)))

    quoteFormat = QTextCharFormat()
    quoteFormat.setForeground(QBrush(QColor(0, 170, 0)))
    quoteFormat.setFontWeight(QFont.Weight.Bold)

    parenthesesFormat = QTextCharFormat()
    parenthesesFormat.setForeground(QBrush(QColor(255, 200, 0)))
    parenthesesFormat.setFontWeight(QFont.Weight.Bold)

    bracesFormat = QTextCharFormat()
    bracesFormat.setForeground(QBrush(QColor(255, 140, 0)))
    bracesFormat.setFontWeight(QFont.Weight.Bold)

    functionsFormat = QTextCharFormat()
    functionsFormat.setForeground(QBrush(QColor(235, 60, 84)))
    functionsFormat.setFontWeight(QFont.Weight.Bold)

    IntFormat = QTextCharFormat()
    IntFormat.setForeground(QBrush(QColor(79, 180, 215)))
    IntFormat.setFontWeight(QFont.Weight.Bold)

    def __init__(self, parent=None, QFontHighlighter=None):
        super(JsHighlighter, self).__init__(parent)
        self.highlightingRules = []

        for word in JsHighlighter.keywords:
            pattern = r"\b" + word + r"\b"
            rule = (pattern, self.keywordFormat)
            self.highlightingRules.append(rule)

        for function in JsHighlighter.functions:
            pattern = r"\b" + function + r"\b"
            rule = (pattern, self.functionsFormat)
            self.highlightingRules.append(rule)

    def highlightBlock(self, text):
        for pattern, formats in self.highlightingRules:
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end()
                self.setFormat(start, end - start, formats)

            pattern = r"'[^']*'"
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end() - 1
                self.setFormat(start, end - start + 1, self.quoteFormat)

            pattern = r'"[^"]*"'
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end() - 1
                self.setFormat(start, end - start + 1, self.quoteFormat)

            pattern = r"\([a-zA-Z0-9_.!,-]+[ !,-]*\)"
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end() - 1
                self.setFormat(start, end - start + 1, self.parenthesesFormat)

            pattern = r"\{"
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end() - 1
                self.setFormat(start, end - start + 1, self.bracesFormat)

            pattern = r"\}"
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end() - 1
                self.setFormat(start, end - start + 1, self.bracesFormat)

            pattern = r"\b\d+\b"
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end() - 1
                self.setFormat(start, end - start + 1, self.IntFormat)