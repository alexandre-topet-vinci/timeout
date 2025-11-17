#!/usr/bin/env python3
"""
API Server pour le modèle IA sarcastique hybride
Utilise DistilBERT pour classification + Ollama pour génération
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import requests
import os

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis Next.js

# Configuration
MODEL_DIR = "./modele_final"
SEUIL_BETISE = 0.5
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://ollama:11434')

# Vérifier que le modèle existe
if not os.path.exists(MODEL_DIR) or not os.path.exists(os.path.join(MODEL_DIR, "config.json")):
    print("❌ ERREUR : Le modèle n'existe pas dans ./modele_final/")
    print("💡 Le modèle doit être entraîné lors du build Docker")
    print("🔍 Contenu du dossier actuel :")
    os.system("ls -la")
    print("🔍 Contenu du dossier modele_final (si existe) :")
    os.system("ls -la modele_final/ 2>/dev/null || echo 'Dossier modele_final inexistant'")
    exit(1)

# Charger le modèle DistilBERT
print("🚀 Chargement du modèle DistilBERT...")
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_DIR)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()
print("✅ Modèle DistilBERT chargé !")

# Prompts pour Ollama
PROMPT_SARCASTIQUE = """Tu es un assistant sarcastique et vulgaire qui répond aux questions stupides d'étudiants en 3ème année d'informatique. 

Ton rôle :
- Répondre de manière TRÈS sarcastique et condescendante
- Utiliser des INSULTES variées (con, débile, idiot, abruti, crétin, etc.)
- Être méchant mais drôle
- Faire comprendre que la question est vraiment nulle
- Varier tes réponses, ne pas répéter les mêmes insultes

Exemples de ton style :
- "Putain mec, t'es en 3ème année et tu sais pas ça ? Va réviser tes bases avant de me faire perdre mon temps, abruti."
- "Sérieux ? Cette question de débile ? Google existe, connard. Même un stagiaire de première année saurait ça."
- "Oh bordel, je crois que j'ai perdu des neurones en lisant ça. T'es sûr que t'es pas en maternelle ? Crétin va."

Question stupide : {question}

Réponds de manière sarcastique avec des insultes (1-2 phrases maximum) :"""

PROMPT_NORMAL = """Tu es un assistant technique qui répond de manière claire et directe aux questions de développement.

Ton rôle :
- Répondre DIRECTEMENT à la question posée
- Être concis (2-3 phrases maximum)
- Donner des informations techniques précises
- Être professionnel mais pas condescendant

Question : {question}

Réponds de manière claire et technique :"""

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

def generer_reponse_ollama(question: str, est_bete: bool):
    """Génère une réponse avec Ollama"""
    try:
        prompt = PROMPT_SARCASTIQUE.format(question=question) if est_bete else PROMPT_NORMAL.format(question=question)
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.9 if est_bete else 0.3,
                    "max_tokens": 150
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        else:
            print(f"❌ Erreur Ollama: {response.status_code} - {response.text}")
            return "Erreur lors de la génération de la réponse." if not est_bete else "Trop con pour répondre à cette question de merde."
            
    except requests.exceptions.Timeout:
        print("⏱️ Timeout Ollama")
        return "Timeout lors de la génération." if not est_bete else "Même mon IA en a marre de tes questions débiles."
    except Exception as e:
        print(f"❌ Erreur génération: {str(e)}")
        return "Erreur lors de la génération." if not est_bete else "Va te faire foutre, j'ai même pas envie de répondre."


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
        
        # 1. Classifier la question avec DistilBERT
        classification = classifier_question(question)
        
        # 2. Générer la réponse avec Ollama
        reponse = generer_reponse_ollama(question, classification['est_bete'])
        type_reponse = "sarcastique" if classification['est_bete'] else "normale"
        
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
        "model_classification": "distilbert-base-multilingual-cased",
        "model_generation": "llama3.2",
        "threshold": SEUIL_BETISE,
        "status": "operational"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Serveur démarré sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
