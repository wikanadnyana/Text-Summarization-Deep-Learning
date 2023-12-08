from flask import Flask, request, jsonify
import pickle
from flask_cors import cross_origin
from bs4 import BeautifulSoup
import requests
import re
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

def summarize_text(model, tokenizer, text):
    # Tokenize and generate summary
    input_ids = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    output = model.generate(input_ids, max_length=150, num_beams=2, length_penalty=2.0, early_stopping=True)
    generated_summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_summary

def processing(text):
    model = T5ForConditionalGeneration.from_pretrained("./model")
    tokenizer = T5Tokenizer.from_pretrained("./model")
    full_text = [text]
    for idx, news_text in enumerate(full_text, start=1):
        generated_summary = summarize_text(model, tokenizer, news_text)
    
    return generated_summary

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
