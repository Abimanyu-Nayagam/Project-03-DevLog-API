from io import BytesIO
import json
from app.models.db_models import Entry, Snippet, db
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

e_bp = Blueprint('export_route', __name__)

@e_bp.route('/api/export-entry-md/<int:entry_id>',methods=['GET'])
@jwt_required()
def export_entry_md(entry_id):

    '''
    Export the selected entry in the form of a Markdown (.md) file using the provided entry id

    Parameters:
        entry_id: id of the entry which needs to be exported
    '''
    current_user_id = get_jwt_identity()

    if type(entry_id) != int:
        return jsonify({'error': 'Invalid id format. id must be an integer.'}), 400
    
    id = entry_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    entry = Entry.query.filter_by(id=id, user_id=current_user_id).first()

    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    md_buffer = BytesIO()

    heading = f"# {entry.title}"

    content = f"{heading}\n{entry.content}"

    md_buffer.write(content.encode('utf-8'))

    md_buffer.seek(0)
    
    return send_file(
        md_buffer,
        as_attachment=True,
        download_name=f"Entry {id}.md",
        mimetype="text/markdown"
        ), 200

@e_bp.route('/api/export-snippet-md/<int:snippet_id>',methods=['GET'])
@jwt_required()
def export_snippet_md(snippet_id):
    '''
    Export the selected entry in the form of a Markdown (.md) file using the provided snippet id

    Parameters:
        snippet_id: id of the snippet which needs to be exported
    '''

    if type(snippet_id) != int:
        return jsonify({'error': 'Invalid id format. id must be an integer.'}), 400

    id = snippet_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    snippet = Snippet.query.filter_by(id=id, user_id=get_jwt_identity()).first()

    if not snippet:
        return jsonify({'error': 'Entry not found'}), 404

    md_buffer = BytesIO()

    heading = f"# {snippet.title}"

    content = f"{heading}\n\n```{snippet.language.lower()}\n{snippet.code}"

    md_buffer.write(content.encode('utf-8'))

    md_buffer.seek(0)
    
    return send_file(
        md_buffer,
        as_attachment=True,
        download_name=f"Snippet {id}.md",
        mimetype="text/markdown"
        ), 200

@e_bp.route('/api/export-snippet-json/<int:snippet_id>',methods=['GET'])
@jwt_required()
def export_snippet_json(snippet_id):
    '''
    Export the selected snippet in the form of a json (.json) file using the provided entry id

    Parameters:
        snippet_id: id of the snippet which needs to be exported
    '''
    if type(snippet_id) != int:
        return jsonify({'error': 'Invalid id format. id must be an integer.'}), 400

    id = snippet_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    snippet = Snippet.query.filter_by(id=id, user_id=get_jwt_identity()).first()

    if not snippet:
        return jsonify({'error': 'Entry not found'}), 404

    response = {
        "title" : f"{snippet.title}",
         "code": f"{snippet.code}",
         "language": f"{snippet.language}", 
         "tags": f"{snippet.tags}"
    }

    md_buffer = BytesIO()

    md_buffer.write(json.dumps(response).encode('utf-8'))

    md_buffer.seek(0)
    
    return send_file(
        md_buffer,
        as_attachment=True,
        download_name=f"Snippet {id}.json",
        mimetype="application/json"
        ), 200

@e_bp.route('/api/export-entry-json/<int:entry_id>',methods=['GET'])
@jwt_required()
def export_entry_json(entry_id):
    '''
    Export the selected entry in the form of a json (.json) file using the provided entry id

    Parameters:
        snippet_id: id of the entry which needs to be exported
    '''

    if type(entry_id) != int:
        return jsonify({'error': 'Invalid id format. id must be an integer.'}), 400

    id = entry_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    entry = Entry.query.filter_by(id=id, user_id=get_jwt_identity()).first()

    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    response = {
        "title" : f"{entry.title}",
         "code": f"{entry.content}",
         "tags": f"{entry.tags}"
    }

    md_buffer = BytesIO()

    md_buffer.write(json.dumps(response).encode('utf-8'))

    md_buffer.seek(0)
    
    return send_file(
        md_buffer,
        as_attachment=True,
        download_name=f"Entry {id}.json",
        mimetype="application/json"
        ), 200