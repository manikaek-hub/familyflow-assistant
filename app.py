from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/claude', methods=['POST'])
def claude_api():
    try:
        # Récupérer la clé API depuis les variables d'environnement
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        if not api_key:
            return jsonify({'error': 'API key not configured on server'}), 500
        
        data = request.json
        messages = data.get('messages')
        
        if not messages:
            return jsonify({'error': 'Missing messages'}), 400
        
        # Appel à l'API Anthropic
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 1500,
                'messages': messages
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': f'API Error: {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
