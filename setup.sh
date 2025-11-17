#!/bin/bash

echo "🚀 Setup IA Sarcastique pour déploiement"
echo "========================================"
echo ""

# Vérifier si le modèle existe localement
if [ -d "./modele_final" ]; then
    echo "✅ Modèle trouvé localement dans ./modele_final/"
    echo "📦 Le modèle sera monté via volume Docker"
    echo ""
    echo "Utilisation du docker-compose.yml (avec volumes)"
    COMPOSE_FILE="docker-compose.yml"
else
    echo "⚠️  Modèle non trouvé dans ./modele_final/"
    echo "🏗️  Le modèle sera entraîné lors du build Docker"
    echo ""
    echo "Option 1 : Entraîner le modèle maintenant (recommandé)"
    echo "Option 2 : Laisser Docker l'entraîner (plus long au build)"
    echo ""
    read -p "Voulez-vous entraîner le modèle maintenant ? (o/N) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        echo "🎓 Entraînement du modèle..."
        
        # Vérifier si l'environnement virtuel existe
        if [ ! -d ".venv" ]; then
            echo "📦 Création de l'environnement virtuel..."
            python3 -m venv .venv
        fi
        
        echo "📥 Installation des dépendances..."
        source .venv/bin/activate
        pip install -q -r requirements.txt
        
        echo "📝 Génération du dataset..."
        python generer_dataset_avance.py
        
        echo "🏋️  Entraînement en cours..."
        python train_model.py
        
        if [ $? -eq 0 ]; then
            echo "✅ Modèle entraîné avec succès !"
            COMPOSE_FILE="docker-compose.yml"
        else
            echo "❌ Erreur lors de l'entraînement"
            exit 1
        fi
    else
        echo "⏩ Le modèle sera entraîné dans Docker"
        COMPOSE_FILE="docker-compose.yml"
    fi
fi

echo ""
echo "🐳 Démarrage des containers Docker..."
echo "========================================"
docker-compose -f $COMPOSE_FILE up --build -d

echo ""
echo "✅ Déploiement terminé !"
echo ""
echo "📍 Services disponibles :"
echo "   - Frontend:    http://localhost:3000"
echo "   - Backend:     http://localhost:3001"
echo "   - Python API:  http://localhost:8000"
echo ""
echo "📊 Vérifier les logs : docker-compose logs -f"
echo "🛑 Arrêter :           docker-compose down"
echo ""
