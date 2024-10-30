import subprocess
import base64

def load_image_as_base64(image_path):
    """Loads an image file and encodes it to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def explain_image_with_llava(prompt_file_path):
    """Generates an explanation of the image using LLaVA via Ollama with prompt passed via stdin."""
    with open(prompt_file_path, "r") as prompt_file:
        prompt_content = prompt_file.read()
        
    # Run the command with the prompt passed via stdin
    result = subprocess.run(
        ["ollama", "run", "llava"],
        input=prompt_content,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout

def save_response(response, save_path):
    """Saves the LLaVA response to a text file."""
    with open(save_path, "w") as f:
        f.write(response)
    print(f"Response saved to {save_path}")

def main():
    # Load and encode the image as base64
    image_path = "img/generated_image.png"  # Change this to your image file path
    image_base64 = load_image_as_base64(image_path)
    
    # Prepare prompt with the base64 data and save it to a file
    prompt_content = f"[Image:{image_base64}] Please provide a detailed description of this image."
    prompt_file_path = "temp_prompt.txt"
    with open(prompt_file_path, "w") as file:
        file.write(prompt_content)
    
    # Get explanation from LLaVA
    response = explain_image_with_llava(prompt_file_path)
    if response:
        # Save the explanation to a text file
        save_path = "image_explanation.txt"
        save_response(response, save_path)

if __name__ == "__main__":
    main()
