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

    def __repr__(self):
        return f"<Entry {self.title}>"


class Snippet(db.Model):
    __tablename__ = "snippets"

    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(255), nullable=False, index=True)  
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False, index=True) 
    tags = db.Column(db.String(500), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Snippet {self.title}>"
    

