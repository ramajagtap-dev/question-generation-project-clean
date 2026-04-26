from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate(text):
    input_text = f"""
You are a question generator.
Generate 3 meaningful questions ONLY from this paragraph:

{text}
"""

    inputs = tokenizer(input_text, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_length=128,
        do_sample=True,
        temperature=0.7
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print(generate("AI is used in healthcare and education"))