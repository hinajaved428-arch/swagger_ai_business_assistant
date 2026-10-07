# Swagger AI Business Assistant

This version does NOT require Ollama or an API key.

It provides:
- Browser web page for business questions
- Swagger UI at `/apidocs/`
- Flask REST API
- TF-IDF + cosine similarity retrieval (local ML)
- Local JSON business knowledge base
- Grounded answers; if no relevant knowledge is found, it says information is missing.

## VS Code extensions
Recommended:
1. Python — Microsoft
2. Pylance — Microsoft
3. Swagger Viewer/Swagger Editor — optional

## Run
Open this folder in VS Code PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If activation is blocked:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open:
- http://127.0.0.1:5000
- http://127.0.0.1:5000/apidocs/

## Swagger test
Expand `POST /api/business-question`, click **Try it out**, then use:
```json
{"question":"How should I troubleshoot a network issue?","top_k":3}
```
Click Execute to see the output.

Edit `app/data/business_knowledge.json` to add your approved business information.

Accuracy note: no AI/ML system can guarantee 100% accuracy for arbitrary questions. This project is grounded in the local knowledge base and avoids inventing company-specific facts.
