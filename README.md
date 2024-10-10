# Ollama Web Summarization

This repository contains a Python-based tool for summarizing web content using the Ollama API. It scrapes articles from URLs, cleans and processes the HTML content, and generates summaries using a pre-trained language model. The repository also includes a rich-based logging utility for improved console output.

## Features

- Fetches web content based on search queries.
- Cleans and extracts the readable part of the content.
- Uses the Ollama API to generate summaries.
- Saves summaries with autogenerated filenames based on content and query.
- Includes a rich-based logging system for structured and styled console outputs.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `readability-lxml`
- `ollama`
- `html2text`
- `pyyaml`
- `rich`

## Installation

Clone the repository:

```bash
git clone
cd ollama-web-summarization
```
Install the required Python packages:
```bash
pip install -r requirements.txt
```
Set up your config.yaml file with the following parameters:
```bash
search_url: "https://example.com"
ollama_url: "https://api.ollama.com"
ollama_model: "llama-2"
output_directory: "./output"
user_prompt: "Summarize the following content: {texts}."
```
## Usage

To summarize web content based on a search query, run the following command:
```bash
python ollama_web_summarize.py "Your search query"
```
The script will fetch the URLs, clean the content, generate a summary using the Ollama API, and save it to the output directory with an autogenerated filename.

## Logging
The repository includes a rich-based logging utility for styled console output. The logging outputs steps, results, and errors clearly in the terminal.

## Files
- ollama_web_summarize.py: Main script to fetch URLs, clean the content, and generate summaries.
- rich_logger.py: Utility for styled logging using rich.

## License
This project is licensed under the MIT License.


