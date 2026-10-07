from flask import Flask, request, jsonify, render_template
from flasgger import Swagger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from pathlib import Path

app=Flask(__name__,template_folder="app/templates",static_folder="app/static")
Swagger(app,template_file="app/swagger.yml")
knowledge=json.loads(Path("app/data/business_knowledge.json").read_text(encoding="utf-8"))
docs=[f"{x['title']} {x['content']} {' '.join(x.get('keywords',[]))}" for x in knowledge]
vectorizer=TfidfVectorizer(lowercase=True,stop_words="english")
matrix=vectorizer.fit_transform(docs)

def answer(q,k=3):
    scores=cosine_similarity(vectorizer.transform([q]),matrix)[0]
    ranked=sorted(enumerate(scores),key=lambda x:x[1],reverse=True)[:k]
    matches=[{"title":knowledge[i]["title"],"content":knowledge[i]["content"],"score":round(float(s),4)}
             for i,s in ranked if s>0]
    if not matches:
        return {"answer":"I could not find enough information in the current business knowledge base to answer this question accurately.","confidence":0.0,"sources":[]}
    return {"answer":"Based on the available business information: "+matches[0]["content"],
            "confidence":round(min(1.0,matches[0]["score"]*1.8),2),"sources":matches}

@app.route("/")
def home(): return render_template("index.html")

@app.post("/api/business-question")
def question():
    data=request.get_json(silent=True) or {}
    q=str(data.get("question","")).strip()
    if not q: return jsonify(success=False,error="Question is required."),400
    try: k=max(1,min(int(data.get("top_k",3)),5))
    except: k=3
    return jsonify(success=True,question=q,**answer(q,k))

@app.get("/api/knowledge")
def get_knowledge(): return jsonify(count=len(knowledge),records=knowledge)

if __name__=="__main__": app.run(host="127.0.0.1",port=5000,debug=True)
