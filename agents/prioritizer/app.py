import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("prioritizer")

INPUT_FILE = "data/summary.txt"
OUTPUT_FILE = "data/prioritized.txt"

PRIORITY_KEYWORDS = [
    "urgent",
    "today",
    "asap",
    "important",
    "high priority",
    "critical",
    "deadline",
]


def score_line(line):
    """Count how many priority keywords appear in a line."""
    lower_line = line.lower()
    return sum(1 for kw in PRIORITY_KEYWORDS if kw in lower_line)


def prioritize():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    scored = [(line, score_line(line)) for line in lines.strip()]
    scored.sort(key=lambda x: x[1], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        for line, score in scored:
            output_file.write(f"[{score}] {line}\n")

    logger.info(
        f"prioritized {len(lines)} lines from {INPUT_FILE} and wrote to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    prioritize()
