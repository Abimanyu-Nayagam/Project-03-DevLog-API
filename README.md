# DevLog API

A RESTful API for managing developer journal entries and code snippets. Built with Flask, SQLAlchemy, and MySQL.


## Features

- Create, read, update, and delete journal entries
- Manage code snippets with syntax highlighting
- Tag-based organization for entries and snippets
- Indexed searches for optimal performance
- Rich CLI tool with syntax highlighting and markdown rendering
- Environment-based configuration
- MySQL database with SQLAlchemy ORM


## Project Structure

```
Project-03-DevLog-API/
├── app/
│   ├── __init__.py
│   ├── app.py                 # Flask application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db_models.py       # SQLAlchemy models
│   │   ├── models.py          # Pydantic models
│   │   └── queries.sql        # Database schema
│   └── routes/
│       ├── __init__.py
│       ├── export_route.py    # File export routes
│       └── route.py           # CRUD routes
│
├── config/
│   ├── __init__.py
│   └── config.py              # Application configuration
├── cli.py                     # Command-line interface tool
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables template
├── .gitignore
├── README.md
└── start.bat                  # Start flask server
```

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YSH-NYK/Project-03-DevLog-API.git
   cd Project-03-DevLog-API
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows (PowerShell)**:
     ```powershell
     \venv\Scripts\Activate
     ```
   - **Windows (CMD)**:
     ```cmd
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database**
   
   Create the MySQL database:
   ```Import the `queries.sql` in your mysql workbench```

## Configuration

1. **Create a `.env` file** in the project root:

2. **Update `.env` with your credentials**:
   ```env
   SECRET_KEY=your-secret-key-here
   
   MYSQL_USER=root
   MYSQL_PASSWORD=your-password-here
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DB=devlog_db

   FLASK_APP = app
   Flask_DEBUG = 1
   ```

   **Note**: Special characters in passwords (like `@`, `:`, `/`) are automatically URL-encoded by the application.

## Running the Application

### Start the Flask Server

From the project root directory:

Option 1: run the start.bat

Option 2: Run the following commands

```bash
python -m venv venv
```

```bash
venv/Scripts/activate
```

```bash
python app_run.py
```

The base URL for server: `http://127.0.0.1:5000`

## API Endpoints

### Entries

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/entries` | Get all entries |
| GET | `/api/v1/entries/:id` | Get entry by ID |
| POST | `/api/v1/entries` | Create new entry |
| PATCH | `/api/v1/entries` | Update entry |
| DELETE | `/api/v1/entries/:id` | Delete entry |

### Snippets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/snippets` | Get all snippets |
| GET | `/api/v1/snippets/:id` | Get snippet by ID |
| POST | `/api/v1/snippets` | Create new snippet |
| PATCH | `/api/v1/snippets` | Update snippet |
| DELETE | `/api/v1/snippets/:id` | Delete snippet |

## CLI Tool

The project includes a command-line interface for managing entries and snippets with rich formatting.

### Example Requests

**Retrieve an existing entry:**
```bash
    python cli.py show-snippet <snippet_id:int>
```

### To view all other options

```bash
python cli.py --help
```

### Multi-line Input

When creating entries or snippets, you can enter multi-line content:
- **Windows**: Press `Ctrl+Z` then `Enter` to finish input
- **Unix/Mac**: Press `Ctrl+D` to finish input

## Database Schema

### Entries Table

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| title | VARCHAR(255) | Entry title (indexed) |
| content | TEXT | Entry content |
| tags | VARCHAR(500) | Comma-separated tags (indexed) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Snippets Table

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| title | VARCHAR(255) | Snippet title (indexed) |
| code | TEXT | Code content |
| language | VARCHAR(50) | Programming language (indexed) |
| tags | VARCHAR(500) | Comma-separated tags (indexed) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Indexes

The following indexes are created for optimal query performance:
- `idx_entries_title` - Entry title searches
- `idx_entries_tags` - Entry tag filtering
- `idx_snippets_title` - Snippet title searches
- `idx_snippets_language` - Language filtering
- `idx_snippets_tags` - Snippet tag filtering


## Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- Rich library for beautiful CLI output
- Revature training program