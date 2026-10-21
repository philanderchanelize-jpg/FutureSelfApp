import sys
import sqlite3
from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QFrame,
    QMessageBox,
    QCheckBox,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QScrollArea,
    QComboBox,
    QInputDialog,
)

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "future_self.db"

COLORS = {
    "background": "#F5F0E7",
    "paper": "#FFFCF6",
    "olive": "#737B50",
    "olive_dark": "#535B38",
    "terracotta": "#B96F55",
    "charcoal": "#302F29",
    "muted": "#817C70",
    "border": "#E3D9C9",
    "gold": "#B69A62",
    "soft_olive": "#E8E9DD",
    "soft_terra": "#F2E3DA",
}


def timestamp_now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def format_timestamp(value):
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value).astimezone().strftime(
            "%d %B %Y at %H:%M"
        )
    except ValueError:
        return value


class Store:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.setup()

    def setup(self):
        with self.connection:
            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL CHECK(kind IN ('journal', 'reflection')),
                    title TEXT NOT NULL DEFAULT '',
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )"""
            )
            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT,
                    category TEXT NOT NULL DEFAULT 'Short term'
                )"""
            )
            goal_columns = {
                row[1] for row in self.connection.execute(
                    "PRAGMA table_info(goals)"
                ).fetchall()
            }
            if "category" not in goal_columns:
                self.connection.execute(
                    "ALTER TABLE goals ADD COLUMN category TEXT "
                    "NOT NULL DEFAULT 'Short term'"
                )
            self.connection.execute(
                """CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )"""
            )

    def save_entry(self, kind, title, content, entry_id=None):
        now = timestamp_now()
        with self.connection:
            if entry_id:
                self.connection.execute(
                    """UPDATE entries
                    SET title = ?, content = ?, updated_at = ?
                    WHERE id = ? AND kind = ?""",
                    (title, content, now, entry_id, kind),
                )
                return entry_id

            cursor = self.connection.execute(
                """INSERT INTO entries
                (kind, title, content, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)""",
                (kind, title, content, now, now),
            )
            return cursor.lastrowid

    def entries(self, kind):
        return self.connection.execute(
            """SELECT * FROM entries
            WHERE kind = ?
            ORDER BY updated_at DESC, id DESC""",
            (kind,),
        ).fetchall()

    def entry(self, entry_id):
        return self.connection.execute(
            "SELECT * FROM entries WHERE id = ?",
            (entry_id,),
        ).fetchone()

    def delete_entry(self, entry_id):
        with self.connection:
            self.connection.execute(
                "DELETE FROM entries WHERE id = ?",
                (entry_id,),
            )

    def add_goal(self, title, category):
        with self.connection:
            self.connection.execute(
                "INSERT INTO goals (title, created_at, category) "
                "VALUES (?, ?, ?)",
                (title, timestamp_now(), category),
            )

    def set_goal_category(self, goal_id, category):
        with self.connection:
            self.connection.execute(
                "UPDATE goals SET category = ? WHERE id = ?",
                (category, goal_id),
            )

    def goals(self):
        return self.connection.execute(
            "SELECT * FROM goals ORDER BY id DESC"
        ).fetchall()

    def set_goal_completed(self, goal_id, completed):
        with self.connection:
            self.connection.execute(
                "UPDATE goals SET completed_at = ? WHERE id = ?",
                (timestamp_now() if completed else None, goal_id),
            )

    def delete_goal(self, goal_id):
        with self.connection:
            self.connection.execute(
                "DELETE FROM goals WHERE id = ?",
                (goal_id,),
            )

    def add_task(self, title):
        with self.connection:
            self.connection.execute(
                "INSERT INTO tasks (title, created_at) VALUES (?, ?)",
                (title, timestamp_now()),
            )

    def tasks(self):
        return self.connection.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    def set_task_completed(self, task_id, completed):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks SET completed_at = ? WHERE id = ?",
                (timestamp_now() if completed else None, task_id),
            )

    def update_task_title(self, task_id, title):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks SET title = ? WHERE id = ?",
                (title, task_id),
            )

    def delete_task(self, task_id):
        with self.connection:
            self.connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,),
            )

    def close(self):
        self.connection.close()


class FutureSelfWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.store = Store(DB_PATH)
        self.current_entry_id = None
        self.current_entry_kind = "journal"

        self.setWindowTitle("Future Self")
        self.resize(1000, 760)
        self.setMinimumSize(800, 600)
        self.setObjectName("mainWindow")
        self.setStyleSheet(self.stylesheet())

        self.build_ui()
        self.refresh_all()
        self.show_page("home")

    def stylesheet(self):
        c = COLORS

        return f"""
            QWidget {{
                background: {c['background']};
                color: {c['charcoal']};
                font-family: 'Segoe UI';
                font-size: 14px;
            }}

            QMainWindow, QScrollArea,
            QScrollArea > QWidget > QWidget {{
                background: {c['background']};
                border: none;
            }}

            QLabel {{
                background: transparent;
            }}

            QLabel#brand {{
                font-size: 30px;
                font-weight: 700;
                color: {c['charcoal']};
            }}

            QLabel#eyebrow {{
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
                color: {c['olive']};
            }}

            QLabel#pageTitle {{
                font-size: 27px;
                font-weight: 700;
                color: {c['charcoal']};
            }}

            QLabel#muted {{
                color: {c['muted']};
            }}

            QLabel#cardTitle {{
                font-size: 19px;
                font-weight: 700;
            }}

            QLabel#timestamp {{
                font-size: 11px;
                color: {c['muted']};
            }}

            QFrame#card {{
                background: {c['paper']};
                border: 1px solid {c['border']};
                border-radius: 16px;
            }}

            QFrame#hero {{
                background: {c['soft_olive']};
                border: 1px solid #D8DCCB;
                border-radius: 18px;
            }}

            QFrame#terraCard {{
                background: {c['soft_terra']};
                border: 1px solid #E8D3C6;
                border-radius: 16px;
            }}

            QPushButton {{
                background: {c['olive']};
                color: #FFFFFF;
                border: none;
                border-radius: 9px;
                padding: 10px 16px;
                font-weight: 600;
                min-height: 18px;
            }}

            QPushButton:hover {{
                background: {c['olive_dark']};
            }}

            QPushButton:pressed {{
                background: #41482C;
            }}

            QPushButton#secondary {{
                background: {c['paper']};
                color: {c['olive_dark']};
                border: 1px solid {c['border']};
            }}

            QPushButton#secondary:hover {{
                background: {c['soft_olive']};
            }}

            QPushButton#terraButton {{
                background: {c['terracotta']};
                color: #FFFFFF;
            }}

            QPushButton#terraButton:hover {{
                background: #A45E46;
            }}

            QPushButton#danger {{
                background: transparent;
                color: {c['terracotta']};
                border: 1px solid #E6C9BC;
                padding-left: 10px;
                padding-right: 10px;
            }}

            QPushButton#danger:hover {{
                background: {c['soft_terra']};
            }}

            QPushButton#nav {{
                background: transparent;
                color: {c['muted']};
                text-align: left;
                padding: 10px 12px;
                border-radius: 8px;
            }}

            QPushButton#nav:hover,
            QPushButton#nav[active="true"] {{
                background: {c['soft_olive']};
                color: {c['olive_dark']};
            }}

            QLineEdit, QTextEdit, QListWidget {{
                background: {c['paper']};
                border: 1px solid {c['border']};
                border-radius: 10px;
                padding: 10px;
                selection-background-color: {c['olive']};
                selection-color: white;
            }}

            QLineEdit:focus, QTextEdit:focus, QListWidget:focus {{
                border: 1px solid {c['olive']};
            }}

            QTextEdit {{
                padding: 12px;
            }}

            QListWidget {{
                padding: 6px;
            }}

            QListWidget::item {{
                padding: 9px;
                border-radius: 7px;
            }}

            QListWidget::item:selected {{
                background: {c['soft_olive']};
                color: {c['charcoal']};
            }}

            QCheckBox {{
                spacing: 10px;
                background: transparent;
            }}

            QCheckBox::indicator {{
                width: 17px;
                height: 17px;
            }}

            QCheckBox::indicator:unchecked {{
                border: 1px solid {c['gold']};
                background: {c['paper']};
                border-radius: 5px;
            }}

            QCheckBox::indicator:checked {{
                border: 1px solid {c['olive']};
                background: {c['olive']};
                border-radius: 5px;
            }}

            QScrollBar:vertical {{
                background: transparent;
                width: 9px;
                margin: 3px;
            }}

            QScrollBar::handle:vertical {{
                background: {c['border']};
                border-radius: 4px;
                min-height: 25px;
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0;
            }}
        """

    def build_ui(self):
        root = QWidget()
        outer = QHBoxLayout(root)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(18)

        sidebar = QFrame()
        sidebar.setObjectName("card")
        sidebar.setFixedWidth(185)

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(14, 18, 14, 16)
        side_layout.setSpacing(8)

        brand = QLabel("Future Self")
        brand.setObjectName("brand")
        brand.setWordWrap(True)
        side_layout.addWidget(brand)

        tagline = QLabel("A life, with intention.")
        tagline.setObjectName("muted")
        tagline.setWordWrap(True)
        side_layout.addWidget(tagline)
        side_layout.addSpacing(22)

        self.nav_buttons = {}

        for key, label in (
            ("home", "Home"),
            ("journal", "Journal"),
            ("goals", "Goals"),
            ("reflection", "Reflection"),
        ):
            button = QPushButton(label)
            button.setObjectName("nav")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, page=key: self.show_page(page)
            )
            side_layout.addWidget(button)
            self.nav_buttons[key] = button

        side_layout.addStretch()

        side_note = QLabel("Small steps still move you forward.")
        side_note.setObjectName("muted")
        side_note.setWordWrap(True)
        side_layout.addWidget(side_note)

        self.pages = QStackedWidget()
        self.pages.addWidget(self.build_home_page())
        self.pages.addWidget(self.build_journal_page())
        self.pages.addWidget(self.build_goals_page())
        self.pages.addWidget(self.build_reflection_page())

        self.page_indices = {
            "home": 0,
            "journal": 1,
            "goals": 2,
            "reflection": 3,
        }

        outer.addWidget(sidebar)
        outer.addWidget(self.pages, 1)
        self.setCentralWidget(root)

    def scroll_page(self, content):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(content)
        return scroll

    def make_card(self, object_name="card"):
        frame = QFrame()
        frame.setObjectName(object_name)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        return frame, layout

    def page_heading(self, eyebrow, title, subtitle):
        layout = QVBoxLayout()
        layout.setSpacing(5)

        label = QLabel(eyebrow.upper())
        label.setObjectName("eyebrow")

        heading = QLabel(title)
        heading.setObjectName("pageTitle")

        description = QLabel(subtitle)
        description.setObjectName("muted")
        description.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(heading)
        layout.addWidget(description)

        return layout

    def build_home_page(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 4, 8, 8)
        layout.setSpacing(16)

        layout.addLayout(
            self.page_heading(
                "Your personal space",
                "Welcome back.",
                "Make room for the person you're becoming.",
            )
        )

        hero, hero_layout = self.make_card("hero")
        hero_layout.addWidget(self.label("TODAY", "eyebrow"))
        hero_layout.addWidget(
            self.label(
                "Take a breath. Choose what matters. Begin where you are.",
                "cardTitle",
            )
        )

        self.today_date = self.label(
            datetime.now().strftime("%A, %d %B %Y"),
            "muted",
        )
        hero_layout.addWidget(self.today_date)
        layout.addWidget(hero)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)

        journal_card, journal_layout = self.make_card("card")
        journal_layout.addWidget(self.label("Journal", "cardTitle"))
        journal_layout.addWidget(
            self.label(
                "Keep the moments, thoughts and lessons worth remembering.",
                "muted",
            )
        )

        self.journal_count = self.label("0 saved entries", "eyebrow")
        journal_layout.addWidget(self.journal_count)

        journal_open = QPushButton("Open journal")
        journal_open.clicked.connect(lambda: self.show_page("journal"))
        journal_layout.addWidget(journal_open)

        goals_card, goals_layout = self.make_card("terraCard")
        goals_layout.addWidget(self.label("Goals", "cardTitle"))
        goals_layout.addWidget(
            self.label(
                "Give your intentions a place to become plans.",
                "muted",
            )
        )

        self.goal_count = self.label("0 active goals", "eyebrow")
        goals_layout.addWidget(self.goal_count)

        goals_open = QPushButton("View goals")
        goals_open.setObjectName("terraButton")
        goals_open.clicked.connect(lambda: self.show_page("goals"))
        goals_layout.addWidget(goals_open)

        cards_row.addWidget(journal_card, 1)
        cards_row.addWidget(goals_card, 1)
        layout.addLayout(cards_row)

        tasks_card, tasks_layout = self.make_card("card")

        tasks_header = QHBoxLayout()
        tasks_header.addWidget(self.label("Your tasks", "cardTitle"))
        tasks_header.addStretch()

        self.task_count = self.label("0 complete", "muted")
        tasks_header.addWidget(self.task_count)
        tasks_layout.addLayout(tasks_header)

        add_row = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText(
            "One thing you want to get done..."
        )
        self.task_input.returnPressed.connect(self.add_task)

        add_task_button = QPushButton("Add task")
        add_task_button.clicked.connect(self.add_task)

        add_row.addWidget(self.task_input, 1)
        add_row.addWidget(add_task_button)
        tasks_layout.addLayout(add_row)

        self.task_list_layout = QVBoxLayout()
        self.task_list_layout.setSpacing(7)
        tasks_layout.addLayout(self.task_list_layout)
        layout.addWidget(tasks_card)

        recent_card, recent_layout = self.make_card("card")
        recent_layout.addWidget(self.label("Recently saved", "cardTitle"))

        self.recent_layout = QVBoxLayout()
        self.recent_layout.setSpacing(8)
        recent_layout.addLayout(self.recent_layout)
        layout.addWidget(recent_card)

        layout.addStretch()
        return self.scroll_page(content)

    def build_journal_page(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 4, 8, 8)
        layout.setSpacing(14)

        layout.addLayout(
            self.page_heading(
                "Keep a record",
                "Your journal",
                "Save an entry today and come back to it whenever you need.",
            )
        )

        editor_card, editor_layout = self.make_card("card")

        editor_layout.addWidget(self.label("ENTRY TITLE", "eyebrow"))

        self.journal_title = QLineEdit()
        self.journal_title.setPlaceholderText("Give this entry a title")
        editor_layout.addWidget(self.journal_title)

        editor_layout.addWidget(self.label("YOUR THOUGHTS", "eyebrow"))

        self.journal_text = QTextEdit()
        self.journal_text.setPlaceholderText(
            "Write freely. This space is yours..."
        )
        self.journal_text.setMinimumHeight(180)
        editor_layout.addWidget(self.journal_text)

        buttons = QHBoxLayout()

        self.journal_status = self.label(
            "Entries are saved on this device.",
            "muted",
        )
        buttons.addWidget(self.journal_status, 1)

        new_button = QPushButton("New entry")
        new_button.setObjectName("secondary")
        new_button.clicked.connect(self.new_journal_entry)

        save_button = QPushButton("Save entry")
        save_button.clicked.connect(self.save_journal_entry)

        buttons.addWidget(new_button)
        buttons.addWidget(save_button)
        editor_layout.addLayout(buttons)
        layout.addWidget(editor_card)

        history_card, history_layout = self.make_card("card")
        history_layout.addWidget(
            self.label("Previous entries", "cardTitle")
        )

        self.journal_history = QListWidget()
        self.journal_history.setMinimumHeight(140)
        self.journal_history.itemClicked.connect(
            self.load_journal_entry
        )
        history_layout.addWidget(self.journal_history)

        history_buttons = QHBoxLayout()
        history_buttons.addStretch()

        delete_button = QPushButton("Delete selected entry")
        delete_button.setObjectName("danger")
        delete_button.clicked.connect(self.delete_journal_entry)

        history_buttons.addWidget(delete_button)
        history_layout.addLayout(history_buttons)
        layout.addWidget(history_card)

        layout.addStretch()
        return self.scroll_page(content)

    def build_goals_page(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 4, 8, 8)
        layout.setSpacing(14)

        layout.addLayout(
            self.page_heading(
                "Be intentional",
                "Goals that matter",
                "Keep your next steps visible and mark progress as you go.",
            )
        )

        add_card, add_layout = self.make_card("terraCard")
        add_layout.addWidget(self.label("ADD A GOAL", "eyebrow"))

        row = QHBoxLayout()

        self.goal_input = QLineEdit()
        self.goal_input.setPlaceholderText(
            "What do you want to work towards?"
        )
        self.goal_input.returnPressed.connect(self.add_goal)

        self.goal_category_input = QComboBox()
        self.goal_category_input.addItems(
            ["Short term", "Medium term", "Long term"]
        )

        add_button = QPushButton("Add goal")
        add_button.setObjectName("terraButton")
        add_button.clicked.connect(self.add_goal)

        row.addWidget(self.goal_input, 1)
        row.addWidget(self.goal_category_input)
        row.addWidget(add_button)
        add_layout.addLayout(row)
        layout.addWidget(add_card)

        goals_card, goals_layout = self.make_card("card")
        goals_layout.addWidget(self.label("YOUR GOALS", "cardTitle"))

        self.goals_list_layout = QVBoxLayout()
        self.goals_list_layout.setSpacing(8)
        goals_layout.addLayout(self.goals_list_layout)
        layout.addWidget(goals_card)

        layout.addStretch()
        return self.scroll_page(content)

    def build_reflection_page(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 4, 8, 8)
        layout.setSpacing(14)

        layout.addLayout(
            self.page_heading(
                "Pause and notice",
                "A moment to reflect",
                "Who are you becoming through the choices you're making today?",
            )
        )

        editor_card, editor_layout = self.make_card("hero")
        editor_layout.addWidget(
            self.label("TODAY'S REFLECTION", "eyebrow")
        )

        self.reflection_text = QTextEdit()
        self.reflection_text.setPlaceholderText(
            "What did today teach you? What are you proud of? "
            "What would you like to do differently?"
        )
        self.reflection_text.setMinimumHeight(200)
        editor_layout.addWidget(self.reflection_text)

        row = QHBoxLayout()

        self.reflection_status = self.label(
            "Your reflections stay on this device.",
            "muted",
        )
        row.addWidget(self.reflection_status, 1)

        save_button = QPushButton("Save reflection")
        save_button.clicked.connect(self.save_reflection)
        row.addWidget(save_button)

        editor_layout.addLayout(row)
        layout.addWidget(editor_card)

        history_card, history_layout = self.make_card("card")
        history_layout.addWidget(
            self.label("Past reflections", "cardTitle")
        )

        self.reflection_history = QListWidget()
        self.reflection_history.setMinimumHeight(170)
        self.reflection_history.itemClicked.connect(
            self.load_reflection
        )
        history_layout.addWidget(self.reflection_history)

        row = QHBoxLayout()
        row.addStretch()

        delete_button = QPushButton("Delete selected reflection")
        delete_button.setObjectName("danger")
        delete_button.clicked.connect(self.delete_reflection)
        row.addWidget(delete_button)

        history_layout.addLayout(row)
        layout.addWidget(history_card)

        layout.addStretch()
        return self.scroll_page(content)

    def label(self, text, object_name=None):
        label = QLabel(text)

        if object_name:
            label.setObjectName(object_name)

        label.setWordWrap(True)
        return label

    def show_page(self, key):
        self.pages.setCurrentIndex(self.page_indices[key])

        for name, button in self.nav_buttons.items():
            button.setProperty("active", name == key)
            button.style().unpolish(button)
            button.style().polish(button)

        if key == "journal":
            self.refresh_journal_history()
        elif key == "goals":
            self.refresh_goals()
        elif key == "reflection":
            self.refresh_reflection_history()
        elif key == "home":
            self.refresh_home()

    def refresh_all(self):
        self.refresh_journal_history()
        self.refresh_reflection_history()
        self.refresh_goals()
        self.refresh_home()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)

    def refresh_home(self):
        entries_count = len(self.store.entries("journal"))
        goals = self.store.goals()
        tasks = self.store.tasks()

        completed_goals = sum(
            1 for goal in goals if goal["completed_at"]
        )
        completed_tasks = sum(
            1 for task in tasks if task["completed_at"]
        )

        self.journal_count.setText(
            f"{entries_count} saved "
            f"{'entry' if entries_count == 1 else 'entries'}"
        )
        self.goal_count.setText(
            f"{len(goals) - completed_goals} active goals"
        )
        self.task_count.setText(
            f"{completed_tasks} of {len(tasks)} complete"
        )

        self.clear_layout(self.task_list_layout)

        if not tasks:
            self.task_list_layout.addWidget(
                self.label(
                    "Your task list is clear. Add one small step above.",
                    "muted",
                )
            )

        for task in tasks:
            row = QHBoxLayout()

            check = QCheckBox(task["title"])
            check.setChecked(bool(task["completed_at"]))
            check.stateChanged.connect(
                lambda state, task_id=task["id"]:
                self.toggle_task(
                    task_id,
                    state == Qt.CheckState.Checked.value,
                )
            )
            row.addWidget(check, 1)

            if task["completed_at"]:
                row.addWidget(
                    self.label(
                        f"Completed {format_timestamp(task['completed_at'])}",
                        "timestamp",
                    )
                )

            edit_button = QPushButton("Edit")
            edit_button.setObjectName("secondary")
            edit_button.setFixedWidth(68)
            edit_button.clicked.connect(
                lambda checked=False, task_id=task["id"],
                title=task["title"]: self.edit_task(task_id, title)
            )
            row.addWidget(edit_button)

            delete_button = QPushButton("Remove")
            delete_button.setObjectName("danger")
            delete_button.setFixedWidth(112)
            delete_button.clicked.connect(
                lambda checked=False, task_id=task["id"]:
                self.delete_task(task_id)
            )
            row.addWidget(delete_button)

            self.task_list_layout.addLayout(row)

        self.clear_layout(self.recent_layout)

        recent = sorted(
            self.store.entries("journal")
            + self.store.entries("reflection"),
            key=lambda item: item["updated_at"],
            reverse=True,
        )[:3]

        if not recent:
            self.recent_layout.addWidget(
                self.label(
                    "Your saved entries will appear here.",
                    "muted",
                )
            )

        for entry in recent:
            title = entry["title"] or (
                "Daily reflection"
                if entry["kind"] == "reflection"
                else "Journal entry"
            )

            row = QHBoxLayout()
            details = QVBoxLayout()

            details.addWidget(self.label(title, "cardTitle"))
            details.addWidget(
                self.label(
                    f"{entry['kind'].title()} · "
                    f"{format_timestamp(entry['updated_at'])}",
                    "timestamp",
                )
            )

            row.addLayout(details, 1)

            open_button = QPushButton("Open")
            open_button.setObjectName("secondary")
            open_button.clicked.connect(
                lambda checked=False,
                entry_id=entry["id"],
                kind=entry["kind"]:
                self.open_recent_entry(entry_id, kind)
            )
            row.addWidget(open_button)

            self.recent_layout.addLayout(row)

    def add_task(self):
        title = self.task_input.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Task needed",
                "Please enter a task first.",
            )
            return

        self.store.add_task(title)
        self.task_input.clear()
        self.refresh_home()

    def toggle_task(self, task_id, completed):
        self.store.set_task_completed(task_id, completed)
        self.refresh_home()

    def edit_task(self, task_id, current_title):
        title, accepted = QInputDialog.getText(
            self, "Edit task", "Task", text=current_title
        )
        title = title.strip()

        if accepted and title:
            self.store.update_task_title(task_id, title)
            self.refresh_home()

    def delete_task(self, task_id):
        self.store.delete_task(task_id)
        self.refresh_home()

    def new_journal_entry(self):
        self.current_entry_id = None
        self.current_entry_kind = "journal"
        self.journal_title.clear()
        self.journal_text.clear()
        self.journal_status.setText("New entry · not saved yet")
        self.journal_history.clearSelection()

    def save_journal_entry(self):
        title = self.journal_title.text().strip()
        content = self.journal_text.toPlainText().strip()

        if not content:
            QMessageBox.warning(
                self,
                "Entry needed",
                "Please write something before saving your entry.",
            )
            return

        if not title:
            title = datetime.now().strftime(
                "Entry · %d %B %Y"
            )
            self.journal_title.setText(title)

        self.current_entry_id = self.store.save_entry(
            "journal",
            title,
            content,
            self.current_entry_id,
        )

        saved = self.store.entry(self.current_entry_id)

        self.journal_status.setText(
            f"Saved {format_timestamp(saved['updated_at'])}"
        )

        self.refresh_journal_history()
        self.refresh_home()

    def refresh_journal_history(self):
        if not hasattr(self, "journal_history"):
            return

        self.journal_history.clear()

        for entry in self.store.entries("journal"):
            item = QListWidgetItem(
                f"{entry['title'] or 'Journal entry'}\n"
                f"Updated {format_timestamp(entry['updated_at'])}"
            )
            item.setData(Qt.ItemDataRole.UserRole, entry["id"])
            self.journal_history.addItem(item)

    def load_journal_entry(self, item):
        entry = self.store.entry(
            item.data(Qt.ItemDataRole.UserRole)
        )

        if not entry or entry["kind"] != "journal":
            return

        self.current_entry_id = entry["id"]
        self.current_entry_kind = "journal"
        self.journal_title.setText(entry["title"])
        self.journal_text.setPlainText(entry["content"])
        self.journal_status.setText(
            f"Last saved {format_timestamp(entry['updated_at'])}"
        )

    def delete_journal_entry(self):
        item = self.journal_history.currentItem()

        if not item:
            QMessageBox.information(
                self,
                "Choose an entry",
                "Select a journal entry to delete.",
            )
            return

        answer = QMessageBox.question(
            self,
            "Delete entry",
            "Delete this journal entry permanently?",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        entry_id = item.data(Qt.ItemDataRole.UserRole)
        self.store.delete_entry(entry_id)

        if self.current_entry_id == entry_id:
            self.new_journal_entry()

        self.refresh_journal_history()
        self.refresh_home()

    def add_goal(self):
        title = self.goal_input.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Goal needed",
                "Please enter a goal first.",
            )
            return

        self.store.add_goal(title, self.goal_category_input.currentText())
        self.goal_input.clear()
        self.refresh_goals()
        self.refresh_home()

    def refresh_goals(self):
        if not hasattr(self, "goals_list_layout"):
            return

        self.clear_layout(self.goals_list_layout)
        goals = self.store.goals()
        categories = ("Short term", "Medium term", "Long term")

        if not goals:
            self.goals_list_layout.addWidget(
                self.label(
                    "Your goals will live here. "
                    "Start with one that matters to you.",
                    "muted",
                )
            )

        for category in categories:
            self.goals_list_layout.addWidget(
                self.label(category.upper(), "eyebrow")
            )
            category_goals = [g for g in goals if g["category"] == category]
            if not category_goals:
                self.goals_list_layout.addWidget(
                    self.label("No goals in this category yet.", "muted")
                )

            for goal in category_goals:
                row = QHBoxLayout()

                check = QCheckBox(goal["title"])
                check.setChecked(bool(goal["completed_at"]))
                check.stateChanged.connect(
                    lambda state, goal_id=goal["id"]:
                    self.toggle_goal(
                        goal_id,
                        state == Qt.CheckState.Checked.value,
                    )
                )
                row.addWidget(check, 1)

                category_picker = QComboBox()
                category_picker.addItems(categories)
                category_picker.setCurrentText(category)
                category_picker.currentTextChanged.connect(
                    lambda value, goal_id=goal["id"]:
                    self.change_goal_category(goal_id, value)
                )
                row.addWidget(category_picker)

                if goal["completed_at"]:
                    row.addWidget(
                        self.label(
                            f"Completed {format_timestamp(goal['completed_at'])}",
                            "timestamp",
                        )
                    )

                delete_button = QPushButton("Remove")
                delete_button.setObjectName("danger")
                delete_button.setFixedWidth(112)
                delete_button.clicked.connect(
                    lambda checked=False, goal_id=goal["id"]:
                    self.delete_goal(goal_id)
                )
                row.addWidget(delete_button)

                self.goals_list_layout.addLayout(row)

    def change_goal_category(self, goal_id, category):
        self.store.set_goal_category(goal_id, category)
        self.refresh_goals()

    def toggle_goal(self, goal_id, completed):
        self.store.set_goal_completed(goal_id, completed)
        self.refresh_goals()
        self.refresh_home()

    def delete_goal(self, goal_id):
        self.store.delete_goal(goal_id)
        self.refresh_goals()
        self.refresh_home()

    def save_reflection(self):
        content = self.reflection_text.toPlainText().strip()

        if not content:
            QMessageBox.warning(
                self,
                "Reflection needed",
                "Please write a reflection before saving.",
            )
            return

        entry_id = self.store.save_entry(
            "reflection",
            "Daily reflection",
            content,
        )

        entry = self.store.entry(entry_id)

        self.reflection_status.setText(
            f"Saved {format_timestamp(entry['updated_at'])}"
        )

        self.refresh_reflection_history()
        self.refresh_home()

    def refresh_reflection_history(self):
        if not hasattr(self, "reflection_history"):
            return

        self.reflection_history.clear()

        for entry in self.store.entries("reflection"):
            preview = " ".join(entry["content"].split())

            if len(preview) > 90:
                preview = preview[:87].rstrip() + "..."

            item = QListWidgetItem(
                f"{format_timestamp(entry['created_at'])}\n{preview}"
            )
            item.setData(Qt.ItemDataRole.UserRole, entry["id"])
            self.reflection_history.addItem(item)

    def load_reflection(self, item):
        entry = self.store.entry(
            item.data(Qt.ItemDataRole.UserRole)
        )

        if not entry or entry["kind"] != "reflection":
            return

        self.reflection_text.setPlainText(entry["content"])
        self.reflection_status.setText(
            f"Saved {format_timestamp(entry['updated_at'])}"
        )

    def delete_reflection(self):
        item = self.reflection_history.currentItem()

        if not item:
            QMessageBox.information(
                self,
                "Choose a reflection",
                "Select a reflection to delete.",
            )
            return

        answer = QMessageBox.question(
            self,
            "Delete reflection",
            "Delete this reflection permanently?",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.store.delete_entry(
            item.data(Qt.ItemDataRole.UserRole)
        )

        self.reflection_text.clear()
        self.reflection_status.setText(
            "Your reflections stay on this device."
        )

        self.refresh_reflection_history()
        self.refresh_home()

    def open_recent_entry(self, entry_id, kind):
        entry = self.store.entry(entry_id)

        if not entry:
            return

        if kind == "journal":
            self.show_page("journal")
            self.current_entry_id = entry_id
            self.journal_title.setText(entry["title"])
            self.journal_text.setPlainText(entry["content"])
            self.journal_status.setText(
                f"Last saved {format_timestamp(entry['updated_at'])}"
            )

            for index in range(self.journal_history.count()):
                item = self.journal_history.item(index)

                if item.data(Qt.ItemDataRole.UserRole) == entry_id:
                    self.journal_history.setCurrentItem(item)
                    break

        else:
            self.show_page("reflection")
            self.reflection_text.setPlainText(entry["content"])
            self.reflection_status.setText(
                f"Saved {format_timestamp(entry['updated_at'])}"
            )

            for index in range(self.reflection_history.count()):
                item = self.reflection_history.item(index)

                if item.data(Qt.ItemDataRole.UserRole) == entry_id:
                    self.reflection_history.setCurrentItem(item)
                    break

    def closeEvent(self, event):
        self.store.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Future Self")

    window = FutureSelfWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
