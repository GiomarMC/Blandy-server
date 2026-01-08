from flask import Flask, request, jsonify
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


@app.route('/')
def home():
    return "¡Servidor de IA para Roblox está ACTIVO!", 200


@app.route('/analizar_jugador', methods=['POST'])
def analizar_jugador():
    try:
        data = request.json
        prompt_roblox = data.get('prompt', '')

        print(f"📩 Recibido prompt de Roblox (Longitud: {len(prompt_roblox)})")

        if not prompt_roblox:
            return jsonify({"error": "No se recibió prompt"}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un psicólogo experto en análisis de comportamiento en videojuegos."},
                {"role": "user", "content": prompt_roblox}
            ],
            max_tokens=150,
            temperature=0.7
        )

        analisis = response.choices[0].message.content.strip()

        print("✅ Análisis generado correctamente")
        return jsonify({"respuesta": analisis})

    except Exception as e:
        print(f"❌ Error interno: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
