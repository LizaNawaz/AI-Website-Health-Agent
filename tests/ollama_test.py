from app.ai.ollama_agent import OllamaAgent


agent = OllamaAgent()

results = {
    "website": "https://example.com",
    "broken_links": [
        {
            "url": "https://example.com/test",
            "status": 404
        }
    ],
    "broken_images": [
        {
            "url": "https://example.com/logo.png",
            "status": 404
        }
    ]
}

report = agent.analyze(results)

print(report)