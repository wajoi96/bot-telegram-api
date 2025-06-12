from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import firestore

app = Flask(__name__)

# === Setup Firebase Admin SDK ===
firebase_admin.initialize_app()

db = firestore.client()

# === API ENDPOINT ===
@app.route('/update-signal', methods=['POST'])
def update_signal():
    data = request.json
    pair = data.get('pair')
    sentiment = data.get('sentiment') or data.get('sentimen')  # support dua2 field

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
