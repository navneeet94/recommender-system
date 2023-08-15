import pickle
import json


# Load the pickle file
with open('./data/movie_list.pkl', 'rb') as f:
    data = pickle.load(f)

json_data = json.dumps(data)

print(json_data)