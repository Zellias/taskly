import flet as ft
import sqlite3
import datetime

class TaskApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Developer's Task Management System"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.window_width = 1200
        self.page.window_height = 800

        # Set up the database
        self.conn = sqlite3.connect('tasks.db')
        self.create_table()

        # Set up the UI
        self.setup_ui()

        # Ensure database closes when the app exits
        self.page.on_close = self.on_close

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks
        (id INTEGER PRIMARY KEY,
         title TEXT,
         description TEXT,
         due_date TEXT,
         deadline TEXT,
         priority TEXT,
         status TEXT,
         tags TEXT,
         estimated_time INTEGER,
         minimum_time INTEGER)
        ''')
        self.conn.commit()

    def setup_ui(self):
        # Create main layout
        self.main_layout = ft.Row(
            expand=True,
            controls=[
                self.create_task_column("Not Started"),
                self.create_task_column("In Progress"),
                self.create_task_column("Completed")
            ]
        )

        # Add task button
        add_button = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=self.show_add_task_dialog,
            bgcolor=ft.colors.BLUE
        )

        # Search bar
        self.search_field = ft.TextField(
            label="Search tasks",
            on_change=self.search_tasks,
            expand=True,
            prefix_icon=ft.icons.SEARCH,
            border_radius=20
        )

        # Main content
        self.page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Row([self.search_field], alignment=ft.MainAxisAlignment.CENTER),
                        padding=10
                    ),
                    self.main_layout
                ],
                expand=True
            )
        )
        self.page.add(add_button)

        # Refresh task list
        self.refresh_tasks()

    def create_task_column(self, title):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column([], scroll=ft.ScrollMode.AUTO),
                        padding=10,
                        expand=True
                    )
                ],
                expand=True
            ),
            border_radius=10,
            padding=10,
            expand=True,
            border=ft.border.all(1, ft.colors.OUTLINE_VARIANT)
        )

    def create_task_card(self, task):
        def change_status(e):
            new_status = e.control.value
            self.update_task_status(task[0], task[1], new_status)

        def delete_task(e):
            self.delete_task(task[0], task[1])

        def toggle_description(e):
            description_text.visible = not description_text.visible
            self.page.update()

        status_options = ["Not Started", "In Progress", "Completed"]
        
        description_text = ft.Text(task[5], visible=False, size=12)

        estimated_time = task[7] if len(task) > 7 else "N/A"
        minimum_time = task[8] if len(task) > 8 else "N/A"

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.TASK_ALT),
                        title=ft.Text(task[0], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Due: {task[1]} | Deadline: {task[2]}", size=12),
                        trailing=ft.PopupMenuButton(
                            icon=ft.icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="Delete", on_click=delete_task, icon=ft.icons.DELETE)
                            ]
                        )
                    ),
                    ft.Divider(height=1),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.FLAG, size=16),
                                ft.Text(f"Priority: {task[3]}", size=14)
                            ]),
                            ft.Row([
                                ft.Icon(ft.icons.LABEL, size=16),
                                ft.Text(f"Tags: {task[6]}", size=14)
                            ]),
                            ft.Row([
                                ft.Icon(ft.icons.TIMER, size=16),
                                ft.Text(f"Est. Time: {estimated_time} hrs, Min. Time: {minimum_time} hrs", size=14)
                            ]),
                            ft.Dropdown(
                                label="Status",
                                value=task[4],
                                options=[ft.dropdown.Option(status) for status in status_options],
                                on_change=change_status,
                                width=200
                            ),
                            ft.TextButton("Show/Hide Description", on_click=toggle_description, icon=ft.icons.DESCRIPTION),
                            description_text
                        ]),
                        padding=10
                    )
                ]),
                padding=5
            ),
            elevation=2,
            margin=5
        )

    def show_add_task_dialog(self, e):
        def save_task(e):
            title = title_field.value
            description = description_field.value
            due_date = due_date_field.value
            deadline = deadline_field.value
            priority = priority_dropdown.value
            status = status_dropdown.value
            tags = tags_field.value
            estimated_time = estimated_time_field.value
            minimum_time = minimum_time_field.value

            if title and due_date and deadline and priority and status and estimated_time and minimum_time:
                cursor = self.conn.cursor()
                cursor.execute('''
                INSERT INTO tasks (title, description, due_date, deadline, priority, status, tags, estimated_time, minimum_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, description, due_date, deadline, priority, status, tags, estimated_time, minimum_time))
                self.conn.commit()
                self.refresh_tasks()
                dialog.open = False
                self.page.update()
            else:
                self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Please fill in all required fields.")))

        title_field = ft.TextField(label="Title", autofocus=True)
        description_field = ft.TextField(label="Description", multiline=True)
        due_date_field = ft.TextField(label="Due Date", value=datetime.date.today().strftime("%Y-%m-%d"))
        deadline_field = ft.TextField(label="Deadline", value=datetime.date.today().strftime("%Y-%m-%d"))
        priority_dropdown = ft.Dropdown(
            label="Priority",
            options=[
                ft.dropdown.Option("Low"),
                ft.dropdown.Option("Medium"),
                ft.dropdown.Option("High")
            ],
            value="Medium"
        )
        status_dropdown = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Not Started"),
                ft.dropdown.Option("In Progress"),
                ft.dropdown.Option("Completed")
            ],
            value="Not Started"
        )
        tags_field = ft.TextField(label="Tags")
        estimated_time_field = ft.TextField(label="Estimated Time (hours)", keyboard_type=ft.KeyboardType.NUMBER)
        minimum_time_field = ft.TextField(label="Minimum Time (hours)", keyboard_type=ft.KeyboardType.NUMBER)

        dialog = ft.AlertDialog(
            title=ft.Text("Add New Task"),
            content=ft.Column([
                title_field,
                description_field,
                due_date_field,
                deadline_field,
                priority_dropdown,
                status_dropdown,
                tags_field,
                estimated_time_field,
                minimum_time_field
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(dialog, 'open', False)),
                ft.TextButton("Save", on_click=save_task)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def refresh_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT title, due_date, deadline, priority, status, description, tags, estimated_time, minimum_time FROM tasks ORDER BY due_date")
        tasks = cursor.fetchall()

        for column in self.main_layout.controls:
            task_list = column.content.controls[1].content
            task_list.controls.clear()

        for task in tasks:
            task_card = self.create_task_card(task)
            if task[4] == "Not Started":
                self.main_layout.controls[0].content.controls[1].content.controls.append(task_card)
            elif task[4] == "In Progress":
                self.main_layout.controls[1].content.controls[1].content.controls.append(task_card)
            elif task[4] == "Completed":
                self.main_layout.controls[2].content.controls[1].content.controls.append(task_card)

        self.page.update()

    def update_task_status(self, title, due_date, new_status):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE tasks
        SET status=?
        WHERE title=? AND due_date=?
        ''', (new_status, title, due_date))
        self.conn.commit()
        self.refresh_tasks()

    def delete_task(self, title, due_date):
        def confirm_delete(e):
            cursor = self.conn.cursor()
            cursor.execute('''
            DELETE FROM tasks
            WHERE title=? AND due_date=?
            ''', (title, due_date))
            self.conn.commit()
            self.refresh_tasks()
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(f"Are you sure you want to delete the task '{title}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page.dialog, 'open', False)),
                ft.TextButton("Delete", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def search_tasks(self, e):
        search_term = self.search_field.value.lower()
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT title, due_date, deadline, priority, status, description, tags, estimated_time, minimum_time
        FROM tasks 
        WHERE LOWER(title) LIKE ? OR LOWER(description) LIKE ? OR LOWER(tags) LIKE ?
        ORDER BY due_date
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        tasks = cursor.fetchall()

        for column in self.main_layout.controls:
            task_list = column.content.controls[1].content
            task_list.controls.clear()

        for task in tasks:
            task_card = self.create_task_card(task)
            if task[4] == "Not Started":
                self.main_layout.controls[0].content.controls[1].content.controls.append(task_card)
            elif task[4] == "In Progress":
                self.main_layout.controls[1].content.controls[1].content.controls.append(task_card)
            elif task[4] == "Completed":
                self.main_layout.controls[2].content.controls[1].content.controls.append(task_card)

        self.page.update()

    def on_close(self, e):
        # Close the database connection when app is closed
        self.conn.close()

def main(page: ft.Page):
    app = TaskApp(page)

ft.app(target=main)
