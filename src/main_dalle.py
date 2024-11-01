import os
import openai
import requests
from dotenv import dotenv_values

# Set up OpenAI credentials

CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG["KEY"] or os.environ["OPEN_AI_KEY"]
OPEN_AI_ORG = CONFIG["ORG"] or os.environ["OPEN_AI_ORG"]

openai.api_key = OPEN_AI_KEY
openai.organization = OPEN_AI_ORG

def load_file(filename: str = "") -> str:
    """Loads an arbitrary file name"""
    with open(filename, "r") as fh:
        return fh.read()

# Function to generate image using DALL-E
def generate_image_prompt(description):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=description,
        n=1
    )
    return response.data[0].url

# Function to download and save the image
def save_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image, status code: {response.status_code}")

def main():
    # Load prompt file
    prompt = load_file("prompt.txt")
    
    # Generate image
    image_url = generate_image_prompt(prompt)

    num_images = 12
    for i in range(num_images):
        image_prompt = f"{prompt} - Part {i + 1}"
        image_url = generate_image_prompt(image_prompt)
        #print(f"Image {i + 1}: {image_url}")
        save_image(image_url, f"img/image_{i + 1}.png")

if __name__ == "__main__":
    main()
