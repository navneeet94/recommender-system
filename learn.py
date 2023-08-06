from flask import Flask , jsonify , request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/sum/<string:a>')
def sum(a):
    return a


@app.route('/api/foo/', methods=['GET'])
def foo():
    bar = request.args.to_dict()
    return jsonify(bar)

if __name__ == "__main__":
    app.run(debug=True)