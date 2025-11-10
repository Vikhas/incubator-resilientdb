from flask import Flask, request, jsonify
import subprocess
import requests
import json

app = Flask(__name__)

@app.route('/mcp', methods=['POST'])
def mcp_server():
    data = request.get_json()
    prompt = data.get('prompt')

    if prompt == 'Smart Contract':
        command = ['rescontract']
        command.extend(data.get('args', []))

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return jsonify({'output': result.stdout})
        except subprocess.CalledProcessError as e:
            return jsonify({'error': e.stderr}), 500

    elif prompt == 'GraphQL':
        graphql_query = data.get('query')
        graphql_variables = data.get('variables', {})

        try:
            response = requests.post(
                'http://localhost:8000/graphql',
                json={'query': graphql_query, 'variables': graphql_variables}
            )
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Invalid prompt specified'}), 400

if __name__ == '__main__':
    app.run(port=8080)
