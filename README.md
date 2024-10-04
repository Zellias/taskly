# Taskly - Developer's Task Management System

Welcome to Taskly, a powerful task management tool designed for developers. Taskly helps you keep track of your tasks, prioritize work, and manage your time efficiently, all from a modern, responsive user interface powered by Flet. Whether you're managing a few tasks or a complex project, Taskly has you covered.

Features:

- Add, Edit, Delete Tasks: Create new tasks, edit existing ones, or remove them when completed.
- Task Columns: Tasks are organized into columns: Not Started, In Progress, and Completed for better visualization.
- Status Update: Change task status to track progress.
- Task Priority and Tags: Set priority levels and add tags for better categorization.
- Search Functionality: Easily search for tasks using keywords.
- Estimated and Minimum Time Tracking: Track estimated and minimum times for each task.
- Dark Mode UI: Enjoy a sleek, dark mode user interface for comfortable use at any time of the day.

Getting Started:

Prerequisites:
- Python 3.7 or later
- Flet (`pip install flet`)
- SQLite3 (usually comes pre-installed with Python)

Installation:
1. Clone the repository:
   git clone https://github.com/Zellias/taskly.git
   cd taskly

2. Install the required dependencies:
   pip install flet

3. Run the app:
   python taskly.py

Usage:
Once you run the application, you'll see a window with columns for different task statuses:

- Not Started: Tasks that are yet to begin.
- In Progress: Tasks that you are currently working on.
- Completed: Tasks that have been completed.

You can:
- Click on the + icon to add a new task.
- Use the dropdown menu to change the status of a task.
- Use the search bar at the top to find tasks by title, description, or tags.

Database:
The app uses SQLite as the underlying database to store tasks. This means all your tasks are saved locally to `tasks.db` in the same directory.

Adding a Task:
Click on the + icon in the bottom right corner to add a new task. A dialog will appear where you can enter:

- Title
- Description
- Due Date
- Deadline
- Priority (Low, Medium, High)
- Status (Not Started, In Progress, Completed)
- Tags
- Estimated Time (in hours)
- Minimum Time (in hours)

Deleting a Task:
To delete a task, click on the "More Options" (⋮) button on the task card and select Delete.

Technologies Used:
- Flet: A UI framework for creating interactive web apps in Python.
- SQLite: A lightweight database for storing task data.

Contributing:
Contributions are welcome! If you'd like to add new features, fix bugs, or improve documentation:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m 'Add my feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a Pull Request.

Please make sure to update tests as appropriate.

License:
This project is licensed under the MIT License - see the LICENSE file for details.

Contact:
If you have any questions or suggestions, feel free to contact me:

- GitHub: [Zellias](https://github.com/Zellias)

Happy Tasking!
