from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QTextEdit
)
import sys


app = QApplication(sys.argv)


# -------------------------
# Home Screen
# -------------------------

home_window = QWidget()
home_window.setWindowTitle("Future Self")
home_window.resize(800, 600)


home_label = QLabel("Welcome to Future Self")

journal_button = QPushButton("New Journal")
goals_button = QPushButton("My Goals")
exit_button = QPushButton("Exit")


home_layout = QVBoxLayout()
home_layout.addWidget(home_label)
home_layout.addWidget(journal_button)
home_layout.addWidget(goals_button)
home_layout.addWidget(exit_button)

home_window.setLayout(home_layout)


# -------------------------
# Journal Screen
# -------------------------

journal_window = QWidget()
journal_window.setWindowTitle("Future Self - Journal")
journal_window.resize(800, 600)


journal_label = QLabel("Today's Reflection")

journal_text = QTextEdit()
journal_text.setPlaceholderText("Write your thoughts here...")

save_journal_button = QPushButton("Save Entry")
journal_back_button = QPushButton("Back")


journal_layout = QVBoxLayout()
journal_layout.addWidget(journal_label)
journal_layout.addWidget(journal_text)
journal_layout.addWidget(save_journal_button)
journal_layout.addWidget(journal_back_button)

journal_window.setLayout(journal_layout)


# -------------------------
# Goals Screen
# -------------------------

goals_window = QWidget()
goals_window.setWindowTitle("Future Self - Goals")
goals_window.resize(800, 600)


goals_label = QLabel("My Goals")

goals_text = QTextEdit()
goals_text.setPlaceholderText("Write your goals here...")

save_goals_button = QPushButton("Save Goals")
goals_back_button = QPushButton("Back")


goals_layout = QVBoxLayout()
goals_layout.addWidget(goals_label)
goals_layout.addWidget(goals_text)
goals_layout.addWidget(save_goals_button)
goals_layout.addWidget(goals_back_button)

goals_window.setLayout(goals_layout)


# -------------------------
# Navigation Functions
# -------------------------

def open_journal():
    home_window.hide()
    journal_window.show()


def open_goals():
    home_window.hide()
    goals_window.show()


def go_home_from_journal():
    journal_window.hide()
    home_window.show()


def go_home_from_goals():
    goals_window.hide()
    home_window.show()


def save_journal():
    journal_label.setText("Journal Entry Saved!")


def save_goals():
    goals_label.setText("Goals Saved!")


# -------------------------
# Button Connections
# -------------------------

journal_button.clicked.connect(open_journal)
goals_button.clicked.connect(open_goals)
exit_button.clicked.connect(app.quit)

journal_back_button.clicked.connect(go_home_from_journal)
goals_back_button.clicked.connect(go_home_from_goals)

save_journal_button.clicked.connect(save_journal)
save_goals_button.clicked.connect(save_goals)


# -------------------------
# Start Application
# -------------------------

home_window.show()

sys.exit(app.exec())