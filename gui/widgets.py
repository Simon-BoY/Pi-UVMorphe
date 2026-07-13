# -*- coding: utf-8 -*-

"""
Custom GUI Widgets - Pi-UVMorphe
"""

import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FileBrowseWidget(QWidget):
    """File browser widget"""
    file_selected = pyqtSignal(str)

    def __init__(self, placeholder="Select file", file_filter="All files (*.*)", parent=None):
        super().__init__(parent)
        self.file_filter = file_filter

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.textChanged.connect(self.file_selected.emit)
        layout.addWidget(self.line_edit)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setFixedWidth(80)
        self.browse_btn.clicked.connect(self.browse)
        layout.addWidget(self.browse_btn)

    def browse(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", self.file_filter)
        if file_path:
            self.line_edit.setText(file_path)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)


class DirectoryBrowseWidget(QWidget):
    """Directory browser widget"""
    dir_selected = pyqtSignal(str)

    def __init__(self, placeholder="Select directory", parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.textChanged.connect(self.dir_selected.emit)
        layout.addWidget(self.line_edit)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setFixedWidth(80)
        self.browse_btn.clicked.connect(self.browse)
        layout.addWidget(self.browse_btn)

    def browse(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.line_edit.setText(dir_path)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)


class CollapsibleBox(QWidget):
    """Collapsible box widget"""

    def __init__(self, title="", parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title button
        self.toggle_btn = QPushButton(title)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px 12px;
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.clicked.connect(self.toggle)
        layout.addWidget(self.toggle_btn)

        # Content area
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.content)

    def toggle(self):
        checked = self.toggle_btn.isChecked()
        self.content.setVisible(checked)
        self.toggle_btn.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)

    def addLayout(self, layout):
        self.content_layout.addLayout(layout)


class LogTextEdit(QTextEdit):
    """Log text edit widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setObjectName("log_text")
        self.setMaximumHeight(250)
        self.setStyleSheet("""
            QTextEdit#log_text {
                font-family: Consolas, monospace;
                font-size: 13px;
                background-color: #1e1e1e;
                color: #d4d4d4;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        self.setLineWrapMode(QTextEdit.NoWrap)

    def append_log(self, text):
        """Append log message with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.append(f"[{timestamp}] {text}")
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def clear(self):
        super().clear()