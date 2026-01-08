from flask import Flask, request, jsonify
import openai

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Pega tu API Key de OpenAI aquí (Empieza con sk-...)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/analizar_jugador', methods=['POST'])
def analizar():
    data = request.json
    prompt_usuario = data.get('prompt', '')

    print(f"📩 Recibido prompt de Roblox (Longitud: {len(prompt_usuario)})")

    try:
        # Enviamos a ChatGPT (Modelo gpt-3.5-turbo o gpt-4)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un analista de comportamiento en un entorno virtual."},
                {"role": "user", "content": prompt_usuario}
            ],
            max_tokens=200
        )

        resultado = response.choices[0].message['content']
        print("✅ Respuesta generada:", resultado)

        return jsonify({"respuesta": resultado})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"respuesta": "Error al conectar con la IA."}), 500


if __name__ == '__main__':
    app.run(port=5000)
