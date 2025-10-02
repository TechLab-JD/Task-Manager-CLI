from datetime import datetime
import json
from typing import Optional, Dict, Any

class Task:
	"""
	Represents a single task in the Task Manager CLI.
	"""
	def __init__(self, id: str, title: str, description: str = "", status: bool = False,
				 priority: str = "low", created_at: Optional[str] = None,
				 updated_on: Optional[str] = None, due_date: Optional[str] = None):
		self.id = id
		self.title = title
		self.description = description
		self.status = status
		self.priority = priority
		self.created_at = created_at or datetime.utcnow().isoformat()
		self.updated_on = updated_on
		self.due_date = due_date

	def mark_complete(self) -> None:
		"""Mark the task as complete and update timestamp."""
		self.status = True
		self.updated_on = datetime.utcnow().isoformat()
		self.save()

	def mark_incomplete(self) -> None:
		"""Mark the task as incomplete and update timestamp."""
		self.status = False
		self.updated_on = datetime.utcnow().isoformat()
		self.save()

	def set_priority(self, priority: str) -> None:
		"""Set the priority of the task."""
		input_priority = priority.lower()
		if input_priority in ["low", "medium", "high"]:
			self.priority = input_priority
			self.updated_on = datetime.utcnow().isoformat()
			self.save()
		else:
			raise ValueError("Priority must be 'low', 'medium', or 'high'.")

	def to_dict(self) -> Dict[str, Any]:
		"""Return a dictionary representation of the task."""
		return {
			"id": self.id,
			"title": self.title,
			"description": self.description,
			"status": self.status,
			"priority": self.priority,
			"created_at": self.created_at,
			"updated_on": self.updated_on,
			"due_date": self.due_date
		}

	def save(self) -> None:
		"""Save or update the task in the tasks.json file."""
		try:
			with open("data/tasks.json", "r", encoding="utf-8") as f:
				tasks = json.load(f)
		except (FileNotFoundError, json.JSONDecodeError):
			tasks = []

		for i, t in enumerate(tasks):
			if t["id"] == self.id:
				tasks[i] = self.to_dict()
				break
		else:
			tasks.append(self.to_dict())
		with open("data/tasks.json", "w", encoding="utf-8") as f:
			json.dump(tasks, f, indent=2)

	def __repr__(self):
		return f"Task(id={self.id}, title='{self.title}', status={self.status})"
