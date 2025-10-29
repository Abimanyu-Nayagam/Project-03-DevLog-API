from flask import Blueprint, request, jsonify
from app.models.db_models import Entry, Snippet, db

bp = Blueprint('routes', __name__)

# Insertion 

@bp.route('/api/v1/snippets', methods=['POST'])
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


@bp.route('/api/v1/entries', methods=['POST'])
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

# Display
@bp.route('/api/v1/entries', methods=['GET'])
def get_entries():
    """Retrieve all entries.

    Returns a list of entries (JSON) with status 200 on success, or JSON error with
    appropriate status code.
    """
    try:
        entries = Entry.query.all() # query.all to get all entries
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    entries_list = []
    for entry in entries:
        entries_list.append({
            'id': entry.id,
            'title': entry.title,
            'content': entry.content,
            'tags': entry.tags,
            'created_at': entry.created_at.isoformat() if entry.created_at else None,
            'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
        })

    return jsonify(entries_list), 200

@bp.route('/api/v1/snippets', methods=['GET'])
def get_snippets():
    """Retrieve all snippets.

    Returns a list of snippets (JSON) with status 200 on success, or JSON error with
    appropriate status code.
    """
    try:
        snippets = Snippet.query.all() # query.all to get all code snippets
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    snippets_list = []
    for snippets in snippets:
        snippets_list.append({
            'id': snippets.id,
            'title': snippets.title,
            'snippet': snippets.code,
            'language': snippets.language,
            'tags': snippets.tags,
            'created_at': snippets.created_at.isoformat() if snippets.created_at else None,
            'updated_at': snippets.updated_at.isoformat() if snippets.updated_at else None,
        })

    return jsonify(snippets_list), 200

@bp.route('/api/v1/entries/<int:id>', methods=['GET'])
def get_entry(id):
    """Retrieve an entry by ID.
    Returns the entry (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    try:
        entry = Entry.query.get(id)
        if not entry:
            return jsonify({'error': 'Entry not found'}), 404
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    entry_data = {
        'id': entry.id,
        'title': entry.title,
        'content': entry.content,
        'tags': entry.tags,
        'created_at': entry.created_at.isoformat() if entry.created_at else None,
        'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
    }

    return jsonify(entry_data), 200

@bp.route('/api/v1/snippets/<int:id>', methods=['GET'])
def get_snippet(id):
    """Retrieve an snippet by ID.
    Returns the entry (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    try:
        snippet = Snippet.query.get(id)
        if not snippet:
            return jsonify({'error': 'snippet not found'}), 404
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    snippet_data = {
        'id': snippet.id,
        'title': snippet.title,
        'snippet': snippet.code,
        'tags': snippet.tags,
        'language': snippet.language,
        'created_at': snippet.created_at.isoformat() if snippet.created_at else None,
        'updated_at': snippet.updated_at.isoformat() if snippet.updated_at else None,
    }

    return jsonify(snippet_data), 200

@bp.route('/api/v1/snippets/<int:id>', methods=['DELETE'])
def delete_snippet(id):
    """Delete a snippet by ID.
    Returns status 204 on success, or JSON error with appropriate status code.
    """
    try:
        snippet = Snippet.query.get(id)
        if not snippet:
            return jsonify({'error': 'Snippet not found'}), 404

        db.session.delete(snippet)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    return jsonify({'Success': f'Deleted Snippet -- {id}'}), 200

@bp.route('/api/v1/entries/<int:id>', methods=['DELETE'])
def delete_entries(id):
    """Delete a entries by ID.
    Returns status 204 on success, or JSON error with appropriate status code.
    """
    try:
        entry = Entry.query.get(id)
        if not entry:
            return jsonify({'error': 'Entry not found'}), 404

        db.session.delete(entry)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    return jsonify({'Success': f'Deleted Entry -- {id}'}), 200
