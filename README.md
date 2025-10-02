A simple Python-based task manager for creating, editing, and completing tasks.

## Features

## Tech Stack

## How to Run
1. Clone this repo: `git clone https://github.com/techlab-jd/task-manager-cli`
2. Run: `python run.py`

## Screenshot


# Task-Manager-CLI

An interactive, colorful command-line task manager built with Python.

## Features
- Add, edit, and delete tasks
- Mark tasks as complete/incomplete
- Set task priority and due date
- Colorful, readable table display (using `rich`)
- All data stored in `data/tasks.json`

## Requirements
- Python 3.8+
- Install dependencies:
  ```sh
  pip install rich
  ```

## Usage
1. Clone the repo:
	```sh
	git clone https://github.com/techlab-jd/task-manager-cli
	cd task-manager-cli
	```
2. Run the CLI:
	```sh
	python run.py
	```

## Example
```
[A]dd [E]dit [D]elete [Q]uit
Choose an action: a
Enter task title: Write docs
Enter description (optional): For GitHub
Priority (low/medium/high): high
Due date (optional): tomorrow
Task added!
```

## License
MIT
