import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox

class ProductivityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productivity Tracker")
        self.setGeometry(100, 100, 400, 300)
        
        self.init_db()
        self.init_ui()
        self.load_tasks()
    
    def init_db(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
        self.conn.commit()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter a task")
        layout.addWidget(self.task_input)
        
        self.add_button = QPushButton("Add Task", self)
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)
        
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)
        
        self.complete_button = QPushButton("Mark as Completed", self)
        self.complete_button.clicked.connect(self.complete_task)
        layout.addWidget(self.complete_button)
        
        self.setLayout(layout)
    
    def load_tasks(self):
        self.task_list.clear()
        self.cursor.execute("SELECT id, task, status FROM tasks")
        for task in self.cursor.fetchall():
            status = "✓" if task[2] == "completed" else "✗"
            self.task_list.addItem(f"{task[0]}. {task[1]} [{status}]")
    
    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
            self.conn.commit()
            self.task_input.clear()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty!")
    
    def complete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_id = selected_item.text().split(".")[0]
            self.cursor.execute("UPDATE tasks SET status='completed' WHERE id=?", (task_id,))
            self.conn.commit()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Select a task to mark as completed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductivityApp()
    window.show()
    sys.exit(app.exec())
