from flask import Flask,jsonify
from flask_cors import CORS
import pandas as pd;
import pickle as pkl;

data = pkl.load(open('./data/movie_list.pkl','rb'))
app = Flask(__name__)
CORS(app)

@app.route("/api/movie-ids")
def home():
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)