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

# Vérifier si le modèle existe déjà
if [ -d "./modele_final" ] && [ -f "./modele_final/config.json" ]; then
    echo "✅ Modèle entraîné trouvé dans ./modele_final/"
    echo ""
    read -p "Voulez-vous régénérer le modèle ? (o/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        echo "🗑️  Suppression de l'ancien modèle..."
        rm -rf ./modele_final
        echo "✅ Ancien modèle supprimé"
        echo ""
        echo "📦 Le modèle sera régénéré dans Docker"
    else
        echo "📦 Utilisation du modèle existant"
    fi
    echo ""
else
    echo "⚠️  Aucun modèle entraîné trouvé"
    echo ""
fi

# Information sur le processus
echo "📦 Le déploiement va :"
if [ -d "./modele_final" ]; then
    echo "   1. Utiliser le modèle existant (monté en volume)"
else
    echo "   1. Générer le dataset dans le container"
    echo "   2. Entraîner le modèle dans le container (~5-10 min)"
fi
echo "   3. Démarrer tous les services"
echo ""
if [ ! -d "./modele_final" ]; then
    echo "⏱️  Premier build avec entraînement : ~5-10 minutes"
else
    echo "⏱️  Build avec modèle existant : ~2 minutes"
fi
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

