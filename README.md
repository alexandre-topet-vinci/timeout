# 🤖 IA Sarcastique - Détection de Questions Bêtes

Ce projet utilise une architecture **hybride** pour détecter les questions "bêtes" de développement et générer des réponses sarcastiques avec insultes, ou répondre normalement aux vraies questions.

## 🧠 Architecture Hybride

### 1. **DistilBERT** (Classification)
- Modèle entraîné localement sur 464 questions
- Détecte si une question est "bête" ou "normale"
- Précision : 98.92%

### 2. **Ollama + Llama3.2** (Génération)
- Si question bête → Génère réponse sarcastique **avec insultes variées**
- Si question normale → Répond **directement à la question**
- LLM local, gratuit, léger (2GB)

## 📋 Structure du Projet

### Scripts Python
- `generer_dataset_avance.py` - Génère un dataset de 464 questions (dev + culture générale)
- `train_model.py` - Entraîne le modèle DistilBERT (98.92% de précision)
- `api_server.py` - API Flask avec DistilBERT + Ollama

### Application Web
- `backend/` - API NestJS (port 3002)
- `frontend/` - Interface Next.js (port 1418)

### Configuration
- `docker-compose.yml` - Orchestration des 4 services (Ollama, Python API, Backend, Frontend)
- `Dockerfile.python` - Container Python avec entraînement automatique
- `setup.sh` - Script de déploiement intelligent
- `init_ollama.sh` - Initialisation d'Ollama avec Llama3.2

## 🚀 Déploiement Rapide

```bash
./setup.sh
```

Le script va automatiquement :
- Vérifier Docker et Docker Compose
- Créer le fichier .env
- Démarrer Ollama
- Télécharger Llama3.2 (2GB, première fois seulement)
- Générer le dataset et entraîner le modèle
- Démarrer tous les services

**Première fois** : ~10-15 minutes (téléchargement Llama3.2 + entraînement)  
**Déploiements suivants** : ~2 minutes

Accédez ensuite à : **http://localhost:1418**

## 📚 Documentation Complète

- `DEPLOIEMENT.md` - Guide de déploiement détaillé
- `COMMENT_DEPLOYER.md` - Instructions pour mini PC
- `EXPLICATION_ENTRAINEMENT.md` - Explications sur l'entraînement du modèle

## 🎯 Architecture

```
Frontend (Next.js:1418) → Backend (NestJS:3002) → Python API (Flask:8001)
                                                          ↓
                                                   DistilBERT (Classification)
                                                          ↓
                                                   Ollama:11434 (Génération)
                                                          ↓
                                                   Llama3.2 (2GB)
```

## ⚙️ Personnalisation

- **Dataset** : Modifiez `generer_dataset_avance.py` pour ajouter vos questions
- **Prompts** : Modifiez `api_server.py` pour changer le style des réponses (insultes, sarcasme, etc.)
- **Modèle LLM** : Changez `llama3.2` par `mistral` ou autre dans `init_ollama.sh` et `api_server.py`
