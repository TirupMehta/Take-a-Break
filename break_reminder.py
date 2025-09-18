import sys
import os
import json
from datetime import date
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QSystemTrayIcon, QMenu, QAction, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation

# --- State Management for Snooze Feature ---
STATE_FILE = os.path.join(os.path.expanduser('~'), '.break_reminder_state.json')

def load_snooze_state():
    """Loads the snooze count and resets it if it's a new day."""
    today = date.today().isoformat()
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        if state.get('date') == today:
            return state.get('count', 0)
        else:
            return 0
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_snooze_state(count):
    """Saves the snooze count for the current day."""
    today = date.today().isoformat()
    state = {'date': today, 'count': count}
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

# --- Main Application ---
class BreakOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.can_close = False

        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setStyleSheet("background-color: rgba(0, 0, 0, 230);")
        self.setGeometry(0, 0, QApplication.primaryScreen().size().width(),
                         QApplication.primaryScreen().size().height())

        # --- Layout and Styling ---
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Time to Take a Break")
        self.label.setFont(QFont("Segoe UI", 50, QFont.Bold))
        self.label.setStyleSheet("color: #FFFFFF;")
        shadow = QGraphicsDropShadowEffect(blurRadius=15, color=QColor(0, 0, 0, 150))
        self.label.setGraphicsEffect(shadow)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.timer_label = QLabel("2:00")
        self.timer_label.setFont(QFont("Segoe UI", 35))
        self.timer_label.setStyleSheet("color: #E0E0E0;")
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.snooze_button = QPushButton()
        self.snooze_button.setMinimumWidth(300) # Increased width for new text
        self.snooze_button.setStyleSheet("""
            QPushButton { background-color: #ff8c00; color: white; padding: 15px; border-radius: 12px; font-size: 18px; }
            QPushButton:disabled { background-color: #555555; }
        """)
        self.snooze_button.clicked.connect(self.snooze_break)
        button_layout.addWidget(self.snooze_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setEnabled(False)
        self.quit_button.setMinimumWidth(300)
        self.quit_button.setStyleSheet("""
            QPushButton { background-color: #555555; color: white; padding: 15px; border-radius: 12px; font-size: 18px; }
            QPushButton:enabled { background-color: #4CAF50; }
        """)
        self.quit_button.clicked.connect(self.close_overlay)
        button_layout.addWidget(self.quit_button)
        
        layout.addLayout(button_layout)

        self.copyright_label = QLabel("© Tirup Mehta")
        self.copyright_label.setFont(QFont("Segoe UI", 10))
        self.copyright_label.setStyleSheet("color: #AAAAAA;")
        layout.addStretch()
        layout.addWidget(self.copyright_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_timer)
        self.animation = QPropertyAnimation(self, b"windowOpacity", duration=500, startValue=0, endValue=1)
        self.snooze_timer = QTimer(self)
        self.snooze_timer.setSingleShot(True)
        self.snooze_timer.timeout.connect(self.show_overlay)

    def show_overlay(self):
        self.can_close = False
        snooze_count = load_snooze_state()
        remaining_snoozes = 3 - snooze_count
        
        self.snooze_button.setText(f"Snooze (1 hour) ({remaining_snoozes} left today)")
        self.snooze_button.setEnabled(snooze_count < 3)

        self.setWindowOpacity(0)
        self.remaining_seconds = 120
        self.quit_button.setEnabled(False)
        self.quit_button.setText("Quit (Available after timer)")
        self.update_timer_label()
        self.countdown_timer.start(1000)
        
        self.showFullScreen()
        self.animation.start()
        
        # This brings the window to the front and makes it the active one.
        # It's less aggressive than grabbing the mouse but still very effective.
        self.activateWindow()

    def update_timer(self):
        self.remaining_seconds -= 1
        self.update_timer_label()
        if self.remaining_seconds <= 0:
            self.countdown_timer.stop()
            self.can_close = True
            self.quit_button.setEnabled(True)
            self.quit_button.setText("Quit Break Screen")

    def update_timer_label(self):
        self.timer_label.setText(f"{self.remaining_seconds // 60}:{self.remaining_seconds % 60:02d}")
        
    def close_overlay(self):
        self.countdown_timer.stop()
        self.hide()

    def snooze_break(self):
        current_count = load_snooze_state()
        if current_count < 3:
            save_snooze_state(current_count + 1)
            self.hide()
            # Snooze for 1 hour (3600 seconds * 1000 milliseconds)
            self.snooze_timer.start(3600 * 1000)

    def closeEvent(self, event):
        # This event is triggered by things like Alt+F4
        if self.can_close:
            event.accept() # Allow closing
        else:
            event.ignore() # Block closing

class BreakReminderApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.overlay = BreakOverlay()

        self.tray_icon = QSystemTrayIcon(QIcon.fromTheme("face-smile"), self.app)
        menu = QMenu()
        show_action = QAction("Show Break Now", triggered=self.overlay.show_overlay)
        exit_action = QAction("Exit App", triggered=self.app.quit)
        menu.addAction(show_action)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.setToolTip("Break Reminder")
        self.tray_icon.show()

        self.main_timer = QTimer()
        self.main_timer.timeout.connect(self.overlay.show_overlay)
        self.main_timer.start(3600 * 1000) # 1 hour

        # --- FOR TESTING: Show break 2 minutes after start. ---
        QTimer.singleShot(120 * 1000, self.overlay.show_overlay)
        
        print("Break Reminder App is running. A test break will appear in 2 minutes.")

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app_instance = BreakReminderApp()
    app_instance.run()