# -*- coding: utf-8 -*-

"""
Worker Thread - Pi-UVMorphe
"""

import sys
import os
import threading
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal, QObject

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class LogEmitter(QObject):
    """Log emitter"""
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)


class WorkerThread(QThread):
    """Worker thread for analysis"""

    finished = pyqtSignal(object, object)  # matches_df, reliability
    error = pyqtSignal(str)
    log = pyqtSignal(str)
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(self, args, parent=None):
        super().__init__(parent)
        self.args = args

        # Setup log capture
        self.log_emitter = LogEmitter()
        self.log_emitter.log_signal.connect(self.log.emit)
        self.log_emitter.progress_signal.connect(self.progress.emit)
        self.log_emitter.status_signal.connect(self.status.emit)

    def run(self):
        """Run analysis"""
        try:
            # Import and run analysis
            from run import main_with_args

            # Redirect stdout to log
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            class LogRedirector:
                def __init__(self, emitter, is_error=False):
                    self.emitter = emitter
                    self.is_error = is_error
                    self.buffer = ""

                def write(self, text):
                    self.buffer += text
                    if '\n' in self.buffer:
                        lines = self.buffer.split('\n')
                        for line in lines[:-1]:
                            if line.strip():
                                self.emitter.log_signal.emit(line)
                        self.buffer = lines[-1]

                def flush(self):
                    if self.buffer.strip():
                        self.emitter.log_signal.emit(self.buffer)
                        self.buffer = ""

            sys.stdout = LogRedirector(self.log_emitter)
            sys.stderr = LogRedirector(self.log_emitter, True)

            try:
                # Execute analysis
                self.status.emit("Analyzing...")
                self.progress.emit(0)

                matches_df, reliability = main_with_args(self.args)

                self.progress.emit(100)
                self.status.emit("Analysis complete")
                self.finished.emit(matches_df, reliability)

            finally:
                # Restore stdout
                sys.stdout = old_stdout
                sys.stderr = old_stderr

        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.error.emit(error_msg)