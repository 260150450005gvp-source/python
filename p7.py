from google import genai
from dotenv import load_dotenv
import argparse
import logging
import os
import json

load_dotenv()
logging.basicConfig(
    filename="logs/summarizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# API key
api_key = os.getenv("GEMINI_API_KEY")
# Create folders
os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Create Gemini client
client = genai.Client(api_key=api_key)

# User input  
parser = argparse.ArgumentParser(description='AI Summarizer CLI Tool')
parser.add_argument('--input', required=True, help='Path to target text file')
parser.add_argument('--output', required=True, help='Path to target text file')
args = parser.parse_args()
logging.info("Program started.")
# Read and preprocess the text
def read_and_preprocess(file):
    logging.info("Processing input file: %s", file)
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        return ""

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            return content.strip()

    except IOError as e:
        print(f"Error reading file: {e}")
        return ""

# Read text
text = read_and_preprocess(args.input)

if not text:
    print("File is empty or not found")

else:
    # Word count
    word_count = len(text.split())

    # Prompt 
    prompt = f"""
    Summarize this text in 2-3 line ,
        

    Text:
    {text}
    """

    try:
        response = client.models.generate_content(
        model="gemini-3.6-flash",
         contents=prompt
        )
        

        result = response.text
        logging.info("Summary generated successfully.")
        # Convert to JSON
        

        # Save output
       
# Save output
        with open(args.output, "w", encoding="utf-8") as f:
         f.write(result)
        logging.info("Summary saved to: %s", args.output)
        print(result)
        print(f"Summary saved to {args.output}")
    except (json.JSONDecodeError, Exception) as e:
     print(f"Error: {e}")
    finally:
     logging.info("Program ended.")
