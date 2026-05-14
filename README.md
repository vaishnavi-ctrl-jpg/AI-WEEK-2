# AI Internship Week 2: The Document Oracle (NLP QnA App)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Core_Engine-EE4C2C.svg?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E.svg?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg?style=for-the-badge)]()

## 📌 Project Overview
This project satisfies the **Week 2 - Natural Language Processing** requirement. 
Going beyond standard text classification tutorials, this project implements a state-of-the-art **Document Oracle**. It is an interactive, web-based Question Answering (QnA) dashboard powered by a pre-trained HuggingFace Transformer model.

The application allows users to load any long-form contextual text, ask natural language questions, and instantly receive precise answers highlighted directly within the source text.

---

## 🧠 System Architecture

The application is built using a modern decoupled architecture:

```mermaid
graph LR
    subgraph Frontend "Synapse Glass UI"
        UI[Web Dashboard]
        Input[Context & Question]
        Highlighter[Dynamic Text Highlighter]
    end
    
    subgraph Backend "Python Flask API"
        API[POST /api/ask]
    end
    
    subgraph NLP Engine "HuggingFace Hub"
        Tokenizer[AutoTokenizer]
        Model[DistilBERT SQuAD Model]
        Torch((PyTorch Tensors))
    end
    
    Input -->|JSON Payload| API
    API --> Tokenizer
    Tokenizer --> Torch
    Torch --> Model
    Model -->|Start/End Logits| Tokenizer
    Tokenizer -->|Decoded Answer & Index| API
    API -->|JSON Response| Highlighter
    Highlighter --> UI
```

---

## 🚀 Technical Highlights & Features
1. **State-of-the-Art Transformer**: Utilizes `distilbert-base-cased-distilled-squad` for high-accuracy, lightning-fast inference on CPU environments without requiring GPU clusters.
2. **Custom Inference Logic**: Built explicit PyTorch tensor passing (`AutoModelForQuestionAnswering`) instead of generic pipelines for maximum control over offset mapping and logit extraction.
3. **Synapse Glass Design System**: The frontend is engineered using a custom glassmorphism design spec (`DESIGN.md`) featuring deep obsidian backgrounds, translucent layers, and cyan synaptic glows.
4. **Dynamic Span Highlighting**: The JavaScript layer parses the AI response and dynamically injects `<mark>` elements directly into the original contextual text to visually prove the source of the answer.

## 🛠️ Tech Stack
* **Backend**: Python 3, Flask, Flask-CORS
* **Machine Learning**: PyTorch, HuggingFace Transformers (`AutoTokenizer`, `AutoModelForQuestionAnswering`)
* **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript
* **Design Spec**: [DESIGN.md](DESIGN.md) open-source standard

## 🏃‍♂️ How to Run Locally

1. **Install Dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install torch transformers flask flask-cors
   ```
   *(Note: For Windows CPU environments, it is highly recommended to install torch via the cpu index to save space: `pip install torch --index-url https://download.pytorch.org/whl/cpu`)*

2. **Start the Server:**
   ```bash
   python app.py
   ```
   *The server will download the model weights (approx. 260MB) on the very first run.*

3. **Access the Dashboard:**
   Open your browser and navigate to:
   **[http://localhost:5000](http://localhost:5000)**

4. **Test the Oracle:**
   - Click "Load Sample Paper" or paste your own text.
   - Ask a question based on the text.
   - Watch the AI compute and highlight the answer!
