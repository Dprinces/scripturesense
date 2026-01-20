import os
import sys
import zipfile
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_ZIP = "data/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR = "data/models/vosk-model-small-en-us-0.15"

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        logging.info(f"File already exists: {dest_path}")
        return

    logging.info(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
    logging.info("Download complete.")

def extract_zip(zip_path, extract_to):
    logging.info(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    logging.info("Extraction complete.")

def main():
    os.makedirs("data/models", exist_ok=True)
    
    if os.path.exists(MODEL_DIR):
        logging.info(f"Model already installed at {MODEL_DIR}")
        return

    download_file(MODEL_URL, MODEL_ZIP)
    extract_zip(MODEL_ZIP, "data/models")
    
    # Cleanup
    if os.path.exists(MODEL_ZIP):
        os.remove(MODEL_ZIP)
        logging.info("Removed zip file.")
        
    logging.info("Vosk setup complete!")

if __name__ == "__main__":
    main()
