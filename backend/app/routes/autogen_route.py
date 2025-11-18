from flask import Blueprint, request, jsonify
from app.models.db_models import User, db
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

autogen_bp = Blueprint('autogen', __name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# route for handling title auto-generation
@autogen_bp.route('/autogen/title', methods=['POST'])
@jwt_required()
def generate_title():
    try: 
        data = request.get_json()
        content = data.get("content", "")
        
        prompt = f"""Generate a short and clear TITLE for the following code snippet or markdown documentation. Only return the title, nothing else.

{content}"""

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        title = response.text.strip()

        return jsonify({"title": title})
    
    except Exception as e:
        import traceback
        error_msg = str(e) if str(e) else "Unknown error occurred"
        return jsonify({"error": error_msg, "type": type(e).__name__, "traceback": traceback.format_exc()}), 500




# route for handling description auto-generation
@autogen_bp.route('/autogen/description', methods=['POST'])
@jwt_required()
def generate_description():
    try:
        data = request.get_json()
        content = data.get("content", "")
        language = data.get("language", "")
        title = data.get("title", "")

        prompt = f"""
Generate a very short description (maximum 2 lines, around 20–30 words total)
for the following code snippet or technical content.

Your output must:
- Be concise
- Be easy to understand
- Be helpful for developers
- NOT include unnecessary details
- Return ONLY the description text (no title, no bullet points, no explanations)

Title: {title}
Language: {language}
Content:
{content}
"""

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        description = response.text.strip()

        return jsonify({"description": description})

    except Exception as e:
        import traceback
        error_msg = str(e) if str(e) else "Unknown error occurred"
        return jsonify({
            "error": error_msg,
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }), 500



# route for handling tags auto-generation
@autogen_bp.route('/autogen/tags', methods=['POST'])
@jwt_required()
def generate_tags():
    try:
        data = request.get_json()
        content = data.get("content", "")
        language = data.get("language", "")
        title = data.get("title", "")

        prompt = f"""
Based on the following code snippet or technical content, generate 3 to 6 SHORT, meaningful TAGS.

Rules:
- Tags must be single words or very short phrases.
- DO NOT include '#', bullet points, numbering, or explanations.
- DO NOT include quotes or formatting.
- Return ONLY the tags separated by commas (example: sorting, python, arrays).
- No extra text before or after.

Title: {title}
Language: {language}
Content:
{content}
"""

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        tags = response.text.strip()

        return jsonify({"tags": tags})

    except Exception as e:
        import traceback
        error_msg = str(e) if str(e) else "Unknown error occurred"
        return jsonify({
            "error": error_msg,
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }), 500
