
from app import app
from app.routes import load_data  # Ensure load_data is accessible and needed
import os

from app.s3_downloader import download_files_from_s3  # Adjust import based on your structure

def setup_model_and_tokenizer():
    bucket_name = 'trainedllm'
    local_base_dir = "/Users/gautami/Desktop/Gautami/Job/Cleric Project/AWS_LLM"

    model_files = [
        'models/config.json',
        'models/generation_config.json',
        'models/model.safetensors',
    ]

    tokenizer_files = [
        'tokenizers/added_tokens.json',
        'tokenizers/special_tokens_map.json',
        'tokenizers/spiece.model',
        'tokenizers/tokenizer_config.json',
    ]

    local_model_dir = os.path.join(local_base_dir, 'model')
    local_tokenizer_dir = os.path.join(local_base_dir, 'tokenizer')

    os.makedirs(local_model_dir, exist_ok=True)
    os.makedirs(local_tokenizer_dir, exist_ok=True)


    download_files_from_s3(bucket_name, model_files, local_model_dir)
    download_files_from_s3(bucket_name, tokenizer_files, local_tokenizer_dir)
    

if __name__ == "__main__":
    setup_model_and_tokenizer()  # Setup model and tokenizer before starting the app
    load_data()  # Load data from file on startup
    app.run(debug=True)
    

