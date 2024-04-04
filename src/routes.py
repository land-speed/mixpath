from flask import Flask, request, jsonify
import sys
from graph import Graph
from file_parsing import to_node
from utils import random_songs

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/create-graph-demo")
def create_demo_graph():
    nodes = random_songs(100)
    g = Graph()
    nodes = g.add_nodes(nodes)
    g.recalculate_edges(int(request.args.get("bpm_tolerance", 1)), int(request.args.get("key_tolerance", 1)))
    return g.to_json()

@app.route("/create-graph/<path:folderpath>")
def create_graph(folderpath):
    if folderpath is None:
        return jsonify({'error': 'Missing directory'}), 400
    else:
        nodes = to_node("/"+folderpath)
        g = Graph()
        nodes = g.add_nodes(nodes)
        g.recalculate_edges(int(request.args.get("bpm_tolerance", 1)), int(request.args.get("key_tolerance", 1)))
        return g.to_json()

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)