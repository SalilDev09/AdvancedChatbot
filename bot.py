from transformers import AutoModelForCausalLM, AutoTokenizer
from diffusers import StableDiffusionPipeline
from PIL import Image
import pyttsx3
import torch
import os
import random

# Create folders
os.makedirs("images", exist_ok=True)
os.makedirs("voices", exist_ok=True)

# Load chatbot
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Load image generator
image_model = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
).to("cuda")  # Use CPU if no GPU

# Initialize text-to-speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def generate_image(prompt, filename=None):
    if filename is None:
        filename = f"images/{random.randint(1000,9999)}.png"
    image = image_model(prompt).images[0]
    image.save(filename)
    return filename

print("AdvancedChatbot is running! Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        speak("Goodbye!")
        break
    elif user_input.lower().startswith("generate image:"):
        prompt = user_input[len("generate image:"):].strip()
        img_path = generate_image(prompt)
        print(f"Bot: Image generated at {img_path}")
        speak("Here is your image.")
    else:
        inputs = tokenizer(user_input + tokenizer.eos_token, return_tensors="pt")
        outputs = model.generate(
            inputs["input_ids"], max_length=1000, pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("Bot:", response)
        speak(response)
