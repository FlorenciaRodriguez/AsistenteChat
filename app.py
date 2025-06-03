from flask import Flask, render_template, request, jsonify
import os
import openai
import time

# Inicializar Flask
app = Flask(__name__)

# Configurar clave de API
openai.api_key = os.environ.get("OPENAI_API_KEY")
ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    # Crear nuevo thread
    thread = openai.beta.threads.create()
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Ejecutar el asistente
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Esperar a que el asistente responda
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    # Obtener la respuesta
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value.strip()
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
