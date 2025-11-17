#!/bin/bash

echo "🚀 Setup IA Sarcastique pour déploiement"
echo "========================================"
echo ""

# Créer le fichier .env depuis .env.example
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "✅ Fichier .env créé"
else
    echo "✅ Fichier .env existe déjà"
fi
echo ""

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé !"
    echo "� Veuillez exécuter d'abord : ./install_dependencies.sh"
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé !"
    echo "📥 Veuillez exécuter d'abord : ./install_dependencies.sh"
    exit 1
fi

echo "✅ Docker et Docker Compose sont installés"
echo ""

# Information sur le processus
echo "📦 Le modèle sera automatiquement :"
echo "   1. Dataset généré dans le container"
echo "   2. Modèle entraîné dans le container"
echo "   3. Services démarrés"
echo ""
echo "⏱️  Premier build : ~5-10 minutes"
echo "⏱️  Builds suivants : ~2 minutes (cache Docker)"
echo ""

read -p "Voulez-vous continuer ? (O/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "❌ Installation annulée"
    exit 0
fi

echo ""
echo "🐳 Construction et démarrage des containers Docker..."
echo "========================================"
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Déploiement terminé !"
    echo ""
    echo "📍 Services disponibles :"
    echo "   - Frontend:    http://localhost:1418"
    echo "   - Backend:     http://localhost:3001"
    echo "   - Python API:  http://localhost:8000"
    echo ""
    echo "📊 Vérifier les logs : docker-compose logs -f"
    echo "🛑 Arrêter :           docker-compose down"
    echo ""
else
    echo ""
    echo "❌ Erreur lors du démarrage des containers"
    echo "📊 Voir les logs : docker-compose logs"
    exit 1
fi

