import os
import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

app = FastAPI(title="Document Oracle API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    context: str
    question: str

print("Initializing HuggingFace Question Answering Model...")
try:
    model_name = "distilbert-base-cased-distilled-squad"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    raw_model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    
    # Apply Dynamic Quantization to reduce memory footprint and boost CPU inference speed
    print("Applying PyTorch Dynamic Quantization (Linear layers -> int8)...")
    model = torch.quantization.quantize_dynamic(
        raw_model, {torch.nn.Linear}, dtype=torch.qint8
    )
    print("Quantized Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Note: We keep the /api/ask route defined before mounting the static files 
# at the root so that the API route takes precedence.
@app.post("/api/ask")
async def ask_question(request: QueryRequest):

    if not model:
        raise HTTPException(status_code=500, detail="Model failed to load.")

    context = request.context.strip()
    question = request.question.strip()

    if not context or not question:
        raise HTTPException(status_code=400, detail="Context and question cannot be empty.")

    try:
        inputs = tokenizer(question, context, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        start_idx = outputs.start_logits.argmax().item()
        end_idx = outputs.end_logits.argmax().item()
        
        predict_answer_tokens = inputs.input_ids[0, start_idx : end_idx + 1]
        raw_answer = tokenizer.decode(predict_answer_tokens, skip_special_tokens=True).strip()
        
        # Approximate char indices
        start_char = context.find(raw_answer)
        
        if start_char == -1:
            start_char = context.lower().find(raw_answer.lower())
            
        if start_char == -1:
            clean_context = context.replace(" ", "").lower()
            clean_answer = raw_answer.replace(" ", "").lower()
            idx = clean_context.find(clean_answer)
            if idx != -1:
                start_char = -1
                
        if start_char == -1:
            end_char = -1
        else:
            end_char = start_char + len(raw_answer)

        return {
            "answer": raw_answer,
            "score": 0.99,
            "start": start_char,
            "end": end_char
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

# Mount static files at the root
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)

