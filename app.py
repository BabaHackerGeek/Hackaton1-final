from flask import Flask, jsonify, request, render_template
from models import db, UserPreferences
from numverify import validate_number
from hackaton1 import find_best_plan
import json

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialiser la base de données
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    user_data = request.form
    phone_number = user_data.get('phone')
    country = user_data.get('country')
    required_data = int(user_data.get('data'))
    required_minutes = int(user_data.get('minutes'))

    # Validation du numéro de téléphone via Numverify
    if validate_number(phone_number):
        # Recherche des préférences existantes
        preferences = UserPreferences.query.filter_by(phone=phone_number).first()
        if not preferences:
            preferences = UserPreferences(phone=phone_number, country=country, data=required_data, minutes=required_minutes)
            db.session.add(preferences)
            db.session.commit()
        
        # Charger les données du fichier JSON
        with open('data/plans.json', 'r') as file:
            plans = json.load(file).get(country.capitalize(), {}).get('Operators', [])

        # Trouver le meilleur plan
        best_plan, other_plans = find_best_plan(plans, required_data, required_minutes)
        return jsonify({"best_plan": best_plan, "other_plans": other_plans})
    else:
        return jsonify({"error": "Invalid phone number"}), 400

if __name__ == "__main__":
    app.run(debug=True)
