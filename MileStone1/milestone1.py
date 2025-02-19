from flask import Flask, jsonify, render_template, url_for
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
    name = db.Column(db.String(100), unique=True, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Seed initial data
def seed_data():
    if not Model.query.first():  # Only seed if empty
        initial_models = ["openai/gpt-3.5", "anthropic/claude-v1", "gemini/gemini-alpha"]
        for model_name in initial_models:
            db.session.add(Model(name=model_name))
        db.session.commit()

with app.app_context():
    seed_data()

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
