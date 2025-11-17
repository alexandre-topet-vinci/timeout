#!/usr/bin/env python3
"""
Script pour utiliser le modèle entraîné et générer des réponses sarcastiques
aux questions bêtes.
"""

import json
import random
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configuration
MODEL_DIR = "./modele_final"  # Chemin vers le modèle entraîné
SEUIL_BETISE = 0.5  # Seuil de confiance pour classifier comme "bête" (50%)

class IASercastique:
    """Classe pour gérer l'IA sarcastique"""
    
    def __init__(self):
        print("🤖 Chargement de l'IA sarcastique...")
        
        # Charger le modèle et le tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        self.model.eval()
        
        # Charger les réponses sarcastiques
        with open('training_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.reponses_sarcastiques = data['reponses_sarcastiques']
        
        print("✅ IA prête à l'emploi !\n")
    
    def classifier_question(self, question):
        """
        Classifie une question comme normale ou bête
        Retourne: (est_bete: bool, confiance: float)
        """
        # Tokenizer
        inputs = self.tokenizer(
            question,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )
        
        # Prédiction
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            
            # probabilities[0][0] = prob normale
            # probabilities[0][1] = prob bête
            prob_bete = probabilities[0][1].item()
            est_bete = prob_bete > SEUIL_BETISE
            
            return est_bete, prob_bete
    
    def generer_reponse(self, question):
        """
        Génère une réponse appropriée à la question
        """
        est_bete, confiance = self.classifier_question(question)
        
        if est_bete:
            # Choisir une réponse sarcastique aléatoire
            reponse = random.choice(self.reponses_sarcastiques)
            return {
                'type': 'sarcastique',
                'reponse': reponse,
                'confiance': confiance
            }
        else:
            return {
                'type': 'normale',
                'reponse': "C'est une bonne question ! Laisse-moi t'aider avec ça.",
                'confiance': 1 - confiance
            }

def mode_interactif():
    """Mode interactif pour tester l'IA"""
    print("=" * 60)
    print("🤖 IA SARCASTIQUE - Mode Interactif")
    print("=" * 60)
    print("\nPose tes questions ! (tape 'quit' pour quitter)\n")
    
    ia = IASercastique()
    
    while True:
        try:
            question = input("💬 Toi: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Au revoir !")
                break
            
            if not question:
                continue
            
            # Générer la réponse
            resultat = ia.generer_reponse(question)
            
            # Afficher la réponse
            if resultat['type'] == 'sarcastique':
                print(f"🤦 IA: {resultat['reponse']}")
                print(f"   (Niveau de bêtise détecté: {resultat['confiance']*100:.1f}%)")
            else:
                print(f"😊 IA: {resultat['reponse']}")
                print(f"   (Question légitime - confiance: {resultat['confiance']*100:.1f}%)")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            break

def mode_test():
    """Mode test avec des exemples prédéfinis"""
    print("=" * 60)
    print("🧪 IA SARCASTIQUE - Mode Test")
    print("=" * 60)
    print()
    
    ia = IASercastique()
    
    # Questions de test
    questions_test = [
        "Est-ce que l'eau est mouillée ?",
        "Comment implémenter un algorithme de tri efficace ?",
        "1 + 1 ça fait combien ?",
        "Explique-moi le fonctionnement de Kubernetes",
        "Pourquoi on appelle ça un gratte-ciel ?",
        "Quelle est la différence entre REST et GraphQL ?",
    ]
    
    for question in questions_test:
        print(f"💬 Question: {question}")
        resultat = ia.generer_reponse(question)
        
        if resultat['type'] == 'sarcastique':
            print(f"🤦 Réponse: {resultat['reponse']}")
            print(f"   📊 Bêtise: {resultat['confiance']*100:.1f}%")
        else:
            print(f"😊 Réponse: {resultat['reponse']}")
            print(f"   📊 Légitimité: {resultat['confiance']*100:.1f}%")
        
        print("-" * 60)
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        mode_test()
    else:
        mode_interactif()
