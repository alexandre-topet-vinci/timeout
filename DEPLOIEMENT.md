# 🤖 IA Sarcastique - Déploiement Docker

Application complète avec détecteur de questions bêtes et réponses sarcastiques.

## 📦 Architecture

```
┌─────────────────┐
│   Frontend      │
│   Next.js       │  Port 3000
│   (React + UI)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Backend       │
│   NestJS        │  Port 3001
│   (API Gateway) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Python API    │
│   Flask +       │  Port 8000
│   DistilBERT    │
└─────────────────┘
```

## 🚀 Déploiement sur Mini PC

### Prérequis

- Docker & Docker Compose installés
- Au moins 4 GB RAM disponible
- 2 GB d'espace disque

### Installation

1. **Cloner le repository** (si pas déjà fait)
```bash
cd /chemin/vers/IA
```

2. **Vérifier que le modèle est entraîné**
```bash
ls -la modele_final/
# Doit contenir : config.json, pytorch_model.bin, etc.
```

3. **Construire et lancer les containers**
```bash
docker-compose up --build -d
```

4. **Vérifier que tout fonctionne**
```bash
docker-compose ps
# Tous les services doivent être "Up"

docker-compose logs -f
# Vérifier les logs en temps réel
```

### Accès à l'application

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:3001
- **Python API** : http://localhost:8000

### Commandes utiles

```bash
# Voir les logs
docker-compose logs -f [service]

# Redémarrer un service
docker-compose restart [service]

# Arrêter tout
docker-compose down

# Supprimer tout (y compris volumes)
docker-compose down -v

# Reconstruire un service
docker-compose up --build [service]

# Voir l'utilisation des ressources
docker stats
```

### Services individuels

```bash
# Python API uniquement
docker-compose up python-api

# Backend uniquement
docker-compose up backend

# Frontend uniquement
docker-compose up frontend
```

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` à la racine si besoin :

```env
# Python API
PORT=8000

# Backend
BACKEND_PORT=3001
PYTHON_API_URL=http://python-api:8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### Ports personnalisés

Modifier dans `docker-compose.yml` :

```yaml
services:
  frontend:
    ports:
      - "8080:3000"  # Accès via port 8080 au lieu de 3000
```

## 📊 Monitoring

### Health Checks

Tous les services ont des health checks automatiques :

```bash
# Vérifier la santé des services
docker inspect --format='{{.State.Health.Status}}' ia-python-api
docker inspect --format='{{.State.Health.Status}}' ia-backend
```

### Logs

```bash
# Logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f python-api

# Dernières 100 lignes
docker-compose logs --tail=100
```

## 🐛 Troubleshooting

### Le modèle ne se charge pas

```bash
# Vérifier que le dossier modele_final existe
ls -la modele_final/

# Si manquant, entraîner le modèle
python train_model.py
```

### Erreur de mémoire

Augmenter la mémoire Docker :
- Docker Desktop > Settings > Resources > Memory > 4GB minimum

### Port déjà utilisé

```bash
# Trouver le processus utilisant le port
lsof -i :3000

# Ou changer le port dans docker-compose.yml
```

### Container qui redémarre en boucle

```bash
# Voir les logs
docker-compose logs [service]

# Vérifier les health checks
docker inspect [container]
```

## 🔄 Mise à jour

### Après modification du modèle

```bash
# Reconstruire seulement le Python API
docker-compose up --build python-api
```

### Après modification du backend

```bash
docker-compose up --build backend
```

### Après modification du frontend

```bash
docker-compose up --build frontend
```

## 📈 Performance

### Ressources recommandées

- **CPU** : 2 cores minimum
- **RAM** : 4 GB minimum
- **Disque** : 2 GB pour images + modèle

### Optimisations

1. **Utiliser un volume pour le cache npm**
```yaml
volumes:
  - npm_cache:/root/.npm
```

2. **Limiter les ressources**
```yaml
services:
  python-api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## 🔐 Sécurité en production

1. **Changer les ports exposés**
2. **Utiliser un reverse proxy (nginx)**
3. **Activer HTTPS**
4. **Limiter les ressources**
5. **Mettre à jour régulièrement les images**

## 📝 Notes

- Le modèle est en **lecture seule** dans le container
- Les logs sont stockés dans Docker
- Les containers redémarrent automatiquement sauf si arrêtés manuellement
- Le réseau `ia-network` isole les containers

## 💡 Commandes rapides

```bash
# Démarrage rapide
docker-compose up -d

# Arrêt rapide
docker-compose down

# Rebuild complet
docker-compose down && docker-compose up --build -d

# Nettoyer tout
docker-compose down -v --rmi all
```

## 🎯 Accès rapide

Une fois déployé, ouvre ton navigateur sur : **http://localhost:3000**

Enjoy ! 🚀
