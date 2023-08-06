from flask import Flask,jsonify
import pandas as pd;

movie_df = pd.read_csv('./data/movie_id.csv')

app = Flask(__name__)

def extractKeyVal(value):
    a,id,name= value
    return {"id":str(id),"name":name}

def movieList():
    movie_list = []
    for i in range(len(movie_df)):
        movie_list.append(extractKeyVal(movie_df.iloc[i]))
    return jsonify(movie_list)

@app.route("/movie-ids")
def home():
    return movieList()


if __name__ == "__main__":
    app.run(debug=True)