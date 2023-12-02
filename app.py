from flask import Flask, request, jsonify
import pickle
from flask_cors import cross_origin
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/api/textscrape", methods=["POST"])
@cross_origin()
def textscrape():
    #Validation for the link to make sure link is exist
    data = request.get_json()
    respon = requests.get(data["full_link"])
    if respon.status_code != 200 :
        return jsonify({"message": "News not found"}), 404
    
    return jsonify({"message": "News found and processed"})

if __name__ == '__main__':
    app.run(debug=True)
