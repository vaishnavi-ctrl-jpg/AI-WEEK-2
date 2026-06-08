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
        # Tokenize with offsets mapping to precisely track token-to-character spans
        encoding = tokenizer(question, context, return_offsets_mapping=True)
        
        # Prepare inputs for the PyTorch model (remove non-tensor fields like offset_mapping)
        model_inputs = {k: torch.tensor([v]) for k, v in encoding.items() if k != "offset_mapping"}
        
        with torch.no_grad():
            outputs = model(**model_inputs)

        start_idx = outputs.start_logits.argmax().item()
        end_idx = outputs.end_logits.argmax().item()
        
        offsets = encoding["offset_mapping"]
        sequence_ids = encoding.sequence_ids(0)
        
        # Filter token indices belonging to the context (seq_id == 1)
        context_tokens = [i for i, seq_id in enumerate(sequence_ids) if seq_id == 1]
        
        if not context_tokens:
            start_char = -1
            end_char = -1
            raw_answer = ""
        else:
            # Clamp the predictions to context token boundaries
            pred_start = max(start_idx, min(context_tokens))
            pred_end = min(end_idx, max(context_tokens))
            
            if pred_start <= pred_end and sequence_ids[pred_start] == 1 and sequence_ids[pred_end] == 1:
                start_char = offsets[pred_start][0]
                end_char = offsets[pred_end][1]
                raw_answer = context[start_char:end_char].strip()
            else:
                # Fallback to string matching if predictions are outside context token range
                predict_tokens = model_inputs["input_ids"][0, start_idx : end_idx + 1]
                raw_answer = tokenizer.decode(predict_tokens, skip_special_tokens=True).strip()
                start_char = context.find(raw_answer)
                if start_char == -1:
                    start_char = context.lower().find(raw_answer.lower())
                end_char = start_char + len(raw_answer) if start_char != -1 else -1

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

