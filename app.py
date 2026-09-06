from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from storage import get_next_id, load_courses, save_courses

app = Flask(__name__)
# Enable CORS so your Part 2 dashboard in the browser can communicate with this API
CORS(app)

ALLOWED_STATUSES = {"Not Started", "In Progress", "Completed"}


# -------------------------------------------------------------
# GET /api/courses - List all courses
# -------------------------------------------------------------
@app.route("/api/courses", methods=["GET"])
def get_all_courses():
  courses = load_courses()
  return jsonify({"success": True, "count": len(courses), "data": courses}), 200


# -------------------------------------------------------------
# GET /api/courses/<id> - Get a single course by ID
# -------------------------------------------------------------
@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_single_course(course_id):
  courses = load_courses()
  # Search the list for a course whose "id" matches course_id
  course = next((c for c in courses if c["id"] == course_id), None)

  if not course:
    return (
        jsonify({
            "success": False,
            "error": f"Course with ID {course_id} not found",
        }),
        404,
    )

  return jsonify({"success": True, "data": course}), 200

def is_valid_date(date_string):
  """Checks if a string strictly follows YYYY-MM-DD format."""
  try:
    datetime.strptime(date_string, "%Y-%m-%d")
    return True
  except (ValueError, TypeError):
    return False


# -------------------------------------------------------------
# POST /api/courses - Create a new course
# -------------------------------------------------------------
@app.route("/api/courses", methods=["POST"])
def create_course():
  data = request.get_json(silent=True)
  if not data:
    return (
        jsonify(
            {"success": False, "error": "Invalid or missing JSON payload"}
        ),
        400,
    )

  # Quality Gate 1: Check required fields
  required_fields = ["name", "description", "target_date", "status"]
  missing = [
      field
      for field in required_fields
      if field not in data or str(data[field]).strip() == ""
  ]
  if missing:
    return (
        jsonify({
            "success": False,
            "error": f"Missing required fields: {', '.join(missing)}",
        }),
        400,
    )

  # Quality Gate 2: Validate status enum
  if data["status"] not in ALLOWED_STATUSES:
    return (
        jsonify({
            "success": False,
            "error": (
                f"Invalid status '{data['status']}'. Allowed values are:"
                f" {', '.join(ALLOWED_STATUSES)}"
            ),
        }),
        400,
    )

  # Quality Gate 3: Validate target_date format
  if not is_valid_date(data["target_date"]):
    return (
        jsonify({
            "success": False,
            "error": "Invalid target_date format. Expected YYYY-MM-DD.",
        }),
        400,
    )

  # Load existing courses, generate ID, and append new record
  courses = load_courses()
  new_course = {
      "id": get_next_id(courses),
      "name": str(data["name"]).strip(),
      "description": str(data["description"]).strip(),
      "target_date": str(data["target_date"]).strip(),
      "status": data["status"],
      "created_at": datetime.utcnow().isoformat() + "Z",
  }

  courses.append(new_course)
  save_courses(courses)

  return (
      jsonify({
          "success": True,
          "message": "Course created successfully",
          "data": new_course,
      }),
      201,
  )
# -------------------------------------------------------------
# PUT /api/courses/<id> - Update an existing course
# -------------------------------------------------------------
@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
  data = request.get_json(silent=True)
  if not data:
    return (
        jsonify(
            {"success": False, "error": "Invalid or missing JSON payload"}
        ),
        400,
    )

  courses = load_courses()
  course = next((c for c in courses if c["id"] == course_id), None)

  if not course:
    return (
        jsonify({
            "success": False,
            "error": f"Course with ID {course_id} not found",
        }),
        404,
    )

  # Validate status if provided
  if "status" in data:
    if data["status"] not in ALLOWED_STATUSES:
      return (
          jsonify({
              "success": False,
              "error": (
                  f"Invalid status '{data['status']}'. Allowed values are:"
                  f" {', '.join(ALLOWED_STATUSES)}"
              ),
          }),
          400,
      )
    course["status"] = data["status"]

  # Validate date format if provided
  if "target_date" in data:
    if not is_valid_date(data["target_date"]):
      return (
          jsonify({
              "success": False,
              "error": "Invalid target_date format. Expected YYYY-MM-DD.",
          }),
          400,
      )
    course["target_date"] = str(data["target_date"]).strip()

  # Update string fields if provided
  if "name" in data and str(data["name"]).strip():
    course["name"] = str(data["name"]).strip()

  if "description" in data and str(data["description"]).strip():
    course["description"] = str(data["description"]).strip()

  save_courses(courses)
  return (
      jsonify({
          "success": True,
          "message": "Course updated successfully",
          "data": course,
      }),
      200,
  )


# -------------------------------------------------------------
# DELETE /api/courses/<id> - Delete a course
# -------------------------------------------------------------
@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
  courses = load_courses()
  initial_length = len(courses)

  # Keep every course EXCEPT the one with matching course_id
  courses = [c for c in courses if c["id"] != course_id]

  if len(courses) == initial_length:
    return (
        jsonify({
            "success": False,
            "error": f"Course with ID {course_id} not found",
        }),
        404,
    )

  save_courses(courses)
  return (
      jsonify({
          "success": True,
          "message": f"Course with ID {course_id} deleted successfully",
      }),
      200,
  )


# -------------------------------------------------------------
# GET /api/courses/stats - Return aggregate statistics
# -------------------------------------------------------------
@app.route("/api/courses/stats", methods=["GET"])
def get_stats():
  courses = load_courses()
  stats = {
      "total_courses": len(courses),
      "not_started": sum(
          1 for c in courses if c.get("status") == "Not Started"
      ),
      "in_progress": sum(1 for c in courses if c.get("status") == "In Progress"),
      "completed": sum(1 for c in courses if c.get("status") == "Completed"),
  }
  return jsonify({"success": True, "data": stats}), 200
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)