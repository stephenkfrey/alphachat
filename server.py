# server.py
from flask import Flask, request, jsonify
from chroma_utils import add_query_LOCAL

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    prompt = request.json['prompt']
    collection_name = request.json['collection_name']
    num_results = request.json['num_results']
    result = add_query_LOCAL.query_db(prompt, collection_name, num_results)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)