#!/bin/bash

echo "🤖 Initialisation d'Ollama avec le modèle Llama3.2..."

# Attendre qu'Ollama soit prêt
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "✅ Ollama est prêt !"
        break
    fi
    echo "⏳ Attente d'Ollama... (tentative $((attempt + 1))/$max_attempts)"
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Timeout : Ollama n'a pas démarré"
    exit 1
fi

# Vérifier si le modèle est déjà téléchargé
if docker exec ia-ollama ollama list | grep -q "llama3.2"; then
    echo "✅ Le modèle llama3.2 est déjà installé"
else
    echo "📥 Téléchargement du modèle llama3.2 (2GB)..."
    docker exec ia-ollama ollama pull llama3.2
    echo "✅ Modèle llama3.2 installé avec succès !"
fi

echo "🎉 Ollama est prêt à générer des réponses !"
