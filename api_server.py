#!/usr/bin/env python3
"""
API Server pour le modèle IA sarcastique
Serveur Flask simple pour exposer le modèle via API REST
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import json
import random
import os

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis Next.js

# Configuration
MODEL_DIR = "./modele_final"
SEUIL_BETISE = 0.5

# Charger les réponses sarcastiques
with open('training_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    REPONSES_SARCASTIQUES = data['reponses_sarcastiques']

# Charger le modèle
print("🚀 Chargement du modèle...")
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_DIR)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()
print("✅ Modèle chargé !")

def classifier_question(question: str):
    """Classifie une question comme bête ou normale"""
    inputs = tokenizer(
        question,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )
    
    with torch.no_grad():
        outputs = model(**inputs)
        probas = torch.softmax(outputs.logits, dim=1)
        
    proba_normale = probas[0][0].item()
    proba_bete = probas[0][1].item()
    
    return {
        "est_bete": proba_bete > SEUIL_BETISE,
        "confiance_normale": proba_normale,
        "confiance_bete": proba_bete
    }

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé"""
    return jsonify({"status": "ok", "model": "loaded"})

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Endpoint principal pour poser une question"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({"error": "Question vide"}), 400
        
        # Classifier la question
        classification = classifier_question(question)
        
        # Générer la réponse
        if classification['est_bete']:
            reponse = random.choice(REPONSES_SARCASTIQUES)
            type_reponse = "sarcastique"
        else:
            reponse = "Bonne question ! Je te laisse chercher la réponse par toi-même, c'est une vraie question qui mérite réflexion. 🤔"
            type_reponse = "normale"
        
        return jsonify({
            "question": question,
            "reponse": reponse,
            "type": type_reponse,
            "est_bete": classification['est_bete'],
            "confiance_normale": round(classification['confiance_normale'], 3),
            "confiance_bete": round(classification['confiance_bete'], 3)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Statistiques sur le modèle"""
    return jsonify({
        "model_name": "distilbert-base-multilingual-cased",
        "total_responses": len(REPONSES_SARCASTIQUES),
        "threshold": SEUIL_BETISE,
        "status": "operational"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Serveur démarré sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
