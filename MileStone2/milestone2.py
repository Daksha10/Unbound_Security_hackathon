from flask import Flask, jsonify, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Model table
class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)  # Add provider field
    name = db.Column(db.String(100), unique=True, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Seed initial data
def seed_data():
    if not Model.query.first():  # Only seed if empty
        initial_models = [
            {"provider": "openai", "name": "gpt-3.5"},
            {"provider": "anthropic", "name": "claude-v1"},
            {"provider": "gemini", "name": "gemini-alpha"}
        ]
        for model in initial_models:
            db.session.add(Model(provider=model["provider"], name=model["name"]))
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_data()

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    
    provider = data.get("provider")
    model = data.get("model")
    prompt = data.get("prompt")

    # Validate input fields
    if not provider or not model or not prompt:
        return jsonify({"error": "Missing provider, model, or prompt"}), 400

    # Check if provider and model exist in DB
    valid_model = Model.query.filter_by(provider=provider, name=model).first()
    if not valid_model:
        return jsonify({"error": "Invalid provider or model"}), 400

    # Stub response generation (Dummy Response for Each Provider)
    response_text = generate_stub_response(provider, model)

    return jsonify({
        "provider": provider,
        "model": model,
        "response": response_text
    })

# Function to Generate Dummy Responses
def generate_stub_response(provider, model):
    responses = {
        "openai": f"OpenAI: Processed your prompt with advanced language understanding. Response ID: openai_response_001",
        "anthropic": f"Anthropic: Your prompt has been interpreted with ethical AI principles. Response ID: anthropic_response_002",
        "gemini": f"Gemini: Your request has been handled with precision. Response ID: gemini_response_003"
    }
    return responses.get(provider, "Unknown Provider Response")

@app.route('/')
def home():
    return render_template('index.html')

# Route to fetch supported models
@app.route('/models', methods=['GET'])
def get_models():
    models = Model.query.all()
    model_list = [model.name for model in models]
    return jsonify(model_list)

if __name__ == '__main__':
    app.run(debug=True)
