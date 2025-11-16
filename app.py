from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_service import generate_social_post

app = Flask(__name__)
CORS(app)

@app.get("/")
def home():
    return {"message": "AI Social Post Generator API Running"}

@app.post("/api/generate_post")
def generate_post():
    data = request.json
    messy_text = data.get("messy_text", "")

    if not messy_text:
        return jsonify({"error": "messy_text is required"}), 400
    
    try:
        response_json = generate_social_post(messy_text)
        return jsonify(response_json)
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to generate post"}), 500

if __name__ == "__main__":
    app.run(debug=True)
