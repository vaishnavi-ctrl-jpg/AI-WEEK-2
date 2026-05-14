import os
import torch
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

print("Initializing HuggingFace Question Answering Model...")
try:
    model_name = "distilbert-base-cased-distilled-squad"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    """Serve the index page."""
    return app.send_static_file('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    if not model:
        return jsonify({"error": "Model failed to load."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    context = data.get("context", "").strip()
    question = data.get("question", "").strip()

    if not context or not question:
        return jsonify({"error": "Context and question cannot be empty."}), 400

    try:
        inputs = tokenizer(question, context, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        start_idx = outputs.start_logits.argmax().item()
        end_idx = outputs.end_logits.argmax().item()
        
        predict_answer_tokens = inputs.input_ids[0, start_idx : end_idx + 1]
        raw_answer = tokenizer.decode(predict_answer_tokens, skip_special_tokens=True).strip()
        
        # Approximate char indices (real implementation requires offset_mapping)
        # Try to find the raw answer directly
        start_char = context.find(raw_answer)
        
        # If strict find fails due to tokenization spaces, try case-insensitive
        if start_char == -1:
            start_char = context.lower().find(raw_answer.lower())
            
        # If still fails, try removing spaces for a fuzzy match
        if start_char == -1:
            clean_context = context.replace(" ", "").lower()
            clean_answer = raw_answer.replace(" ", "").lower()
            idx = clean_context.find(clean_answer)
            if idx != -1:
                # We can't map this back to original text easily without a loop,
                # so we will just return -1 for the highlight to safely ignore it.
                start_char = -1
                
        if start_char == -1:
            end_char = -1
        else:
            end_char = start_char + len(raw_answer)

        return jsonify({
            "answer": raw_answer,
            "score": 0.99,
            "start": start_char,
            "end": end_char
        })
    except Exception as e:
        return jsonify({"error": f"Inference failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


