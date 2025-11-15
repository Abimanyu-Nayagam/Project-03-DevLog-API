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
