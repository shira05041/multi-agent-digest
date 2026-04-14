import os
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("formatter")

INPUT_FILE = "data/prioritized.txt"
OUTPUT_FILE = "output/daily_digest.md"


def format_to_markdown():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    today = datetime.now().strftime("%Y-%m-%d")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        output.write(f"# Your Daily AI Digest - {today}\n\n")
        output.write(f"**Date:** {today}\n\n")
        output.write("## Top Insights\n\n")
        for line in lines:
            if "] " in line:
                score = line.split("]")[0][1:]
                content = line.split("] ", 1)[1]
                output.write(f"- **Priority {score}**: {content}\n")
            else:
                output.write(f"- {line}\n")

    logger.info(f"Digest written to {OUTPUT_FILE}")


if __name__ == "__main__":
    format_to_markdown()