#!/usr/bin/env python3
"""
Script de démonstration rapide sans mode interactif
"""

import json
import random
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configuration
MODEL_DIR = "./modele_final"  # Chemin vers le modèle entraîné
SEUIL_BETISE = 0.5  # Seuil ajusté à 50%

print("🤖 Chargement de l'IA sarcastique...")

# Charger le modèle et le tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

# Charger les réponses sarcastiques
with open('training_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    reponses_sarcastiques = data['reponses_sarcastiques']

print("✅ IA prête !\n")
print("=" * 70)
print("🧪 TEST DE L'IA SARCASTIQUE")
print("=" * 70)
print()

# Questions de test
questions_test = [
    "Est-ce que l'eau est mouillée ?",
    "Comment implémenter un algorithme de tri efficace ?",
    "1 + 1 ça fait combien ?",
    "Explique-moi le fonctionnement de Kubernetes",
    "Pourquoi on appelle ça un gratte-ciel ?",
    "Quelle est la différence entre REST et GraphQL ?",
    "C'est quoi la capitale de la France ?",
    "Comment optimiser les performances d'une base de données ?",
]

for question in questions_test:
    # Tokenizer
    inputs = tokenizer(
        question,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )
    
    # Prédiction
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        prob_bete = probabilities[0][1].item()
        est_bete = prob_bete > SEUIL_BETISE
    
    print(f"💬 Question: {question}")
    
    if est_bete:
        reponse = random.choice(reponses_sarcastiques)
        print(f"🤦 IA: {reponse}")
        print(f"   📊 Niveau de bêtise: {prob_bete*100:.1f}%")
    else:
        print(f"😊 IA: C'est une bonne question ! Laisse-moi t'aider avec ça.")
        print(f"   📊 Question légitime: {(1-prob_bete)*100:.1f}%")
    
    print("-" * 70)
    print()

print("🎉 Démonstration terminée !")
print("\n💡 Pour utiliser en mode interactif: python generate_responses.py")
