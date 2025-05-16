import os
import requests
from flask import Request, jsonify
from dotenv import load_dotenv

load_dotenv()

def handler(request: Request):
    if request.method != 'POST':
        return jsonify({"error": "Only POST method allowed"}), 405

    script = request.form.get("script")
    if not script:
        return jsonify({"error": "No script provided"}), 400

    prompt = f"Analyze this teleserye script. Identify any cliché plot points, tropes, or character patterns and suggest improvements:\n\n{script}"

    headers = {
        'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = r.json()
        analysis = data.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
        return jsonify({
            "ai_analysis": analysis,
            "basic_analysis": {}
        })

    except Exception as e:
        return jsonify({"error": f"OpenRouter request failed: {str(e)}"}), 500