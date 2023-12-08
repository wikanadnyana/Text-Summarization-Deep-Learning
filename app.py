from flask import Flask, request, jsonify
import pickle
from flask_cors import cross_origin
from bs4 import BeautifulSoup
import requests
import re
from transformers import pipeline

app = Flask(__name__)

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, framework="tf")

def processing(text):
    model_path = "../path"
    tokenizer_path = "../path/to/tokenizer"
    summary = summarizer(
        text,
        min_length=5,
        max_length=128,
    )
    return summary[0]["summary_text"]

@app.route("/api/fromnews", methods=["POST"])
@cross_origin() 
def fromnews():
    data = request.get_json()
    #validation to check wheter request is bbc news using regex
    pattern = re.compile(r'bbc\.com', re.IGNORECASE)
    match = re.search(pattern, data["full_link"])
    validating_bbc = bool(match)
    if not validating_bbc :
        return jsonify({"message" : "expected a bbc news"}), 400

    #Validation for the link to make sure link is exist
    respon = requests.get(data["full_link"])
    if respon.status_code != 200 :
        return jsonify({"message": "News not found"}), 404
    
    #using beautifulsoup to scrape news 


    #concating the block

    #returning the full text

    #processing the text
    
    return jsonify({"message": "News found and processed"})

@app.route("/api/fromtext", methods=["POST"])
@cross_origin()
def fromtext():
    #just process it, do we need to preprocess it?
    data = request.get_json()
    full_text = data["full_text"]
    return jsonify({"full_text": full_text, "summarize" : processing(full_text)})




if __name__ == '__main__':
    app.run(debug=True)
