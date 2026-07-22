from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Future Self")
window.resize(800, 600)

label = QLabel("Welcome to Future Self")
layout = QVBoxLayout()
layout.addWidget(label)
window.setLayout(layout)

window.show()

sys.exit(app.exec())