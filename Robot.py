# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, jsonify, make_response, request, redirect
import json
import random

app = Flask(__name__)

# Global variable to store the damaged system
damaged_system = None
pressure = None

# Lista de sistemas posibles y sus códigos
systems = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

@app.before_request
def enforce_https():
    if request.is_secure:
        url = request.url.replace("https://", "http://")
        return redirect(url, 301)

@app.route('/')
def home():
    return ("Bienvenido a la API de Reparación Espacial. Usa las rutas disponibles para interactuar con la API.", 200)

# First GET /status to get the damaged system
# @app.route('/status', methods=['GET'])
# def status():
#     global damaged_system
#     # You can choose the damaged system randomly, for example:
#     damaged_system = random.choice(list(systems.keys()))  # Or pick it dynamically based on your logic
    
#     # Return the damaged system as JSON
#     return jsonify({"damaged_system": damaged_system}), 200

@app.route('/status', methods=['GET'])
def status():
    
    global damaged_system
    # Get the 'damaged_system' parameter from the query string
    damaged_system = request.args.get('damaged_system', default=None)

    if damaged_system:
        # If a system is selected, return that specific system
        if damaged_system in systems:
            return jsonify({"damaged_system": damaged_system}), 200
        else:
            return jsonify({"error": "Invalid system selected"}), 400
    else:
        # If no system is selected, pick a random system
        damaged_system = random.choice(list(systems.keys()))
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
    return make_response(html_response), 200

@app.route('/teapot', methods=['POST'])
def teapot():
    # Responde con el código de estado 418 (I'm a teapot)
    return make_response("I'm a teapot", 418)

@app.route('/phase-change-diagram', methods=['GET'])
def get_phase_change_data():
    
    try:
        pressure = float(request.args.get('pressure', default=None, type=float))
    
        # if pressure:
        #     if pressure >= 10:
        #         response_data = {
        #             "specific_volume_liquid": 0.0035,
        #             "specific_volume_vapor": 0.0035
        #         }
        #     elif pressure >= 0:
        #         specific_volume_liquid = (0.00245 / 9.95 * pressure) + (0.00105 - 0.00245 / 9.95 * 0.05)
        #         specific_volume_vapor = (29.9965 / -9.95 * pressure) + (0.0035 + 29.9965 / 9.95 * 10)
    
        #         response_data = {
        #             # "specific_volume_liquid": round(specific_volume_liquid, 5),
        #             # "specific_volume_vapor": round(specific_volume_vapor, 5)
                    
        #             "specific_volume_liquid": specific_volume_liquid,
        #             "specific_volume_vapor": specific_volume_vapor
                    
        #             # "specific_volume_liquid": f"{specific_volume_liquid:.4f}",
        #             # "specific_volume_vapor": f"{specific_volume_vapor:.4f}"
              
        #         }
        #     else:
        #         return jsonify({"error": "Unsupported pressure value"}), 400
    
        #     # Use json.dumps() to pretty-print the response
        #     return app.response_class(
        #         response=json.dumps(response_data, indent=2),
        #         status=200,
        #         mimetype='application/json'
        #     )
        # else:
        #     return jsonify({"error": "Pressure value is required"}), 400
    
        
        if pressure:
            if pressure >= 10:
                return jsonify({
                    "specific_volume_liquid": 0.0035,
                    "specific_volume_vapor": 0.0035
                })
                
            else: 
                specific_volume_liquid = (0.00245/9.95*pressure) + (0.00105 - (0.00245/9.95*0.05))
                specific_volume_vapor = (29.9965/-9.95*pressure) + (0.0035 + (29.9965/9.95*10))
            
                return jsonify({
                    "specific_volume_liquid": specific_volume_liquid,
                    "specific_volume_vapor": specific_volume_vapor
            }), 200
        else:
            return jsonify({
                "error": "Unsupported pressure value"
            }), 400
        
    except ValueError:
        # If the conversion to float fails, return an error message
        return jsonify({"error": "Invalid pressure value. Pressure must be a number."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)