
-- Create new database
CREATE DATABASE IF NOT EXISTS devlog_db;

-- Use the database
USE devlog_db;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS snippets;
DROP TABLE IF EXISTS entries;

-- Create entries table (journal entries)
CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    tags VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create snippets table (code snippets)
CREATE TABLE snippets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    code TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    tags VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO entries (title, content, tags) VALUES
('Getting Started with Flask', 
'Today I started learning Flask framework for building REST APIs. Flask is a lightweight Python web framework that makes it easy to build web applications. Key concepts I learned:\n\n1. **Flask App Initialization**: Create app using `Flask(__name__)`\n2. **Routes**: Use `@app.route()` decorator to define endpoints\n3. **Request Handling**: Access request data using `request.json`\n4. **Response**: Return JSON using `jsonify()`\n\nNext steps: Learn about Flask-SQLAlchemy for database integration.',
'flask,python,web-development,api'),

('Understanding SQLAlchemy ORM',
'Explored SQLAlchemy today - it''s an Object-Relational Mapping (ORM) tool for Python. Instead of writing raw SQL, we define models as Python classes.\n\n**Key Benefits:**\n- Write Python code instead of SQL\n- Database-agnostic (works with MySQL, PostgreSQL, SQLite)\n- Prevents SQL injection automatically\n- Easy relationship management\n\n**Example Model:**\n```python\nclass User(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    name = db.Column(db.String(100))\n```\n\nThis approach makes database operations much cleaner and maintainable.',
'sqlalchemy,orm,database,python'),

('REST API Design Best Practices',
'Learned about RESTful API design principles today. Important conventions:\n\n**HTTP Methods:**\n- GET: Retrieve data\n- POST: Create new resource\n- PUT: Update entire resource\n- PATCH: Partial update\n- DELETE: Remove resource\n\n**URL Structure:**\n- Use nouns, not verbs: `/api/users` not `/api/getUsers`\n- Use plural names: `/api/entries` not `/api/entry`\n- Version your API: `/api/v1/entries`\n\n**Status Codes:**\n- 200: Success\n- 201: Created\n- 400: Bad Request\n- 404: Not Found\n- 500: Server Error\n\nConsistent API design makes integration easier for frontend developers.',
'rest-api,design,best-practices,http'),

('Debugging MySQL Connection Issues',
'Spent 2 hours debugging a MySQL connection error. The issue was with the connection string format.\n\n**Problem:**\n```\nOperationalError: (2003, "Can''t connect to MySQL server")\n```\n\n**Solution:**\nThe connection URI format needs to be exact:\n```\nmysql+pymysql://username:password@localhost:3306/database_name\n```\n\n**Common Mistakes:**\n- Wrong port (default is 3306)\n- Special characters in password need URL encoding\n- MySQL service not running\n- Firewall blocking connection\n\n**Lesson Learned:** Always test database connection before building features. Add proper error handling and logging.',
'mysql,debugging,database,troubleshooting'),

('Implementing Pydantic Validation',
'Integrated Pydantic for request validation in our Flask API. Pydantic validates data types automatically and provides clear error messages.\n\n**Without Pydantic:**\n```python\nif not request.json.get("title"):\n    return {"error": "Title required"}, 400\n```\n\n**With Pydantic:**\n```python\nclass EntrySchema(BaseModel):\n    title: str\n    content: str\n    tags: Optional[str]\n```\n\n**Benefits:**\n- Automatic type checking\n- Clear error messages\n- Self-documenting code\n- Less boilerplate validation code\n\nPydantic catches errors before they reach the database, making the API more robust.',
'pydantic,validation,python,api');

INSERT INTO snippets (title, code, language, tags) VALUES
('Flask Basic Route',
'from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/v1/hello", methods=["GET"])
def hello():
    return jsonify({
        "status": "success",
        "message": "Hello, World!",
        "data": None
    }), 200

if __name__ == "__main__":
    app.run(debug=True)',
'Python',
'flask,api,basic,route'),

('SQLAlchemy Model Example',
'from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = "entries"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Entry {self.title}>"',
'Python',
'sqlalchemy,model,database,orm'),

('MySQL Connection Configuration',
'import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # MySQL Database Configuration
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "devlog_db")
    
    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False',
'Python',
'mysql,config,database,environment'),

('Pydantic Validation Schema',
'from pydantic import BaseModel, Field, validator
from typing import Optional

class EntrySchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    tags: Optional[str] = Field(None, max_length=500)
    
    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "title": "My First Entry",
                "content": "This is the content of my journal entry",
                "tags": "python,flask,learning"
            }
        }',
'Python',
'pydantic,validation,schema,api'),

('JavaScript Fetch API Example',
'// POST request to create a new entry
async function createEntry(entryData) {
    try {
        const response = await fetch("http://localhost:5000/api/v1/entries", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(entryData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log("Entry created:", data);
            return data;
        } else {
            console.error("Error:", data.message);
            throw new Error(data.message);
        }
    } catch (error) {
        console.error("Network error:", error);
        throw error;
    }
}

// Example usage
const newEntry = {
    title: "Learning JavaScript",
    content: "Today I learned about async/await",
    tags: "javascript,async,learning"
};

createEntry(newEntry);',
'JavaScript',
'javascript,fetch,api,async');

-- ================================================================================
-- VERIFICATION QUERIES
-- ================================================================================

-- -- Check if tables were created successfully
-- SHOW TABLES;

-- -- View all entries
-- SELECT * FROM entries;

-- -- View all snippets
-- SELECT * FROM snippets;

-- -- Count records
-- SELECT 'Entries' as table_name, COUNT(*) as record_count FROM entries
-- UNION ALL
-- SELECT 'Snippets' as table_name, COUNT(*) as record_count FROM snippets;


