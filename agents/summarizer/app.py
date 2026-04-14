import os
import logging
import time
from openai import OpenAI, RateLimitError, APIError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("summarizer")

INPUT_FILE = "data/ingested.txt"
OUTPUT_FILE = "data/summary.txt"

client = OpenAI()

SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes long text into key bullet points. "
    "Each bullet should be one concise sentence capturing a core insight."
)

MAX_RETRIES = 3
RETRAY_DELAY = 5  # seconds

def sumarize(text, retrise=MAX_RETRIES):
    """Call the LLM API with retray logic for rate limits."""
    for attempt in range(retrise):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system" , "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text[:8000]}
                    ],
                    max_tokens=1000,
                    temperature=0.3,
                )
            return response.choices[0].message.content
        except RateLimitError:
            wait = RETRAY_DELAY * (attempt + 1)
            logger.warning(f"Rate limit hit. Retrying in {wait} seconds...")
            time.sleep(wait)
        except APIError as e:
            logger.error(f"API error: {e}")
            raise
    raise RuntimeError("Max retries exceeded for LLM API call.") 

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    if not raw_text.strip():
        logger.warning("Empty input file. No content to summarize.")    
        summary = "No content to summarize."
    else:
        try:
            summary = sumarize(raw_text)
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            summary = f"Summarization failed: {e}"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(summary)
    logger.info(f"summarization complete. Output written to {OUTPUT_FILE}")    

if __name__ == "__main__":
    main()

