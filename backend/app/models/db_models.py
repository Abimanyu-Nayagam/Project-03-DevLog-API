# Database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(255), nullable=False, index=True)  
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationship
    user = db.relationship("User", back_populates="entries")

    def __repr__(self):
        return f"<Entry {self.title}>"


class Snippet(db.Model):
    __tablename__ = "snippets"

    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(255), nullable=False, index=True)  
    code = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=False, index=False)
    language = db.Column(db.String(50), nullable=False, index=True) 
    tags = db.Column(db.String(500), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationship
    user = db.relationship("User", back_populates="snippets")

    def __repr__(self):
        return f"<Snippet {self.title}>"
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hashed = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    snippets = db.relationship("Snippet", back_populates="user", cascade="all, delete-orphan")
    entries = db.relationship("Entry", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"