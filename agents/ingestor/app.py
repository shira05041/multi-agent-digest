import os
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger =  logging.getLogger("ingestor")

INPUT_DIR = "./data/input"
OUTPUT_FILE = "data/output/ingested_data.txt"

def ingest():
    content = ""
    files_processed = 0
    for filename in sorted(os.listdir(INPUT_DIR)):
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content += f"\n--- {filename} ---\n"
                    content += f.read() + "\n"
                    files_processed += 1
            except Exception as e:
                logger.error(f"Failed to read {filename}: {e}")

    if files_processed == 0:
        logger.warning("No files found in input directory.")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as uotput_file:
        uotput_file.write(content)
    logger.info(f"Ingested  {files_processed} files into {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest()        


