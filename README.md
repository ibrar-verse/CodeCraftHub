# CodeCraftHub - Personalized Learning Platform API

A lightweight RESTful API built with Python and Flask for tracking developer learning paths. Data persists to a local JSON file (`courses.json`) without requiring a relational or NoSQL database.

---

## Features

- **Full CRUD Operations:** Create, retrieve, update, and delete courses.
- **Flat-file Persistence:** Safe reading and atomic writing to `courses.json`.
- **Validation Gates:** Enforces required fields, date formats (`YYYY-MM-DD`), and a strict status enum (`Not Started`, `In Progress`, `Completed`).
- **CORS Enabled:** Pre-configured with `flask-cors` to allow communication with frontend web clients.
- **Aggregate Analytics:** Built-in `/api/courses/stats` endpoint for progress overview.

---

## Project Structure

```text
codecrafthub/
├── courses.json        # Flat-file database (auto-generated)
├── storage.py          # Persistence helpers (load_courses, save_courses, get_next_id)
├── app.py              # Flask server and REST routing logic
├── requirements.txt    # Application dependencies
└── README.md           # Project documentation
```

---

## Installation & Setup

1. **Clone or Navigate to the Project:**
   ```bash
   cd codecrafthub
   ```

2. **Create and Activate a Virtual Environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API Server:**
   ```bash
   python app.py
   ```
   The API will start locally at: `http://127.0.0.1:5000`

---

## API Reference

### Base URL: `http://127.0.0.1:5000`

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/courses` | Retrieve all tracked courses | `200 OK` |
| `GET` | `/api/courses/<id>` | Retrieve a single course by ID | `200 OK` / `404 Not Found` |
| `POST` | `/api/courses` | Add a new course | `201 Created` / `400 Bad Request` |
| `PUT` | `/api/courses/<id>` | Update an existing course | `200 OK` / `400 Bad Request` / `404 Not Found` |
| `DELETE`| `/api/courses/<id>` | Delete a course by ID | `200 OK` / `404 Not Found` |
| `GET` | `/api/courses/stats` | Retrieve course status metrics | `200 OK` |

---

## Example Payloads & Testing

### 1. Add a Course (`POST /api/courses`)
**Payload:**
```json
{
  "name": "Python Basics",
  "description": "Learn Python syntax and data structures",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

### 2. Update a Course (`PUT /api/courses/1`)
**Payload:**
```json
{
  "status": "In Progress"
}
```

---

## Troubleshooting Common Issues

- **Port 5000 Already in Use:** If port 5000 is occupied, adjust the port inside `app.py` under `app.run(port=5001)` and update client requests accordingly.
- **PowerShell Quote Escaping with cURL:** Windows PowerShell processes double quotes aggressively. Use PowerShell's native `Invoke-RestMethod` or escape interior quotes using backticks (`` `"` ``).
- **CORS Issues in Browser:** Ensure `flask-cors` is installed and `CORS(app)` is initialized in `app.py`.