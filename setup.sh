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

# Vérifier et arrêter les anciens containers
if docker ps -a | grep -E "ia-python-api|ia-backend|ia-frontend" > /dev/null; then
    echo "🛑 Anciens containers détectés, nettoyage..."
    docker-compose down 2>/dev/null
    
    # Forcer l'arrêt si nécessaire
    docker stop ia-python-api ia-backend ia-frontend 2>/dev/null
    docker rm ia-python-api ia-backend ia-frontend 2>/dev/null
    
    echo "✅ Containers nettoyés"
    echo ""
fi

# Vérifier si les ports sont déjà utilisés
echo "🔍 Vérification des ports..."
PORTS_IN_USE=false

if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8001 déjà utilisé"
    PORTS_IN_USE=true
fi

if lsof -Pi :3002 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 3002 déjà utilisé"
    PORTS_IN_USE=true
fi

if lsof -Pi :1418 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 1418 déjà utilisé"
    PORTS_IN_USE=true
fi

if lsof -Pi :11434 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 11434 (Ollama) déjà utilisé"
    PORTS_IN_USE=true
fi

if [ "$PORTS_IN_USE" = true ]; then
    echo ""
    echo "❌ Certains ports sont déjà utilisés par d'autres processus"
    echo "💡 Solutions :"
    echo "   1. Arrêter les processus utilisant ces ports"
    echo "   2. Modifier les ports dans docker-compose.yml"
    echo ""
    echo "🔍 Pour voir qui utilise les ports :"
    echo "   lsof -i :8001"
    echo "   lsof -i :3002"
    echo "   lsof -i :1418"
    echo "   lsof -i :11434"
    echo ""
    read -p "Voulez-vous continuer quand même ? (o/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
fi

echo ""

# Déterminer si un build est nécessaire
NEED_BUILD=false

# Vérifier si les images Docker existent
if ! docker images | grep -q "ia-python-api"; then
    echo "🔨 Images Docker non trouvées, build nécessaire"
    NEED_BUILD=true
elif [ ! -d "./modele_final" ]; then
    echo "🔨 Modèle non trouvé, rebuild nécessaire pour entraîner"
    NEED_BUILD=true
else
    echo "✅ Images Docker et modèle existants"
fi

echo ""

if [ "$NEED_BUILD" = true ]; then
    echo "🐳 Construction et démarrage des containers Docker..."
    echo "========================================"
    docker-compose up --build -d
else
    echo "🐳 Démarrage des containers Docker (sans rebuild)..."
    echo "========================================"
    docker-compose up -d
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Containers démarrés !"
    echo ""
    echo "🤖 Initialisation d'Ollama et téléchargement du modèle..."
    echo "   (Première fois : téléchargement de llama3.2 ~2GB, peut prendre 5-10 min)"
    echo ""
    
    # Exécuter le script d'initialisation d'Ollama
    ./init_ollama.sh
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Déploiement terminé !"
        echo ""
        echo "📍 Services disponibles :"
        echo "   - Frontend:    http://localhost:1418"
        echo "   - Backend:     http://localhost:3002"
        echo "   - Python API:  http://localhost:8001"
        echo "   - Ollama:      http://localhost:11434"
        echo ""
        echo "📊 Vérifier les logs : docker-compose logs -f"
        echo "🛑 Arrêter :           docker-compose down"
        echo ""
    else
        echo ""
        echo "❌ Erreur lors de l'initialisation d'Ollama"
        echo "💡 Vous pouvez réessayer avec : ./init_ollama.sh"
        echo "📊 Voir les logs : docker logs ia-ollama"
    fi
else
    echo ""
    echo "❌ Erreur lors du démarrage des containers"
    echo "📊 Voir les logs : docker-compose logs"
    exit 1
fi


