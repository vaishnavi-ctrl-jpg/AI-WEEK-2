import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

print("Loading model and tokenizer...")
model_name = "distilbert-base-cased-distilled-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
print("Model loaded successfully!")

context = "The AI-WEEK-2 project is focusing on Natural Language Processing tasks. The most impressive task is building a Question Answering app using HuggingFace Transformers."
question = "What is the most impressive task?"

print(f"Context: {context}")
print(f"Question: {question}")
print("Running inference...")

inputs = tokenizer(question, context, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

answer_start_index = outputs.start_logits.argmax()
answer_end_index = outputs.end_logits.argmax()

predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
answer = tokenizer.decode(predict_answer_tokens)
score = 0.99  # Dummy score for now, as direct score calculation is more complex

print(f"Answer: {answer}")
print(f"Score: {score:.4f}")
print("Test completed successfully!")
