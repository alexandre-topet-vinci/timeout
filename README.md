# 🤖 IA Sarcastique - Entraînement d'un Modèle Personnalisé

Ce projet entraîne un modèle d'IA léger à détecter les questions "bêtes" et y répondre de manière sarcastique.

## 📋 Structure du Projet

- `train_model.py` - Script d'entraînement du modèle
- `generate_responses.py` - Utiliser le modèle entraîné pour générer des réponses
- `training_data.json` - Dataset d'entraînement (questions bêtes vs normales)
- `requirements.txt` - Dépendances Python

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 📚 Utilisation

### 1. Entraîner le modèle
```bash
python train_model.py
```

### 2. Tester le modèle
```bash
python generate_responses.py
```

## 🎯 Comment ça marche

1. Le modèle est entraîné à classifier si une question est "bête" ou "normale"
2. Si la question est classée comme "bête", l'IA répond sarcastiquement
3. Sinon, elle répond normalement

## ⚙️ Personnalisation

Modifiez `training_data.json` pour ajouter vos propres exemples !
# timeout
