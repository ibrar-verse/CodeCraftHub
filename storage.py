import json
import os

# Define the relative path to the storage file
DATA_FILE = "courses.json"


def load_courses():
  """Reads and returns the list of courses from courses.json.

  Returns an empty list if the file does not exist or contains invalid JSON.
  """
  # Guard clause: check if the file exists on disk
  if not os.path.exists(DATA_FILE):
    return []

  try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except (json.JSONDecodeError, OSError):
    # Handles empty files or corrupted JSON syntax safely
    return []


def save_courses(courses):
  """Overwrites courses.json with the provided list of courses."""
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    # indent=2 formats the JSON with indentation for readability
    json.dump(courses, f, indent=2)


def get_next_id(courses):
  """Calculates an auto-incrementing ID.

  Returns 1 if no courses exist; otherwise, increments the highest existing ID.
  """
  if not courses:
    return 1
  return max(course["id"] for course in courses) + 1