from flask import Flask, request, jsonify
import pickle
from flask_cors import cross_origin
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

@app.route("/api/textscrape", methods=["POST"])
@cross_origin()
def textscrape():
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
    
    return jsonify({"message": "News found and processed"})

if __name__ == '__main__':
    app.run(debug=True)
