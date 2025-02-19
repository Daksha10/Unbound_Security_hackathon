from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import re
import psycopg2

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Model Table
class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)

# Create the database tables and seed data
with app.app_context():
    db.create_all()

def seed_data():
    existing_models = {m.name.lower() for m in Model.query.all()}  # Ensure case insensitivity
    initial_models = [
        {"provider": "openai", "name": "gpt-3.5"},
        {"provider": "openai", "name": "gpt-4o"},
        {"provider": "anthropic", "name": "claude-v1"},
        {"provider": "gemini", "name": "gemini-alpha"},
        {"provider": "google", "name": "bard"},
        {"provider": "openai", "name": "med-gpt"},
        {"provider": "openai", "name": "financial-gpt"}
    ]
    
    for model in initial_models:
        if model["name"].lower() not in existing_models:  # Avoid duplicate case-sensitive names
            db.session.add(Model(provider=model["provider"], name=model["name"]))
    
    db.session.commit()

with app.app_context():
    seed_data()

# Database connection function
def get_db_connection():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None  # Prevent crashes if DB is unreachable

# Fetch all regex rules
@app.route('/api/regex-rules', methods=['GET'])
def get_regex_rules():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM routing_rules;")
    rules = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rules)

# Add a new regex rule

@app.route('/api/regex-rules', methods=['POST'])
def add_regex_rule():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO routing_rules (original_model, regex_pattern, redirect_model)
            VALUES (%s, %s, %s) RETURNING id;
        """, (data['original_model'], data['regex_pattern'], data['redirect_model']))
        conn.commit()
        rule_id = cur.fetchone()[0]
        cur.close()
        return jsonify({"message": "Regex rule added successfully", "id": rule_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Edit an existing regex rule
@app.route('/api/regex-rules/<int:rule_id>', methods=['PUT'])
def update_regex_rule(rule_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE routing_rules SET regex_pattern=%s, original_model=%s, redirect_model=%s WHERE id=%s;",
        ( data['regex_pattern'],data['original_model'], data['redirect_model'], rule_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Rule updated successfully"})

# Delete a regex rule
@app.route('/api/regex-rules/<int:rule_id>', methods=['DELETE'])
def delete_regex_rule(rule_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM routing_rules WHERE id=%s;", (rule_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Rule deleted successfully"})

# Admin Panel Route
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

# Function to determine redirect model based on regex rules
def get_redirect_model(user_prompt, model_name):
    conn = get_db_connection()
    if not conn:
        return model_name  # Default to original model if DB fails

    cursor = conn.cursor()

    try:
        # Fetch only relevant rules for the given model
        cursor.execute(
            """
            SELECT regex_pattern, redirect_model 
            FROM routing_rules 
            WHERE original_model = %s 
            ORDER BY LENGTH(regex_pattern) DESC
            """,  # Orders by pattern length to prioritize specific rules
            (model_name,)
        )
        rules = cursor.fetchall()

        for regex_pattern, redirect_model in rules:
            if re.search(regex_pattern, user_prompt, re.IGNORECASE):
                print(f"Match found: '{user_prompt}' → '{regex_pattern}' → Redirecting to {redirect_model}")
                return redirect_model  # Redirect model found

        return model_name  # No match, use original model

    except Exception as e:
        print(f"Error fetching routing rules: {e}")
        return model_name  # Default to original model in case of an error

    finally:
        cursor.close()
        conn.close()

# Endpoint to determine the routed model based on regex rules
@app.route("/route_prompt", methods=["POST"])
def route_prompt():
    data = request.json
    user_prompt = data.get("prompt", "").strip()
    model_name = data.get("model", "").strip()

    if not user_prompt or not model_name:
        return jsonify({"error": "Missing prompt or model"}), 400

    final_model = get_redirect_model(user_prompt, model_name)

    return jsonify({
        "query": user_prompt,
        "original_model": model_name,
        "final_model": final_model,
        "message": f"Rerouted to {final_model}" if final_model != model_name else "No reroute applied"
    })
# API to fetch unique providers
@app.route('/providers', methods=['GET'])
def get_providers():
    providers = db.session.query(Model.provider).distinct().all()
    provider_list = [p[0] for p in providers]
    return jsonify(provider_list)

# API to fetch models (optional provider filter)
@app.route('/models', methods=['GET'])
def get_models():
    provider = request.args.get('provider', '').strip()

    query = Model.query
    if provider:
        query = query.filter_by(provider=provider)

    models = query.all()
    model_list = [{"provider": model.provider, "name": model.name} for model in models]
    return jsonify(model_list)


# Chat Completion Endpoint
@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    provider = data.get("provider", "").strip().lower()
    model = data.get("model", "").strip()
    prompt = data.get("prompt", "").strip()

    if not provider or not model or not prompt:
        return jsonify({"error": "Missing provider, model, or prompt"}), 400

    # Ensure case-sensitive match against stored models
    valid_model = Model.query.filter_by(provider=provider, name=model).first()
    if not valid_model:
        return jsonify({"error": "Invalid provider or model"}), 400

    # Apply regex-based rerouting
    final_model = get_redirect_model(prompt, model)

    response_text = generate_stub_response(provider, final_model)

    return jsonify({
        "provider": provider,
        "model": final_model,
        "response": response_text
    })

# Function to Generate Dummy Responses
def generate_stub_response(provider, model):
    responses = {
        "openai": f"OpenAI: Processed your prompt with advanced AI. Response ID: {model}_response_001",
        "anthropic": f"Anthropic: Ethical AI interpreted your prompt. Response ID: {model}_response_002",
        "gemini": f"Gemini: Precision AI processed your request. Response ID: {model}_response_003",
        "google": f"Google: Bard AI has generated a response. Response ID: {model}_response_004"
    }
    return responses.get(provider, f"{provider.capitalize()}: Processed with {model}.")


# Home Route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
