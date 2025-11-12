from flask import Blueprint, request, jsonify
from app.models.db_models import Entry, Snippet, db
from app.models.models import CreateEntryRequest, CreateSnippetRequest, UpdateEntryRequest, UpdateSnippetRequest
from sqlalchemy import or_
from flask_jwt_extended import jwt_required

bp = Blueprint('routes', __name__)

# Insertion 

@bp.route('/api/v1/snippets', methods=['POST'])
@jwt_required()
def create_code():
    """Insert a new Code.

    Expects JSON body with:
      - language (str, required)
      - snippet (str, required)
      - tags (str, optional)

    Returns created code (JSON) with status 201 on success, or JSON error with
    appropriate status code."""

    data = request.get_json() 

    try:
        create_snippet = CreateSnippetRequest(**data)
    except Exception as e:
        return jsonify({'error': 'Invalid request', 'details': str(e)}), 400

    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400   # validare request is of json type
    
    title = data.get('title')   #Get each key
    snippets = data.get('snippet')
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
        'snippet': code_entry.code,
        'language': code_entry.language,
        'tags': code_entry.tags,
        'created_at': code_entry.created_at.isoformat() if code_entry.created_at else None,
        'updated_at': code_entry.updated_at.isoformat() if code_entry.updated_at else None,
    }), 201


@bp.route('/api/v1/entries', methods=['POST'])
@jwt_required()
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

    try:
        create_entry = CreateEntryRequest(**data)
    except Exception as e:
        return jsonify({'error': 'Invalid request', 'details': str(e)}), 400

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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def get_entry(id):
    """Retrieve an entry by ID.
    Returns the entry (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    if type(id) is not int:
        return jsonify({'error': 'ID must be an integer'}), 400
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
@jwt_required()
def get_snippet(id):
    """Retrieve an snippet by ID.
    Returns the entry (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    if type(id) is not int:
        return jsonify({'error': 'ID must be an integer'}), 400
    try:
        snippet = Snippet.query.get(id)
        if not snippet:
            return jsonify({'error': 'Snippet not found'}), 404
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
@jwt_required()
def delete_snippet(id):
    """Delete a snippet by ID.
    Returns status 204 on success, or JSON error with appropriate status code.
    """

    if type(id) is not int:
        return jsonify({'error': 'ID must be an integer'}), 400
    
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
@jwt_required()
def delete_entries(id):
    """Delete a entries by ID.
    Returns status 204 on success, or JSON error with appropriate status code.
    """

    if type(id) is not int:
        return jsonify({'error': 'ID must be an integer'}), 400

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

#update exisitng entry
@bp.route('/api/v1/entries', methods=['PATCH'])
@jwt_required()
def update_entry():
    """Update an existing entry by ID."""
    data = request.get_json()

    # Validate request body using Pydantic model
    try:
        update_entry = UpdateEntryRequest(**data)
    except Exception as e:
        return jsonify({'error': 'Invalid request', 'details': str(e)}), 400

    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400

    entry = Entry.query.get(data['id'])
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    # Update only provided fields
    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    entry.tags = data.get('tags', entry.tags)

    try:
        db.session.commit()
        return jsonify({
            'id': entry.id,
            'title': entry.title,
            'content': entry.content,
            'tags': entry.tags,
            'created_at': entry.created_at.isoformat() if entry.created_at else None,
            'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
        }), 200
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500


@bp.route('/api/v1/snippets', methods=['PATCH'])
@jwt_required()
def update_snippet():
    """Update an existing snippet by ID."""
    data = request.get_json()

    # Validate request body using Pydantic model
    try:
        update_snippet = UpdateSnippetRequest(**data)
    except Exception as e:
        return jsonify({'error': 'Invalid request', 'details': str(e)}), 400
    
    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400

    snippet = Snippet.query.get(data['id'])
    if not snippet:
        return jsonify({'error': 'Snippet not found'}), 404

    snippet.title = data.get('title', snippet.title)
    snippet.code = data.get('snippets', snippet.code)
    snippet.tags = data.get('tags', snippet.tags)
    snippet.language = data.get('language', snippet.language)

    try:
        db.session.commit()
        return jsonify({
            'id': snippet.id,
            'title': snippet.title,
            'snippet': snippet.code,
            'language': snippet.language,
            'tags': snippet.tags,
            'created_at': snippet.created_at.isoformat() if snippet.created_at else None,
            'updated_at': snippet.updated_at.isoformat() if snippet.updated_at else None,
        }), 200
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500
    


# search entries 
@bp.route('/api/v1/entries/search', methods=['GET'])
@jwt_required()
def search_entries():
    """Search entries by title, content, or tags."""
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Search query (q) is required'}), 400

    try:
        results = Entry.query.filter(
            or_(
                Entry.title.ilike(f'%{query}%'),
                Entry.content.ilike(f'%{query}%'),
                Entry.tags.ilike(f'%{query}%')
            )
        ).all()
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    entries_list = [{
        'id': e.id,
        'title': e.title,
        'content': e.content,
        'tags': e.tags,
        'created_at': e.created_at.isoformat() if e.created_at else None,
        'updated_at': e.updated_at.isoformat() if e.updated_at else None,
    } for e in results]

    return jsonify(entries_list), 200


@bp.route('/api/v1/snippets/search', methods=['GET'])
@jwt_required()
def search_snippets():
    """Search snippets by title, code, tags, or language."""
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Search query (q) is required'}), 400

    try:
        results = Snippet.query.filter(
            or_(
                Snippet.title.ilike(f'%{query}%'),
                Snippet.code.ilike(f'%{query}%'),
                Snippet.tags.ilike(f'%{query}%'),
                Snippet.language.ilike(f'%{query}%')
            )
        ).all()
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    snippets_list = [{
        'id': s.id,
        'title': s.title,
        'snippet': s.code,
        'language': s.language,
        'tags': s.tags,
        'created_at': s.created_at.isoformat() if s.created_at else None,
        'updated_at': s.updated_at.isoformat() if s.updated_at else None,
    } for s in results]

    return jsonify(snippets_list), 200

@bp.route('/api/v1/snippets/filter/tag/<string:tag>', methods=['GET'])
@jwt_required()
def filter_snippet_by_tag(tag):
    """Retrieve an snippet by tags.
    Returns the snippet (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    try:
        snippets = Snippet.query.filter(Snippet.tags.contains(tag)).all()
        if not snippets:
            return jsonify({'error': 'No snippets found'}), 404
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    snippets_data = []
    for snippet in snippets:
        snippets_data.append({
        'id': snippet.id,
        'title': snippet.title,
        'snippet': snippet.code,
        'tags': snippet.tags,
        'created_at': snippet.created_at.isoformat() if snippet.created_at else None,
        'updated_at': snippet.updated_at.isoformat() if snippet.updated_at else None,
    })
    
    return jsonify(snippets_data), 200

@bp.route('/api/v1/snippets/filter/language/<string:lang>', methods=['GET'])
@jwt_required()
def filter_snippet_by_lang(lang):
    """Retrieve an snippet by language.
    Returns the snippet (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    try:
        snippets = Snippet.query.filter(Snippet.language.contains(lang)).all()
        if not snippets:
            return jsonify({'error': 'No snippets found'}), 404
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    snippets_data = []
    for snippet in snippets:
        snippets_data.append({
        'id': snippet.id,
        'title': snippet.title,
        'snippet': snippet.code,
        'tags': snippet.tags,
        'created_at': snippet.created_at.isoformat() if snippet.created_at else None,
        'updated_at': snippet.updated_at.isoformat() if snippet.updated_at else None,
    })
    
    return jsonify(snippets_data), 200

@bp.route('/api/v1/entries/filter/tag/<string:tag>', methods=['GET'])
@jwt_required()
def filter_entry_by_tag(tag):
    """Retrieve an entry by tags.
    Returns the entry (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    try:
        entries = Entry.query.filter(Entry.tags.contains(tag)).all()
        if not entries:
            return jsonify({'error': 'No entries found'}), 404
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    entry_data = []
    for entry in entries:
        entry_data.append({
            'id': entry.id,
        'title': entry.title,
        'content': entry.content,
        'tags': entry.tags,
        'created_at': entry.created_at.isoformat() if entry.created_at else None,
        'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
    })

    return jsonify(entry_data), 200

@bp.route('/api/v1/entries/filter/title/<string:title>', methods=['GET'])
@jwt_required()
def filter_entry_by_title(title):
    """Retrieve an entry by title.
    Returns the entry (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    try:
        entries = Entry.query.filter(Entry.title.contains(title)).all()
        if not entries:
            return jsonify({'error': 'No entries found'}), 404
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    entry_data = []
    for entry in entries:
        entry_data.append({
            'id': entry.id,
        'title': entry.title,
        'content': entry.content,
        'tags': entry.tags,
        'created_at': entry.created_at.isoformat() if entry.created_at else None,
        'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
    })

    return jsonify(entry_data), 200

@bp.route('/api/v1/snippets/filter/title/<string:title>', methods=['GET'])
@jwt_required()
def filter_snippet_by_title(title):
    """Retrieve a snippet by title.
    Returns the snippet (JSON) with status 200 on success, or JSON error with appropriate status code.
    """
    try:
        snippets = Snippet.query.filter(Snippet.title.contains(title)).all()
        if not snippets:
            return jsonify({'error': 'No snippets found'}), 404
    except Exception as exc:
        return jsonify({'error': 'Database error', 'details': str(exc)}), 500

    snippet_data = []
    for snippet in snippets:
        snippet_data.append({
            'id': snippet.id,
            'title': snippet.title,
            'code': snippet.code,
            'tags': snippet.tags,
        'created_at': snippet.created_at.isoformat() if snippet.created_at else None,
        'updated_at': snippet.updated_at.isoformat() if snippet.updated_at else None,
    })

    return jsonify(snippet_data), 200