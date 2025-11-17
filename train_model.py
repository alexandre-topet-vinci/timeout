#!/usr/bin/env python3
"""
Script d'entraînement d'un modèle pour détecter les questions bêtes
et y répondre de manière sarcastique.
"""

import json
import random
import os
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from datasets import Dataset
from sklearn.model_selection import train_test_split
import numpy as np
import shutil

# Configuration
MODEL_NAME = "distilbert-base-multilingual-cased"  # Modèle léger et multilingue
OUTPUT_DIR = "./modele_final"  # Dossier où sera sauvegardé le modèle final
TEMP_DIR = "./temp_training"   # Dossier temporaire pour l'entraînement
MAX_LENGTH = 128

def charger_donnees():
    """Charge les données d'entraînement depuis training_data.json"""
    print("📂 Chargement des données d'entraînement...")
    
    with open('training_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Préparer les données : 0 = normale, 1 = bête
    textes = []
    labels = []
    
    # Questions normales (label = 0)
    for question in data['questions_normales']:
        textes.append(question)
        labels.append(0)
    
    # Questions bêtes (label = 1)
    for question in data['questions_betes']:
        textes.append(question)
        labels.append(1)
    
    print(f"✅ {len(textes)} exemples chargés")
    print(f"   - {len(data['questions_normales'])} questions normales")
    print(f"   - {len(data['questions_betes'])} questions bêtes")
    
    return textes, labels

def preparer_dataset(textes, labels):
    """Prépare le dataset pour l'entraînement"""
    print("\n🔄 Préparation du dataset...")
    
    # Split train/test
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        textes, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Créer les datasets
    train_dataset = Dataset.from_dict({
        'text': train_texts,
        'label': train_labels
    })
    
    test_dataset = Dataset.from_dict({
        'text': test_texts,
        'label': test_labels
    })
    
    print(f"✅ Dataset préparé:")
    print(f"   - Entraînement: {len(train_dataset)} exemples")
    print(f"   - Test: {len(test_dataset)} exemples")
    
    return train_dataset, test_dataset

def tokenize_function(examples, tokenizer):
    """Tokenize les textes"""
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=MAX_LENGTH
    )

def compute_metrics(eval_pred):
    """Calcule les métriques d'évaluation"""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    accuracy = (predictions == labels).mean()
    return {'accuracy': accuracy}

def entrainer_modele():
    """Fonction principale d'entraînement"""
    print("🚀 Démarrage de l'entraînement du modèle IA sarcastique\n")
    
    # 1. Charger les données
    textes, labels = charger_donnees()
    
    # 2. Préparer le dataset
    train_dataset, test_dataset = preparer_dataset(textes, labels)
    
    # 3. Charger le tokenizer et le modèle
    print(f"\n📥 Chargement du modèle {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2  # 2 classes: normale (0) et bête (1)
    )
    print("✅ Modèle chargé")
    
    # 4. Tokenizer les datasets
    print("\n🔤 Tokenization des textes...")
    train_dataset = train_dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True
    )
    test_dataset = test_dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True
    )
    print("✅ Tokenization terminée")
    
    # 5. Nettoyer les anciens dossiers
    print("\n🧹 Nettoyage des anciens fichiers...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        print(f"   ✅ Dossier temporaire nettoyé")
    
    # 5. Configurer l'entraînement
    training_args = TrainingArguments(
        output_dir=TEMP_DIR,  # Sauvegarder dans un dossier temporaire
        num_train_epochs=5,  # 5 epochs suffisent pour un petit dataset
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=50,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        save_total_limit=1,  # Garder seulement le meilleur checkpoint
    )
    
    # 6. Créer le trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
    )
    
    # 7. Entraîner !
    print("\n🎓 Début de l'entraînement...\n")
    trainer.train()
    
    # 8. Évaluer
    print("\n📊 Évaluation du modèle...")
    results = trainer.evaluate()
    print(f"\n✅ Résultats finaux:")
    print(f"   - Précision: {results['eval_accuracy']*100:.2f}%")
    
    # 9. Sauvegarder le modèle final (remplacer l'ancien)
    print(f"\n💾 Sauvegarde du modèle final dans {OUTPUT_DIR}...")
    
    # Supprimer l'ancien modèle s'il existe
    if os.path.exists(OUTPUT_DIR):
        print(f"   🗑️  Suppression de l'ancien modèle...")
        shutil.rmtree(OUTPUT_DIR)
    
    # Sauvegarder le nouveau modèle
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print(f"   ✅ Modèle sauvegardé dans {OUTPUT_DIR}/")
    
    # 10. Nettoyer les fichiers temporaires
    print(f"\n🧹 Nettoyage des fichiers temporaires...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    if os.path.exists('./logs'):
        shutil.rmtree('./logs')
    print("   ✅ Nettoyage terminé")
    
    print("\n" + "="*70)
    print("🎉 ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS !")
    print("="*70)
    print(f"\n📂 Votre modèle est prêt dans : {OUTPUT_DIR}/")
    print(f"📊 Précision obtenue : {results['eval_accuracy']*100:.2f}%")
    print(f"\n💡 Pour l'utiliser : python generate_responses.py")
    print("="*70)

if __name__ == "__main__":
    entrainer_modele()
