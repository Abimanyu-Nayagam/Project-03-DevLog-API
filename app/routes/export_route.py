import os
import json
from flask import Blueprint, request, jsonify, send_file
from flask_pydantic import validate
from app.models.db_models import Entry, Snippet, db
from app.models.models import ExportEntryRequest, ExportSnippetRequest

e_bp = Blueprint('export_route', __name__)

@e_bp.route('/export-entry-md/v1/<int:entry_id>',methods=['GET'])
def export_entry_md(entry_id):
    '''
    Export the selected entry in the form of a Markdown (.md) file using the provided entry id

    Parameters:
        entry_id: id of the entry which needs to be exported
    '''

    id = entry_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    entry = Entry.query.get(id)

    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    with open(f"Entry {id}.md", 'w') as f:
        heading = f"# {entry.title}"
        
        f.write(heading)
        f.write("\n")
        f.write(entry.content)
    
    return send_file(f"Entry {id}.md", as_attachment=True), 200

@e_bp.route('/export-snippet-md/v1/<int:snippet_id>',methods=['GET'])
def export_snippet_md(snippet_id):
    '''
    Export the selected entry in the form of a Markdown (.md) file using the provided snippet id

    Parameters:
        snippet_id: id of the snippet which needs to be exported
    '''

    id = snippet_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    snippet = Snippet.query.get(id)

    if not snippet:
        return jsonify({'error': 'Entry not found'}), 404

    with open(f"Snippet {id}.md", 'w') as f:
        heading = f"# {snippet.title}"
        
        f.write(heading)
        f.write("\n")
        f.write(f"```{snippet.language.lower()}")
        f.write("\n")
        f.write(snippet.code)

    return send_file(f"Snippet {id}.md", as_attachment=True), 200

@e_bp.route('/export-snippet-json/v1/<int:entry_id>',methods=['GET'])
def export_snippet_json(entry_id):
    '''
    Export the selected snippet in the form of a json (.json) file using the provided entry id

    Parameters:
        snippet_id: id of the snippet which needs to be exported
    '''

    id = entry_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    snippet = Snippet.query.get(id)

    if not snippet:
        return jsonify({'error': 'Entry not found'}), 404

    response = {
        "title" : f"{snippet.title}",
         "code": f"{snippet.code}",
         "language": f"{snippet.language}", 
         "tags": f"{snippet.tags}"
    }

    with open(f"Snippet {id}.json", 'w') as f:
        json.dump(response, f, indent=4, ensure_ascii=False)

    return send_file(f"Snippet {id}.json", as_attachment=True), 200

@e_bp.route('/export-entry-json/v1/<int:entry_id>',methods=['GET'])
def export_entry_json(entry_id):
    '''
    Export the selected entry in the form of a json (.json) file using the provided entry id

    Parameters:
        snippet_id: id of the entry which needs to be exported
    '''

    id = entry_id

    if not id:
        return jsonify({'error': 'id is required for exporting.'}), 400  #Validate Each value
    
    entry = Entry.query.get(id)

    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    response = {
        "title" : f"{entry.title}",
         "code": f"{entry.content}",
         "tags": f"{entry.tags}"
    }

    with open(f"Entry {id}.json", 'w') as f:
        json.dump(response, f, indent=4, ensure_ascii=False)

    return send_file(f"Entry {id}.json", as_attachment=True), 200
