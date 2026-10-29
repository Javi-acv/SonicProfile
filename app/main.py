import sys
from PySide6.QtWidgets import QApplication
from sonicprofile.main_window import MainWindow
from sonicprofile.theme import APP_STYLE

app = QApplication(sys.argv)
app.setApplicationName("SonicProfile")
app.setStyleSheet(APP_STYLE)
window = MainWindow()
window.show()
sys.exit(app.exec())
