from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


@app.route('/')
def home():
    return "¡Servidor con GEMINI (Google) activo!", 200


@app.route('/analizar_jugador', methods=['POST'])
def analizar_jugador():
    try:
        data = request.json
        prompt_roblox = data.get('prompt', '')

        print(f"📩 Recibido prompt de Roblox (Longitud: {len(prompt_roblox)})")

        if not prompt_roblox:
            return jsonify({"error": "No se recibió prompt"}), 400

        prompt_completo = (
            "Eres un psicólogo experto en análisis de comportamiento en videojuegos. "
            "Analiza los siguientes datos y da un perfil breve:\n\n" + prompt_roblox
        )

        response = model.generate_content(prompt_completo)
        analisis = response.text

        print("✅ Análisis de Gemini generado correctamente")
        return jsonify({"respuesta": analisis})

    except Exception as e:
        print(f"❌ Error interno: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
