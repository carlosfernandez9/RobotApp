# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, jsonify, make_response#, request
import random

app = Flask(__name__)

# Global variable to store the damaged system
damaged_system = None

# Lista de sistemas posibles y sus códigos
systems = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

@app.route('/')
def home():
    return ("Bienvenido a la API de Reparación Espacial. Usa las rutas disponibles para interactuar con la API.", 200)

# First GET /status to get the damaged system
@app.route('/status', methods=['GET'])
def status():
    global damaged_system
    # You can choose the damaged system randomly, for example:
    damaged_system = random.choice(list(systems.keys()))  # Or pick it dynamically based on your logic
    
    # Return the damaged system as JSON
    return jsonify({"damaged_system": damaged_system}), 200


# Second GET /repair-bay to get the repair bay page
@app.route('/repair-bay', methods=['GET'])
def repair_bay():
    global damaged_system
    
    if damaged_system is None:
        return jsonify({"error": "No damaged system found. Please call /status first."}), 400
    
    # Mapping of damaged systems to repair codes
    repair_codes = {
        "navigation": "NAV-01",
        "communications": "COM-02",
        "life_support": "LIFE-03",
        "engines": "ENG-04",
        "deflector_shield": "SHLD-05"
    }
    
    # Get the repair code for the damaged system
    repair_code = repair_codes.get(damaged_system, "Unknown")
    
    # Generate HTML response
    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{repair_code}</div>
    </body>
    </html>
    """
    
    # Return the HTML response with the correct repair code
    return make_response(html_response, 200)

@app.route('/teapot', methods=['POST'])
def teapot():
    # Responde con el código de estado 418 (I'm a teapot)
    return make_response("I'm a teapot", 418)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)