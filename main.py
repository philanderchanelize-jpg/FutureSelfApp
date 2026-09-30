from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QFrame,
    QMessageBox,
    QCheckBox
)
import sys
from datetime import datetime

app = QApplication(sys.argv)

home_window = QWidget()
home_window.setWindowTitle("Future Self")
home_window.resize(800, 600)

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

cards_layout = QHBoxLayout()
cards_layout.addWidget(journal_frame)
cards_layout.addWidget(goals_frame)

reflection_frame = QFrame()
reflection_frame.setFrameShape(QFrame.Shape.StyledPanel)

reflection_layout = QVBoxLayout()

reflection_label = QLabel("REFLECTION")
reflection_label.setStyleSheet(
    "font-size: 14px; font-weight: bold;"
)

reflection_question = QLabel(
    "Who am I becoming through the choices "
    "I'm making today?"
)
reflection_question.setStyleSheet(
    "font-size: 15px;"
)

reflection_input = QTextEdit()
reflection_input.setPlaceholderText(
    "Write your reflection here..."
)

save_reflection_button = QPushButton("Save Reflection")

reflection_layout.addWidget(reflection_label)
reflection_layout.addWidget(reflection_question)
reflection_layout.addWidget(reflection_input)
reflection_layout.addWidget(save_reflection_button)

reflection_frame.setLayout(reflection_layout)

todo_frame = QFrame()
todo_frame.setFrameShape(QFrame.Shape.StyledPanel)

todo_layout = QVBoxLayout()

todo_label = QLabel("TASKS")
todo_label.setStyleSheet(
    "font-size: 14px; font-weight: bold;"
)

todo_input = QLineEdit()
todo_input.setPlaceholderText(
    "Add a task..."
)

add_task_button = QPushButton("Add Task")

todo_list_layout = QVBoxLayout()

todo_layout.addWidget(todo_label)
todo_layout.addWidget(todo_input)
todo_layout.addWidget(add_task_button)
todo_layout.addLayout(todo_list_layout)

todo_frame.setLayout(todo_layout)

exit_button = QPushButton("Exit")

home_layout = QVBoxLayout()

home_layout.addWidget(home_title)
home_layout.addWidget(home_welcome)
home_layout.addWidget(home_subtitle)

home_layout.addSpacing(25)

home_layout.addWidget(today_frame)

home_layout.addSpacing(20)

home_layout.addLayout(cards_layout)

home_layout.addSpacing(20)

home_layout.addWidget(todo_frame)

home_layout.addSpacing(20)

home_layout.addWidget(reflection_frame)

home_layout.addStretch()

home_layout.addWidget(exit_button)

home_window.setLayout(home_layout)

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
    entry = journal_text.toPlainText().strip()

    if not entry:
        QMessageBox.warning(
            journal_window,
            "Warning",
            "Please enter a journal entry."
        )
        return

    current_time = datetime.now().strftime(
        "%d %B %Y at %H:%M"
    )

    journal_label.setText(
        f"Journal Entry Saved! • {current_time}"
    )

def save_goals():
    entry = goals_text.toPlainText().strip()

    if not entry:
        QMessageBox.warning(
            goals_window,
            "Warning",
            "Please enter your goals."
        )
        return

    current_time = datetime.now().strftime(
        "%d %B %Y at %H:%M"
    )

    goals_label.setText(
        f"Goals Saved! • {current_time}"
    )

def save_reflection():
    reflection = reflection_input.toPlainText().strip()

    if not reflection:
        QMessageBox.warning(
            home_window,
            "Warning",
            "Please write a reflection."
        )
        return

    current_time = datetime.now().strftime(
        "%d %B %Y at %H:%M"
    )

    reflection_label.setText(
        f"REFLECTION SAVED • {current_time}"
    )

def complete_task(state, checkbox):
    if state:
        current_time = datetime.now().strftime(
            "%d %B %Y at %H:%M"
        )

        task = checkbox.property("task")

        checkbox.setText(
            f"{task} • Completed {current_time}"
        )
    else:
        task = checkbox.property("task")
        checkbox.setText(task)

def add_task():
    task = todo_input.text().strip()

    if not task:
        QMessageBox.warning(
            home_window,
            "Warning",
            "Please enter a task."
        )
        return

    task_checkbox = QCheckBox(task)
    task_checkbox.setProperty("task", task)

    task_checkbox.stateChanged.connect(
        lambda state: complete_task(
            state,
            task_checkbox
        )
    )

    todo_list_layout.addWidget(task_checkbox)

    todo_input.clear()

journal_button.clicked.connect(open_journal)
goals_button.clicked.connect(open_goals)
exit_button.clicked.connect(app.quit)

journal_back_button.clicked.connect(
    go_home_from_journal
)

goals_back_button.clicked.connect(
    go_home_from_goals
)

save_journal_button.clicked.connect(save_journal)
save_goals_button.clicked.connect(save_goals)
save_reflection_button.clicked.connect(
    save_reflection
)

add_task_button.clicked.connect(add_task)

home_window.show()

sys.exit(app.exec())