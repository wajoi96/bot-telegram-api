from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# === Setup Firebase Admin SDK ===
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# === API ENDPOINT ===
@app.route('/update-signal', methods=['POST'])
def update_signal():
    data = request.json
    pair = data.get('pair')
    sentiment = data.get('sentiment')

    if not pair or not sentiment:
        return jsonify({
            'status': 'failed',
            'reason': 'Missing pair or sentiment'
        }), 400

    doc_id = pair.replace("/", "").replace("-", "").replace(" ", "")
    doc_ref = db.collection('signals').document(doc_id)

    doc_ref.set({
        'pair': pair,
        'sentiment': sentiment
    })

    return jsonify({
        'status': 'success',
        'pair': pair,
        'sentiment': sentiment
    })

# === Run app ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
