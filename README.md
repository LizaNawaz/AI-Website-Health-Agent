# 🔍 AI Website Health Agent

An AI-powered website health monitoring application that analyzes a website and detects broken webpages, links, images, CSS files, and JavaScript resources.

The system uses a Python-based website crawler and checker for deterministic scanning and **Ollama with Llama 3.2** for intelligent analysis and report generation.

---

## 🚀 Features

- 🌐 Website URL scanning
- 🕷️ Multi-page website crawling
- 🔗 Broken link detection
- 🖼️ Broken image detection
- 🎨 Broken CSS detection
- ⚙️ Broken JavaScript detection
- 📄 Failed webpage detection
- 📊 Website health score
- 🚨 Severity classification
- 🤖 Local AI analysis using Ollama
- 📋 Automated AI health report
- 📦 Raw JSON scan report
- 🖥️ Streamlit web interface
- ⬇️ Downloadable reports

---

## 🏗️ Architecture

```text
                    USER
                     │
                     ▼
            STREAMLIT WEB APP
                     │
                     ▼
                WEBSITE URL
                     │
                     ▼
             WEBSITE CRAWLER
                     │
                     ▼
               PAGE PARSER
                     │
                     ▼
             RESOURCE CHECKER
             ┌───────┼────────┐
             ▼       ▼        ▼
           Links   Images   CSS / JS
             │       │        │
             └───────┼────────┘
                     ▼
               RAW SCAN JSON
                     │
                     ▼
             RESULT SUMMARIZER
                     │
                     ▼
              SEVERITY ENGINE
                     │
                     ▼
                HEALTH SCORE
                     │
                     ▼
             OLLAMA LLAMA 3.2
                     │
                     ▼
             AI HEALTH REPORT
                     │
                     ▼
             STREAMLIT DASHBOARD
