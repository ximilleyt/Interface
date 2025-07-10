from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/date', methods=['GET'])
def get_date():
    now = datetime.now().date().isoformat()
    return jsonify({
        "date": now
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
