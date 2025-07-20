from flask import Flask, render_template, request
import os
import json
import urllib.parse
import requests

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), 'languages.json'), 'r', encoding='utf-8') as f:
    language_list = json.load(f)

LINGVA_BASE = "https://lingva.ml"

@app.route('/', methods=["GET", "POST"])
def home():
    translated_text = None
    selected_language = "en"

    if request.method == "POST":
        text = request.form.get('source_text', '')
        selected_language = request.form.get('language', 'es')

        src = "auto"
        q = urllib.parse.quote(text)
        url = f"{LINGVA_BASE}/api/v1/{src}/{selected_language}/{q}"
        resp = requests.get(url)

        if resp.ok:
            data = resp.json()
            translated_text = data.get('translation') or data.get('translatedText') or str(data)
        else:
            translated_text = f"Error: {resp.status_code}"

    return render_template(
        'index.html',
        language_list=language_list,
        translated_text=translated_text,
        selected_language=selected_language
    )

if __name__ == '__main__':
    app.run(debug=True)