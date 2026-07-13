from PySide6.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Future Self")
window.resize(800, 600)

window.show()

sys.exit(app.exec())