from flask import Flask, request, jsonify
from models import db, Entry, Snippet
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/update_entry/<int:id>', methods=['PUT'])
def update_entry(id):
    data = request.get_json()
    entry = Entry.query.get(id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    entry.title = data.get("title", entry.title)
    entry.content = data.get("content", entry.content)
    entry.tags = data.get("tags", entry.tags)
    db.session.commit()
    return jsonify({"message": "Entry updated successfully!"})

@app.route('/update_snippet/<int:id>', methods=['PUT'])
def update_snippet(id):
    data = request.get_json()
    snippet = Snippet.query.get(id)
    if not snippet:
        return jsonify({"error": "Snippet not found"}), 404

    snippet.title = data.get("title", snippet.title)
    snippet.code = data.get("code", snippet.code)
    snippet.language = data.get("language", snippet.language)
    snippet.tags = data.get("tags", snippet.tags)
    db.session.commit()
    return jsonify({"message": "Snippet updated successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
