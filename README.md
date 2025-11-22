# DevLog API

A RESTful API for managing developer journal entries and code snippets. Built with Flask, SQLAlchemy, and MySQL (or compatible server). This repository contains the backend API, a CLI tool, and a small frontend in `src/`.

## Key Features

- Created an API to store and retrieve technical journal entries with **Markdown support**.
- Implemented a **code snippet repository** with language tagging and **fuzzy search**.
- Added **filtering** by tags, title, and programming language.
- Added **Title, Tags, and Description** for each code snippet and Entries, with optional **LLM-based auto-generation**.
- Implemented a **user login system** allowing registered users to manage their own snippets and entries with protected routes.
- Integrated **JWT authentication** for secure, stateless sessions.
- Modeled `Entry`, `Snippet`, and `User` using **SQLAlchemy** with efficient indexing.
- Added **CLI functionality** to export entries/snippets to **Markdown** or **JSON** files.
- Built a **CLI interface** to interact with all API routes.
- Designed **versioned API endpoints** (e.g., `/api/entries`) for future compatibility.
- Configured **AWS RDS** to host and manage the relational database.
- **Containerized** the application using Docker for consistent cross-environment behavior.
- Implemented a **CI/CD pipeline** using GitHub Actions for automated build and testing.
- Deployed the application on **AWS EC2** for scalable and reliable hosting.
- Developed a **web-based frontend using React** to interact with the application.
- Displayed code snippets with proper syntax formatting using ```Rich``` for cli interface and ```SyntaxHighlighter``` for web interface
- Implemented **consistent, machine-readable success and error responses** across the API.

**Tech stack & integrations**

- Frontend: React
- Backend framework: Flask, Flask-SQLAlchemy, Flask-Migrate
- Authentication: Flask-JWT-Extended
- Data export: Argparse CLI, `json`, `pathlib`
- Validation: Pydantic for payload validation
- Database: MySQL (hosted on AWS RDS)
- Containerization: Docker
- CI/CD: GitHub Actions
- Hosting: AWS EC2
- AI Integration: Gemini for auto-generating fields

## Repository Layout

```
Project-03-DevLog-API/
├── app_run.py                 # Project entry used to run the Flask server
├── cli.py                     # CLI interface tool
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── db_models.py       # SQLAlchemy models
│   │   ├── models.py          # validation / pydantic models
│   │   └── queries.sql        # DB schema / creation SQL
│   └── routes/
│       ├── auth.py            # REST API handlers
│       ├── autogen_route.py
│       ├── export_route.py
│       └── route.py           
├── config/
│   └── config.py              # Application configuration loader
├── src/                       # frontend (React)
├── tests/                     # Unit tests (pytest)
├── requirements.txt
├── package.json            
├── start.bat                  # Execute to start React + Flask app 
└── README.md
```

## Quick Setup (Windows PowerShell)

1. Clone the repository:

```powershell
git clone https://github.com/Abimanyu-Nayagam/Project-03-DevLog-API.git
cd Project-03-DevLog-API
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate
```

3. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

4. Install frontend dependencies :

```powershell
npm install
```
   5. Start the App by running ```start.bat```

## Configuration

Create a `.env` file in the project root (the app reads configuration from `config/config.py`). 

Example values:
```env
MYSQL_USER=your-username-or-root
MYSQL_PASSWORD=your-password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=devlog_db
GEMINI_API_KEY=your-gemini-API-Key
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
VITE_API_BASE=http://localhost:5000
FLASK_APP = app
FLASK_DEBUG=1
```

## Database Setup

Create the database and tables using the provided SQL schema `app/models/queries.sql`.

Using MySQL CLI (example):

```powershell
# create database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS devlog_db;"
# import schema
mysql -u root -p devlog_db < .\\app\\models\\queries.sql
```

Or import `app/models/queries.sql` in MySQL Workbench.

## Running the Application

After cloning 
1. Do ```npm install```
2. Activate ```venv``` and run ```pip install -r requirements.txt```
3. Execute the ```start.bat``` file (runs the flask server + React frontend)

## API Endpoints

- Entries
  - `GET  /api/entries` — list entries
  - `GET  /api/entries/<id>` — get entry by id
  - `POST /api/entries` — create entry
  - `PATCH /api/entries/<id>` — update entry
  - `DELETE /api/entries/<id>` — delete entry

- Snippets
  - `GET  /api/snippets` — list snippets
  - `GET  /api/snippets/<id>` — get snippet by id
  - `POST /api/snippets` — create snippet
  - `PATCH /api/snippets/<id>` — update snippet
  - `DELETE /api/snippets/<id>` — delete snippet

### Authentication

- `POST /register` — create a new user
- `POST /login` — authenticate and receive a JWT

### Entries

- `GET  /api/entries` — list entries for the authenticated user
- `GET  /api/entries/<id>` — get entry by id
- `POST /api/entries` — create entry 
- `PATCH /api/entries` — update entry 
- `DELETE /api/entries/<id>` — delete entry
- `GET /api/entries/search?q=<query>` — fuzzy search entries 
- `GET /api/entries/filter/tag/<tag>` — filter entries by tag
- `GET /api/entries/filter/title/<title>` — filter entries by title

### Snippets

- `GET  /api/snippets` — list snippets for the authenticated user
- `GET  /api/snippets/<id>` — get snippet by id
- `POST /api/snippets` — create snippet
- `PATCH /api/snippets` — update snippet 
- `DELETE /api/snippets/<id>` — delete snippet
- `GET /api/snippets/search?q=<query>` — fuzzy search snippets 
- `GET /api/snippets/filter/tag/<tag>` — filter snippets by tag
- `GET /api/snippets/filter/language/<language>` — filter snippets by language
- `GET /api/snippets/filter/title/<title>` — filter snippets by title

### Auto-generation (LLM-powered)

- `POST /autogen/title` — generate a concise title from `content` 
- `POST /autogen/description` — generate a short description from `content`, `language`, `title`
- `POST /autogen/tags` — generate 3–6 short tags from `content`, `language`, `title`

### Export endpoints

- `GET  /export-entry-md/<entry_id>` — download a Markdown file for an entry
- `GET  /export-snippet-md/<snippet_id>` — download a Markdown file for a snippet (includes fenced code block)
- `GET  /export-snippet-json/<snippet_id>` — download snippet as JSON
- `GET  /export-entry-json/<entry_id>` — download entry as JSON

Refer to the route handlers in `app/routes/` (`route.py`, `auth.py`, `autogen_route.py`, `export_route.py`) for parameter names, example payloads, and exact response shapes.

## CLI Usage

`cli.py` provides convenience commands for interacting with entries and snippets. Example:

```powershell
python cli.py show-snippet <snippet_id>
python cli.py --help
```

Multi-line input notes:
- Windows PowerShell: press `Ctrl+Z` then `Enter` to finish multiline input
- Unix/macOS: press `Ctrl+D` to finish

## Tests

Run the test suite with `pytest`:

```powershell
pip install -r requirements.txt
pytest -q
```

Tests are located in the `tests/` directory (e.g., `test_auth.py`, `test_base.py`).


## Acknowledgments

- Flask
- SQLAlchemy
- Rich (for CLI)
- SyntaxHighlighter (for React)
