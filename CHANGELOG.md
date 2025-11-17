# 📝 Changelog - Architecture Hybride

## �� Version 2.0 - Architecture Hybride (17 Nov 2025)

### 🆕 Nouvelles Fonctionnalités

#### Génération Dynamique de Réponses
- **Avant** : Réponses sarcastiques choisies aléatoirement dans une liste
- **Maintenant** : Réponses **générées dynamiquement** par Llama3.2
- **Avantage** : Chaque réponse est unique avec insultes variées

#### Réponses Directes aux Questions Normales
- **Avant** : "Bonne question ! Je te laisse chercher..."
- **Maintenant** : IA répond **directement** à la question
- **Avantage** : Vraie valeur ajoutée pour les bonnes questions

#### Insultes Variées et Créatives
- **Avant** : Même pool de ~20 réponses sarcastiques
- **Maintenant** : Génération infinie avec vocabulaire complet
- **Exemples** : con, débile, abruti, crétin, connard, couillon, branque, etc.

### 🏗️ Architecture Technique

```
Ancienne Architecture (v1.0) :
Question → DistilBERT → Si bête ? Choisir réponse aléatoire : "Question normale"

Nouvelle Architecture (v2.0) :
Question → DistilBERT → Si bête ? Ollama génère sarcasme : Ollama répond directement
```

### 📦 Nouveaux Services

1. **Ollama** (Port 11434)
   - Container Docker avec Llama3.2 (2GB)
   - Génération de texte en temps réel
   - Température ajustable pour créativité

2. **API Hybride**
   - DistilBERT pour classification (rapide, <100ms)
   - Ollama pour génération (1-2 secondes)
   - Fallback en cas d'erreur Ollama

### 📄 Nouveaux Fichiers

- `init_ollama.sh` - Script d'initialisation Ollama
- `ARCHITECTURE_HYBRIDE.md` - Documentation détaillée
- `START_HERE.md` - Guide de démarrage rapide
- `CHANGELOG.md` - Ce fichier

### 🔧 Fichiers Modifiés

- `api_server.py`
  - Ajout fonction `generer_reponse_ollama()`
  - Suppression dépendance à `training_data.json` pour réponses
  - Ajout prompts SARCASTIQUE et NORMAL
  - Gestion erreurs Ollama avec fallback

- `docker-compose.yml`
  - Ajout service `ollama`
  - Ajout volume `ollama_data`
  - Dépendance `python-api` sur `ollama`
  - Healthcheck Ollama

- `setup.sh`
  - Ajout vérification port 11434
  - Appel automatique à `init_ollama.sh`
  - Message d'info sur téléchargement Llama3.2

- `requirements.txt`
  - Ajout `requests>=2.31.0`

- `.env.example`
  - Ajout `OLLAMA_URL=http://ollama:11434`

- `.gitignore`
  - Ajout `ollama_data/`

- `README.md`
  - Mise à jour architecture
  - Explications modèles hybrides
  - Instructions personnalisation

### 🗑️ Fichiers Supprimés

- `api_server_fewshot.py` - Non utilisé
- `api_server_generative.py` - Non utilisé
- `train_model_generative.py` - Non utilisé
- `demo.py` - Obsolète
- `demo_apprentissage.py` - Obsolète
- `generer_dataset.py` - Remplacé par `generer_dataset_avance.py`
- `generate_responses.py` - Fonctionnalité intégrée à l'API
- `README_GENERATIF.md` - Redondant
- `EXPLICATIONS_SYSTEME.md` - Remplacé par `ARCHITECTURE_HYBRIDE.md`
- `temp_training/` - Dossier temporaire nettoyé

### ⚡ Améliorations de Performance

- **Classification** : Toujours <100ms (DistilBERT inchangé)
- **Génération** : 1-2 secondes (Ollama avec Llama3.2)
- **RAM totale** : ~3-4 GB (DistilBERT 1GB + Ollama 2-3GB)
- **Disque** : ~2.5 GB (modèle DistilBERT 516MB + Llama3.2 2GB)

### 🔒 Sécurité et Vie Privée

- ✅ **100% local** - Aucune donnée envoyée à l'extérieur
- ✅ **Pas de clé API** - Pas besoin de compte OpenAI/Anthropic
- ✅ **Gratuit** - Aucun coût d'utilisation
- ✅ **Hors ligne** - Fonctionne sans connexion internet (après téléchargement initial)

### 🎯 Cas d'Usage

#### Questions Bêtes (Classification DistilBERT + Génération Ollama)
```
Question : "C'est quoi une variable ?"
→ DistilBERT : Bête à 95%
→ Ollama : "Putain mec, t'es en 3ème année et tu sais pas ça ? 
            Va réviser tes bases avant de me faire perdre mon temps, abruti."
```

#### Questions Normales (Classification DistilBERT + Génération Ollama)
```
Question : "Comment implémenter un algorithme de consensus distribué ?"
→ DistilBERT : Normale à 92%
→ Ollama : "Un algorithme de consensus distribué comme Raft ou Paxos 
            nécessite une gestion d'états, des élections de leader et 
            des mécanismes de réplication. Je te conseille de commencer 
            par étudier Raft qui est plus accessible."
```

### 📊 Métriques

- **Précision DistilBERT** : 98.92% (inchangée)
- **Variété des réponses** : ∞ (vs 73 réponses fixes avant)
- **Pertinence** : Améliorée (contexte de la question utilisé)
- **Temps de réponse** : +1-2s (acceptable pour génération)

### 🔄 Migration

Pour migrer depuis v1.0 :

```bash
git pull
docker-compose down
./setup.sh
```

Le script gérera automatiquement :
- Téléchargement de Llama3.2
- Mise à jour des containers
- Configuration Ollama

### 🐛 Corrections de Bugs

- Suppression import `json` inutilisé dans `api_server.py`
- Suppression dépendance à `training_data.json` pour réponses (toujours utilisé pour entraînement)
- Nettoyage fichiers obsolètes

### 📝 TODO Futures Versions

- [ ] Ajouter cache des réponses fréquentes
- [ ] Support multi-langues pour génération
- [ ] Interface admin pour ajuster température
- [ ] Métriques d'utilisation (compteur questions bêtes vs normales)
- [ ] API pour ajouter questions au dataset
- [ ] Fine-tuning Llama3.2 sur style personnel

---

## Version 1.0 - Version Initiale

- Classification DistilBERT (98.92%)
- 464 questions d'entraînement
- 73 réponses sarcastiques fixes
- Docker avec 3 services
- Frontend Next.js + Backend NestJS
