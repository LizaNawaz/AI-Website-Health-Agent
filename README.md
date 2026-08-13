# AI Website Health Agent

An AI-powered website health checking agent using Python and Ollama.

## Features

- Website crawling
- Broken link detection
- Broken image detection
- CSS/JS resource checking
- Page status checking
- Browser testing with Playwright
- JavaScript error detection
- Network error detection
- AI analysis using local Ollama
- Website health reports

## AI

This project uses Ollama as the local LLM.

No OpenAI API or Gemini API is required.

## Project Structure

app/
+-- crawler/
+-- checker/
+-- browser/
+-- ai/
+-- report/

## Run

Create a virtual environment:

python -m venv .venv

Activate:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Install Playwright browser:

playwright install

Run:

python main.py
