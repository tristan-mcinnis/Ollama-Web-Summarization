import os
import requests
from bs4 import BeautifulSoup
from readability import Document
import ollama
import html2text
import yaml # type: ignore
from rich_logger import setup_logger, log_step, log_result, log_error
from rich.progress import track
from datetime import datetime
import re

# Set up Rich logger
logger = setup_logger()

def load_config():
    with open("config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

config = load_config()
logger.info("Configuration loaded")

# Fetches news URLs based on search query (but here just fetch the main URL directly)
def get_news_urls(query):
    search_url = config["search_url"]
    log_step(f"Fetching news from: {search_url}")
    return [search_url]

# Cleans and extracts readable text from a list of URLs
def get_cleaned_text(urls):
    texts = []
    for url in track(urls, description="Processing URLs"):
        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text
            text = html_to_text(html)
            texts.append(f"Source: {url}\n{text}\n\n")
            logger.info(f"Successfully processed content from {url}")
        except requests.RequestException as e:
            log_error(f"Error fetching or processing URL {url}: {e}")
    return texts

# Uses Readability to extract main text from HTML
def html_to_text(html):
    log_step("Converting HTML to readable text")
    doc = Document(html)
    return html2text.html2text(doc.summary())

# Queries Ollama's LLM using the provided texts and question
def answer_query(query, texts):
    OLLAMA_URL = config["ollama_url"]
    OLLAMA_MODEL = config["ollama_model"]

    prompt = config["user_prompt"].format(query=query, texts=' '.join(texts))
    log_step("Generating answer")
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": config["system_prompt"]},
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "options": {
                    "num_predict": 16000,
                    "temperature": 0.2
                }
            }
        )

        response.raise_for_status()
        
        content = response.json()["message"]["content"]
        log_result(content)

        # Generate title and save content
        title = generate_title(content)
        save_content(content, title)

    except requests.RequestException as e:
        log_error(f"Error calling Ollama API: {e}")
    except Exception as e:
        log_error(f"Unexpected error: {e}")

def generate_title(content):
    log_step("Generating title for the content")
    OLLAMA_URL = config["ollama_url"]
    OLLAMA_MODEL = config["ollama_model"]

    prompt = config["title_prompt"].format(content=content)

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that generates concise titles."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 0.7
                }
            }
        )

        response.raise_for_status()
        
        title = response.json()["message"]["content"].strip()
        # Remove quotation marks and any characters that are invalid in filenames
        title = re.sub(r'[<>:"/\\|?*]', '', title)
        log_result(f"Generated title: {title}")
        return title

    except requests.RequestException as e:
        log_error(f"Error calling Ollama API for title generation: {e}")
        return "Untitled"

def save_content(content, title):
    output_dir = config["output_directory"]
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{title}_{date_str}.txt"
    file_path = os.path.join(output_dir, filename)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        log_result(f"Content saved to: {file_path}")
    except IOError as e:
        log_error(f"Error saving content to file: {e}")

# Main execution
if __name__ == "__main__":
    query = " ".join(os.sys.argv[1:])
    log_step(f"Received query: {query}")
    
    urls = get_news_urls(query)
    logger.info(f"Retrieved URLs: {urls}")
    
    all_texts = get_cleaned_text(urls)
    logger.info(f"Processed {len(all_texts)} text(s) from URLs")
    
    answer_query(query, all_texts)
    log_step("Query answering process completed")
