from blockchain import *
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the Blockchain Voting API!",
        "endpoints": {
            "/vote": "Add a vote",
            "/mine": "Mine a new block",
            "/chain": "View the blockchain",
            "/nodes/register": "Register a new node",
            "/nodes/resolve": "Resolve conflicts in the chain"
        }
    }), 200

@app.route('/vote', methods=['POST'])
def new_vote():
    values = request.get_json()
    required = ['voter_id', 'candidate']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_vote(values['voter_id'], values['candidate'])
    return jsonify({'message': f'Vote will be added to Block {index}'}), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': 'New block forged',
        'index': block['index'],
        'votes': block['votes'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {'message': 'New nodes have been added', 'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {'message': 'Our chain was replaced', 'new_chain': blockchain.chain}
    else:
        response = {'message': 'Our chain is authoritative', 'chain': blockchain.chain}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)