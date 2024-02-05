from flask import Flask, request, jsonify
from flask_cors import cross_origin
from bs4 import BeautifulSoup
import requests
import re
import time


app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/ayuliasw/summarization-t5"
headers = {"Authorization": "YOUR_AUTH_BEARER"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def is_model_ready():
    response = requests.get(API_URL)
    return response.status_code == 200


@app.route("/api/fromnews", methods=["POST"])
@cross_origin() 
def fromnews():
    data = request.get_json()
    #validation to check wheter request is bbc news using regex
    pattern = re.compile(r'bbc\.com/news', re.IGNORECASE)
    match = re.search(pattern, data["full_link"])
    validating_bbc = bool(match)
    if not validating_bbc :
        return jsonify({"message" : "expected a bbc news"}), 400

    #Validation for the link to make sure link is exist
    respon = requests.get(data["full_link"])
    if respon.status_code != 200 :
        return jsonify({"message": "News not found"}), 404
    
    #using beautifulsoup to scrape news
    url = data["full_link"]
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    div_elements = soup.find_all('div', {'class': 'ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0'})

    text_data = ' '.join(div.find('p').get_text(strip=True) if div.find('p') else '' for div in div_elements)
    preprocessed_text = re.sub(r"['\"]", '', text_data)

    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', preprocessed_text)
    truncated_text = ''

    for sentence in sentences:
        if len(truncated_text) + len(sentence) <= 512:
            truncated_text += sentence
        else:
            break
    
    while not is_model_ready():
        print("Model is still initializing. Waiting for 2 seconds...")
        time.sleep(2)
    
    output = query({
	"inputs": truncated_text,
    })
    return jsonify({"full text": truncated_text, "summarize" : output[0]["summary_text"]})


@app.route("/api/fromtext", methods=["POST"])
@cross_origin()
def fromtext():
    #just process it, do we need to preprocess it?
    data = request.get_json()
    full_text = data["full_text"]
    truncated_text = ' '.join(full_text.split()[:512])
    while not is_model_ready():
        print("Model is still initializing. Waiting for 2 seconds...")
        time.sleep(2)
    output = query({
	"inputs": truncated_text,
    })
    return jsonify({"full_text": full_text, "summarize" : output[0]["summary_text"]})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
