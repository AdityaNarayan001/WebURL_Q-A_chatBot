import ollama

def chat(prompt, image_path):
    print("🔍 Generating response...")
    response = ollama.chat(
        model="llava",
        messages=[{"role": "user", "content": prompt, "images": [image_path]}]
    )
    print(response["message"]["content"])
