from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def obtener_modelo_valido():
    try:
        print("🔍 Buscando modelos disponibles...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   ✅ Encontrado: {m.name}")
                if 'gemini' in m.name:
                    return m.name
        return "models/gemini-1.5-flash"
    except Exception as e:
        print(f"⚠️ Error listando modelos: {e}")
        return "gemini-pro"


NOMBRE_MODELO = obtener_modelo_valido()
print(f"🤖 MODELO SELECCIONADO: {NOMBRE_MODELO}")

model = genai.GenerativeModel(NOMBRE_MODELO)


@app.route('/')
def home():
    return f"¡Servidor ACTIVO! Usando modelo: {NOMBRE_MODELO}", 200

@app.route('/analizar_jugador', methods=['POST'])
def analizar_jugador():
    try:
        data = request.json
        prompt_roblox = data.get('prompt', '')

        print(f"📩 Recibido prompt (Longitud: {len(prompt_roblox)})")

        if not prompt_roblox:
            return jsonify({"error": "No se recibió prompt"}), 400

        prompt_completo = (
            "Eres un psicólogo experto en videojuegos. "
            "Analiza brevemente (2 lineas) el comportamiento de este jugador:\n\n" + prompt_roblox
        )

        response = model.generate_content(prompt_completo)
        analisis = response.text

        print("✅ Análisis generado correctamente")
        return jsonify({"respuesta": analisis})

    except Exception as e:
        print(f"❌ Error generando respuesta: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
