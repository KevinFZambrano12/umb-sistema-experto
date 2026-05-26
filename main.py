from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Equivalente al manejo de CORS del código GCP

# ══════════════════════════════════
# BASE DE CONOCIMIENTO (Reglas)
# ══════════════════════════════════
reglas_diagnostico = [
    {
        "sintomas": ["no enciende", "sin ruidos"],
        "diagnostico": "Fallo en la fuente de poder o cable desconectado.",
        "certeza": 0.9
    },
    {
        "sintomas": ["no enciende", "pitidos continuos"],
        "diagnostico": "Error en la memoria RAM. Verifique que esté bien conectada.",
        "certeza": 0.85
    },
    {
        "sintomas": ["enciende", "pantalla azul"],
        "diagnostico": "Conflicto de drivers o falla crítica de hardware (posible disco duro).",
        "certeza": 0.75
    },
    {
        "sintomas": ["lento", "ruido rasgueo"],
        "diagnostico": "Disco duro mecánico (HDD) a punto de fallar. Respalde sus datos inmediatamente.",
        "certeza": 0.95
    }
]

# ══════════════════════════════════
# MOTOR DE INFERENCIA (Forward Chaining)
# ══════════════════════════════════
def evaluar_sintomas(sintomas_usuario):
    mejor_coincidencia = {
        "diagnostico": "No se pudo determinar el problema. Consulte a un técnico presencial.",
        "certeza": 0.0
    }
    for regla in reglas_diagnostico:
        match = all(s in sintomas_usuario for s in regla["sintomas"])
        if match and regla["certeza"] > mejor_coincidencia["certeza"]:
            mejor_coincidencia = regla
    return mejor_coincidencia

# ══════════════════════════════════
# ENDPOINT REST (equivalente al trigger HTTP de Cloud Functions)
# ══════════════════════════════════
@app.route("/diagnosticar", methods=["POST", "OPTIONS"])
def api_sistema_experto():
    if request.method == "OPTIONS":
        return "", 204  # preflight CORS

    data = request.get_json(silent=True)

    if data and "sintomas" in data:
        resultado = evaluar_sintomas(data["sintomas"])
        return jsonify(resultado), 200
    else:
        return jsonify({"error": "Debe enviar una lista de síntomas."}), 400

# Render espera que la app escuche en el puerto del entorno
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)