from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QFrame
)
import sys


app = QApplication(sys.argv)


# Home Screen

home_window = QWidget()
home_window.setWindowTitle("Future Self")
home_window.resize(800, 600)


# Header
home_title = QLabel("Future Self")
home_title.setStyleSheet(
    "font-size: 32px; font-weight: bold;"
)

home_welcome = QLabel("Welcome back.")
home_welcome.setStyleSheet(
    "font-size: 20px;"
)

home_subtitle = QLabel(
    "What do you want to work on today?"
)
home_subtitle.setStyleSheet(
    "font-size: 16px;"
)

# Today Section

today_frame = QFrame()
today_frame.setFrameShape(QFrame.Shape.StyledPanel)

today_layout = QVBoxLayout()

today_label = QLabel("TODAY")
today_label.setStyleSheet(
    "font-size: 14px; font-weight: bold;"
)

today_info = QLabel(
    "Take some time today to reflect, plan, "
    "and move forward with intention."
)
today_info.setStyleSheet(
    "font-size: 15px;"
)

today_layout.addWidget(today_label)
today_layout.addWidget(today_info)

today_frame.setLayout(today_layout)


# Journal Card

journal_frame = QFrame()
journal_frame.setFrameShape(QFrame.Shape.StyledPanel)

journal_card_layout = QVBoxLayout()

journal_card_title = QLabel("Journal")
journal_card_title.setStyleSheet(
    "font-size: 20px; font-weight: bold;"
)

journal_card_text = QLabel(
    "Take a moment to reflect on your day."
)
journal_card_text.setStyleSheet(
    "font-size: 14px;"
)

journal_button = QPushButton("New Journal")

journal_card_layout.addWidget(journal_card_title)
journal_card_layout.addWidget(journal_card_text)
journal_card_layout.addWidget(journal_button)

journal_frame.setLayout(journal_card_layout)


# Goals Card

goals_frame = QFrame()
goals_frame.setFrameShape(QFrame.Shape.StyledPanel)

goals_card_layout = QVBoxLayout()

goals_card_title = QLabel("Goals")
goals_card_title.setStyleSheet(
    "font-size: 20px; font-weight: bold;"
)

goals_card_text = QLabel(
    "Keep moving forward with intention."
)
goals_card_text.setStyleSheet(
    "font-size: 14px;"
)

goals_button = QPushButton("View Goals")

goals_card_layout.addWidget(goals_card_title)
goals_card_layout.addWidget(goals_card_text)
goals_card_layout.addWidget(goals_button)

goals_frame.setLayout(goals_card_layout)


# Put Journal and Goals beside each other
cards_layout = QHBoxLayout()
cards_layout.addWidget(journal_frame)
cards_layout.addWidget(goals_frame)


# Reflection Section

reflection_frame = QFrame()
reflection_frame.setFrameShape(QFrame.Shape.StyledPanel)

reflection_layout = QVBoxLayout()

reflection_label = QLabel("REFLECTION")
reflection_label.setStyleSheet(
    "font-size: 14px; font-weight: bold;"
)

reflection_text = QLabel(
    "Who am I becoming through the choices "
    "I'm making today?"
)
reflection_text.setStyleSheet(
    "font-size: 15px;"
)

reflection_layout.addWidget(reflection_label)
reflection_layout.addWidget(reflection_text)

reflection_frame.setLayout(reflection_layout)


# Exit Button


exit_button = QPushButton("Exit")


# Home Layout

home_layout = QVBoxLayout()

home_layout.addWidget(home_title)
home_layout.addWidget(home_welcome)
home_layout.addWidget(home_subtitle)

home_layout.addSpacing(25)

home_layout.addWidget(today_frame)

home_layout.addSpacing(20)

home_layout.addLayout(cards_layout)

home_layout.addSpacing(20)

home_layout.addWidget(reflection_frame)

home_layout.addStretch()

home_layout.addWidget(exit_button)

home_window.setLayout(home_layout)


# Journal Screen

journal_window = QWidget()
journal_window.setWindowTitle("Future Self - Journal")
journal_window.resize(800, 600)


journal_label = QLabel("Today's Reflection")

journal_text = QTextEdit()
journal_text.setPlaceholderText(
    "Write your thoughts here..."
)

save_journal_button = QPushButton("Save Entry")
journal_back_button = QPushButton("Back")


journal_layout = QVBoxLayout()

journal_layout.addWidget(journal_label)
journal_layout.addWidget(journal_text)
journal_layout.addWidget(save_journal_button)
journal_layout.addWidget(journal_back_button)

journal_window.setLayout(journal_layout)


# Goals Screen

goals_window = QWidget()
goals_window.setWindowTitle("Future Self - Goals")
goals_window.resize(800, 600)


goals_label = QLabel("My Goals")

goals_text = QTextEdit()
goals_text.setPlaceholderText(
    "Write your goals here..."
)

save_goals_button = QPushButton("Save Goals")
goals_back_button = QPushButton("Back")


goals_layout = QVBoxLayout()

goals_layout.addWidget(goals_label)
goals_layout.addWidget(goals_text)
goals_layout.addWidget(save_goals_button)
goals_layout.addWidget(goals_back_button)

goals_window.setLayout(goals_layout)


# Navigation Functions

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


# Button Connections

journal_button.clicked.connect(open_journal)
goals_button.clicked.connect(open_goals)
exit_button.clicked.connect(app.quit)

journal_back_button.clicked.connect(go_home_from_journal)
goals_back_button.clicked.connect(go_home_from_goals)

save_journal_button.clicked.connect(save_journal)
save_goals_button.clicked.connect(save_goals)


# Start Application

home_window.show()

sys.exit(app.exec())