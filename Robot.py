# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, jsonify, make_response, request
import random

app = Flask(__name__)

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


@app.route('/status', methods=['GET'])
def status():
    # Simula la elección aleatoria de un sistema averiado
    damaged_system = random.choice(list(systems.keys()))
    return jsonify({"damaged_system": damaged_system})

@app.route('/repair-bay', methods=['GET'])
def repair_bay():
    # Obtenemos el sistema dañado desde los parámetros de consulta
    damaged_system = request.args.get('damaged_system')
    if not damaged_system or damaged_system not in systems:
        return make_response("Invalid damaged system", 400)
    
    # Generamos la página HTML con el código del sistema
    repair_code = systems[damaged_system]
    html_content = f"""
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
    return html_content

@app.route('/teapot', methods=['POST'])
def teapot():
    # Responde con el código de estado 418 (I'm a teapot)
    return make_response("I'm a teapot", 418)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)