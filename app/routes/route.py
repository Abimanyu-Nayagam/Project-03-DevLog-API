from flask import Blueprint, request, jsonify
from app.models.db_models import Entry, Snippet, db

bp = Blueprint('routes', __name__)


@bp.route('/snippets', methods=['POST'])
def create_code():
    """Insert a new Code.

    Expects JSON body with:
      - language (str, required)
      - snippet (str, required)

    Returns created code (JSON) with status 201 on success, or JSON error with
    appropriate status code."""

    data = request.get_json() 

    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400   # validare request is of json type
    
    title = data.get('title')   #Get each key
    snippets = data.get('snippets')
    tags = data.get('tags')
    language = data.get('language')

    if not title:
        return jsonify({'error': '"title" is required.'}), 400  #Validate Each value
    if not snippets:
        return jsonify({'error': '"snippets" is required.'}), 400
   
    code_entry = Snippet(title=title, code=snippets, tags=tags, language=language)  # ORM or model object for code
    
    try:
        db.session.add(code_entry) # insert the new entry
        db.session.commit() # commit the transaction
    except Exception as exc: 
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    # Return created resource
    return jsonify({
        'id': code_entry.id,
        'title': code_entry.title,
        'snippets': code_entry.code,
        'language': code_entry.language,
        'tags': code_entry.tags,
        'created_at': code_entry.created_at.isoformat() if code_entry.created_at else None,
        'updated_at': code_entry.updated_at.isoformat() if code_entry.updated_at else None,
    }), 201


@bp.route('/entries', methods=['POST'])
def create_entry():
    """Insert a new Entry.

    Expects JSON body with:
      - title (str, required)
      - content (str, required)
      - tags (str, optional)

    Returns created entry (JSON) with status 201 on success, or JSON error with
    appropriate status code.
    """
    data = request.get_json() 

    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400   # validare request is of json type

    title = data.get('title')   #Get each key
    content = data.get('content')
    tags = data.get('tags')

    if not title:
        return jsonify({'error': '"title" is required.'}), 400  #Validate Each value
    if not content:
        return jsonify({'error': '"content" is required.'}), 400

    entry = Entry(title=title, content=content, tags=tags)  # ORM or model object for entry

    try:
        db.session.add(entry) # insert the new entry
        db.session.commit() # commit the transaction
    except Exception as exc: 
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    # Return created resource
    return jsonify({
        'id': entry.id,
        'title': entry.title,
        'content': entry.content,
        'tags': entry.tags,
        'created_at': entry.created_at.isoformat() if entry.created_at else None,
        'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
    }), 201
