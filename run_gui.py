#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pi-Morphe GUI Launcher
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from gui import PiMorpheMainWindow


def main():
    """Launch GUI"""
    # Enable high DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set application info
    app.setApplicationName("Pi-Morphe")
    app.setOrganizationName("PiMorphe")

    # Create main window
    window = PiMorpheMainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()