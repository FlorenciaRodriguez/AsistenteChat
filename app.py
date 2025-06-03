from flask import Flask, render_template, request, jsonify
import subprocess
import os
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    prompt = f"""Sos un asistente experto en productos de cosmética natural.
Respondé en español y con tono amable. Usá solo información del catálogo.
Cliente: {user_input}
Asistente:"""

    result = subprocess.run(
        ["ollama", "run", "llama3:8b-instruct"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return jsonify({"response": result.stdout.strip()})

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
