
import os
import json
import logging
from datetime import datetime
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("API_KEY")
)

os.makedirs("output", exist_ok=True)

logging.basicConfig(
    filename="output/app.log",
    level=logging.INFO
)

path = input("Enter file or folder path: ")

if os.path.isfile(path):
    files = [path]

elif os.path.isdir(path):
    files = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith(".txt")
    ]

else:
    print("Invalid path")
    exit()

output_file = "output/summaries.json"

if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        try:
            old_summaries = json.load(f)
            if not isinstance(old_summaries, list):
                old_summaries = []
        except json.JSONDecodeError:
            old_summaries = []
else:
    old_summaries = []

existing_names = {
    item.get("file_name")
    for item in old_summaries
    if isinstance(item, dict)
}

summaries = []

for file in files:

    filename = os.path.basename(file)
    print("Processing:", filename)

    try:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            print("Empty file")
            logging.info(
                f"{datetime.now()} - {filename} - Failure - Empty file"
            )
            continue

        prompt = f"""
You are an expert text summarizer.

Summarize the given text and return ONLY a valid JSON object.
Do not include Markdown, code fences, or extra explanation.

Follow these requirements:
1. "title": A short, meaningful title describing the text.
2. "summary": A clear summary written in 2-3 concise lines.
3. "keywords": A list of 3-5 important keywords from the text.
4. "word_count": The exact number of words in the original text.
   Use the provided word count; do not estimate it.

Original text word count: {len(text.split())}

Text to summarize:
{text}

Return JSON in this structure:
{{
    "title": "Text title",
    "summary": "Summary line one. Summary line two.",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "word_count": {len(text.split())}
}}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        result = (response.text or "").strip()
        result = result.replace("```json", "").replace("```", "").strip()

        data = json.loads(result)

        required = ["title", "summary", "keywords", "word_count"]

        if (
            isinstance(data, dict)
            and all(field in data for field in required)
            and isinstance(data["title"], str)
            and isinstance(data["summary"], str)
            and isinstance(data["keywords"], list)
            and isinstance(data["word_count"], int)
        ):
            data["file_name"] = filename

            if filename not in existing_names:
                summaries.append(data)
                existing_names.add(filename)
                print("Success")
            else:
                print("Already exists; duplicate skipped")

            logging.info(
                f"{datetime.now()} - {filename} - Success"
            )
            print("Timestamp:", datetime.now())

        else:
            print("Required field missing or invalid")
            logging.error(
                f"{datetime.now()} - {filename} - Required field missing or invalid"
            )

    except json.JSONDecodeError:
        print("Invalid JSON")
        logging.error(
            f"{datetime.now()} - {filename} - JSON parsing error"
        )

    except Exception as e:
        print("Error:", e)
        logging.error(
            f"{datetime.now()} - {filename} - Failure - {e}"
        )

old_summaries.extend(summaries)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        old_summaries,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Done!")
