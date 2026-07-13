# -*- coding: utf-8 -*-

"""
GUI样式表定义
"""

# 主窗口样式
MAIN_STYLE = """
QMainWindow {
    background-color: #f5f7fa;
}

QLabel {
    font-size: 12px;
    font-weight: 500;
    color: #2c3e50;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #dce1e8;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    background-color: white;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px 0 8px;
    color: #2c3e50;
}

QLineEdit, QTextEdit, QComboBox {
    padding: 8px 10px;
    border: 2px solid #dce1e8;
    border-radius: 6px;
    font-size: 11px;
    background-color: white;
    color: #2c3e50;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border-color: #4CAF50;
}

QTextEdit {
    font-family: Consolas, monospace;
}

QPushButton {
    padding: 8px 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
    min-height: 30px;
}
QPushButton:hover {
    background-color: #43A047;
}
QPushButton:pressed {
    background-color: #388E3C;
}
QPushButton:disabled {
    background-color: #bdbdbd;
    color: #757575;
}

QPushButton#danger_btn {
    background-color: #e74c3c;
}
QPushButton#danger_btn:hover {
    background-color: #c0392b;
}

QPushButton#info_btn {
    background-color: #3498db;
}
QPushButton#info_btn:hover {
    background-color: #2980b9;
}

QPushButton#warning_btn {
    background-color: #f39c12;
}
QPushButton#warning_btn:hover {
    background-color: #e67e22;
}

QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #ecf0f1;
    height: 20px;
}
QProgressBar::chunk {
    border-radius: 4px;
    background-color: #4CAF50;
}

QTextEdit#log_text {
    font-family: Consolas, monospace;
    font-size: 10px;
    background-color: #1e1e1e;
    color: #d4d4d4;
    border-radius: 6px;
}

QTabWidget::pane {
    border: 2px solid #dce1e8;
    border-radius: 8px;
    background-color: white;
}
QTabBar::tab {
    padding: 8px 16px;
    background-color: #ecf0f1;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #4CAF50;
    color: white;
}
QTabBar::tab:hover:!selected {
    background-color: #d5dbdb;
}

QCheckBox {
    font-size: 12px;
    color: #2c3e50;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
}
QCheckBox::indicator:checked {
    background-color: #4CAF50;
    border-radius: 4px;
}

QStatusBar {
    background-color: #2c3e50;
    color: white;
    font-size: 11px;
}
QStatusBar::item {
    border: none;
}

QScrollBar:vertical {
    border: none;
    background-color: #ecf0f1;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #bdc3c7;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background-color: #95a5a6;
}

QScrollBar:horizontal {
    border: none;
    background-color: #ecf0f1;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background-color: #bdc3c7;
    border-radius: 5px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #95a5a6;
}

QMessageBox {
    background-color: white;
}
QMessageBox QLabel {
    color: #2c3e50;
}
"""

# 结果表格样式
TABLE_STYLE = """
QTableWidget {
    gridline-color: #dce1e8;
    background-color: white;
    border: 1px solid #dce1e8;
    border-radius: 6px;
}
QTableWidget::item {
    padding: 5px;
}
QTableWidget::item:selected {
    background-color: #4CAF50;
    color: white;
}
QHeaderView::section {
    background-color: #34495e;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}
QTableWidget QTableCornerButton::section {
    background-color: #34495e;
}
"""