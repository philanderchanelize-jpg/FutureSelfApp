from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Future Self")
window.resize(800, 600)

label = QLabel("Welcome to Future Self")

journal_button = QPushButton("New Journal")
goals_button = QPushButton("My Goals")
exit_button = QPushButton("Exit")

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(journal_button)
layout.addWidget(goals_button)
layout.addWidget(exit_button)

window.setLayout(layout)

window.show()

sys.exit(app.exec())