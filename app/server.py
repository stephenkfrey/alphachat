from flask import Flask, request, jsonify
import src.scripts.db_query_data as db_query_data

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    prompt = request.json['prompt']
    collection_name = request.json['collection_name']
    num_results = request.json['num_results']
    result = db_query_data.query_db(prompt, collection_name, num_results)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)