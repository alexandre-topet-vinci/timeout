#!/usr/bin/env python3
"""
Script de démonstration visuelle : Comment l'IA apprend pas à pas
"""

import torch
import torch.nn.functional as F
import numpy as np

print("=" * 70)
print("🧠 DÉMONSTRATION : Comment l'IA apprend à détecter les questions bêtes")
print("=" * 70)
print()

# ============================================================================
# PARTIE 1 : TOKENIZATION
# ============================================================================

print("📝 PARTIE 1 : TOKENIZATION (Texte → Nombres)")
print("-" * 70)

question = "Est-ce que l'eau est mouillée ?"
print(f"Question originale: '{question}'")
print()

# Simulation simplifiée de la tokenization
tokens = ["est", "-", "ce", "que", "l", "'", "eau", "est", "mouil", "##lée", "?"]
print(f"Étape 1 - Découpage en tokens:")
print(f"  {tokens}")
print()

# Conversion en IDs (simulé)
token_ids = [1047, 118, 1456, 2034, 156, 112, 2345, 1047, 8923, 4567, 136]
print(f"Étape 2 - Conversion en IDs (nombres du vocabulaire):")
print(f"  {token_ids}")
print()

# Padding
max_length = 20
padded_ids = token_ids + [0] * (max_length - len(token_ids))
attention_mask = [1] * len(token_ids) + [0] * (max_length - len(token_ids))
print(f"Étape 3 - Padding à longueur {max_length}:")
print(f"  Input IDs:      {padded_ids}")
print(f"  Attention Mask: {attention_mask}")
print(f"  (1 = vrai token, 0 = padding)")
print()

input("Appuyez sur Entrée pour continuer... ")
print()

# ============================================================================
# PARTIE 2 : EMBEDDINGS
# ============================================================================

print("🔢 PARTIE 2 : EMBEDDINGS (IDs → Vecteurs)")
print("-" * 70)

# Simuler des embeddings (normalement 768 dimensions, ici on en montre 5)
embedding_dim = 5
print(f"Chaque token est converti en un vecteur de {embedding_dim} dimensions")
print(f"(Dans DistilBERT, c'est 768 dimensions)")
print()

# Simuler quelques embeddings
embeddings_exemple = {
    "est": [0.23, -0.45, 0.67, -0.12, 0.89],
    "eau": [0.56, 0.34, -0.78, 0.91, -0.23],
    "mouillée": [0.45, 0.67, -0.34, 0.78, -0.56]
}

print("Exemples d'embeddings:")
for token, embedding in embeddings_exemple.items():
    print(f"  '{token}' → {embedding}")
print()

print("Ces vecteurs capturent le 'sens' du mot dans un espace mathématique.")
print("Des mots similaires ont des vecteurs proches !")
print()

input("Appuyez sur Entrée pour continuer... ")
print()

# ============================================================================
# PARTIE 3 : FORWARD PASS (Prédiction)
# ============================================================================

print("🚀 PARTIE 3 : FORWARD PASS (Prédiction)")
print("-" * 70)

print("Les embeddings passent à travers 6 couches de Transformers...")
print()

# Simuler le passage à travers le réseau
print("Couche 1: Multi-Head Attention + Feed Forward")
print("  → Le modèle 'regarde' les relations entre mots")
print("Couche 2-5: Même processus, de plus en plus abstrait")
print("Couche 6: Représentation finale contextuelle")
print()

# Simuler les logits finaux
print("Classification Head:")
print("  → Prend la représentation du token [CLS]")
print("  → Passe à travers une couche linéaire (768 → 2)")
print()

# Exemple avec des vraies valeurs
logits = torch.tensor([[-0.5, 0.8]])  # [logit_normale, logit_bête]
print(f"Logits bruts: {logits.tolist()[0]}")
print(f"  [normale, bête] = [{logits[0][0]:.2f}, {logits[0][1]:.2f}]")
print()

# Softmax
probabilities = F.softmax(logits, dim=1)
print("Après Softmax (conversion en probabilités):")
print(f"  P(normale) = {probabilities[0][0].item():.1%}")
print(f"  P(bête)    = {probabilities[0][1].item():.1%}")
print()

prediction = "BÊTE" if probabilities[0][1] > 0.5 else "NORMALE"
print(f"🎯 Prédiction finale: Question {prediction}")
print()

input("Appuyez sur Entrée pour continuer... ")
print()

# ============================================================================
# PARTIE 4 : CALCUL DE LA LOSS
# ============================================================================

print("📊 PARTIE 4 : CALCUL DE L'ERREUR (Loss)")
print("-" * 70)

# Label réel
true_label = 1  # C'est bien une question bête
print(f"Label réel: {true_label} (0=normale, 1=bête)")
print(f"Probabilité prédite pour 'bête': {probabilities[0][1].item():.3f}")
print()

# Cross-Entropy Loss
loss = F.cross_entropy(logits, torch.tensor([true_label]))
print(f"Cross-Entropy Loss = {loss.item():.4f}")
print()

print("💡 Interprétation:")
print("  - Loss proche de 0 = très bonne prédiction")
print("  - Loss élevée = mauvaise prédiction")
print()

# Montrer ce qui se passerait avec différentes prédictions
print("Exemple avec différentes prédictions:")
scenarios = [
    (torch.tensor([[2.0, -2.0]]), "Mauvaise prédiction (pense que c'est normal)"),
    (torch.tensor([[0.0, 0.0]]), "Incertain (50/50)"),
    (torch.tensor([[-1.0, 1.0]]), "Bonne prédiction (73% bête)"),
    (torch.tensor([[-3.0, 3.0]]), "Excellente prédiction (95% bête)"),
]

for scenario_logits, description in scenarios:
    scenario_prob = F.softmax(scenario_logits, dim=1)
    scenario_loss = F.cross_entropy(scenario_logits, torch.tensor([true_label]))
    print(f"  {description}")
    print(f"    → P(bête) = {scenario_prob[0][1].item():.1%}, Loss = {scenario_loss.item():.4f}")
print()

input("Appuyez sur Entrée pour continuer... ")
print()

# ============================================================================
# PARTIE 5 : BACKPROPAGATION
# ============================================================================

print("🔄 PARTIE 5 : BACKPROPAGATION (Ajustement des poids)")
print("-" * 70)

print("Le modèle calcule comment modifier ses 66 MILLIONS de paramètres")
print("pour réduire l'erreur.")
print()

# Simuler un poids simple
print("Exemple simplifié avec UN SEUL poids:")
print()

weight = 0.5
learning_rate = 0.01
gradient = 0.2  # Calculé par backpropagation

print(f"Poids actuel:        {weight}")
print(f"Gradient (∂Loss/∂w): {gradient}")
print(f"Learning rate:       {learning_rate}")
print()

new_weight = weight - learning_rate * gradient
print(f"Formule: nouveau_poids = ancien_poids - lr × gradient")
print(f"         {new_weight:.4f} = {weight} - {learning_rate} × {gradient}")
print()

print(f"✅ Nouveau poids: {new_weight:.4f}")
print()

print("💡 Le gradient indique dans quelle direction modifier le poids")
print("   pour RÉDUIRE l'erreur.")
print()

print("Dans le vrai modèle:")
print("  - 66 millions de paramètres")
print("  - Chacun a son propre gradient")
print("  - Tous mis à jour simultanément !")
print()

input("Appuyez sur Entrée pour continuer... ")
print()

# ============================================================================
# PARTIE 6 : ÉVOLUTION SUR PLUSIEURS EPOCHS
# ============================================================================

print("📈 PARTIE 6 : ÉVOLUTION DE L'APPRENTISSAGE")
print("-" * 70)

print("Simulation de l'apprentissage sur 5 epochs:")
print()

# Simuler l'évolution
epochs_data = [
    {"epoch": 1, "train_loss": 0.686, "eval_loss": 0.683, "accuracy": 0.50},
    {"epoch": 2, "train_loss": 0.652, "eval_loss": 0.671, "accuracy": 0.50},
    {"epoch": 3, "train_loss": 0.612, "eval_loss": 0.648, "accuracy": 0.625},
    {"epoch": 4, "train_loss": 0.543, "eval_loss": 0.592, "accuracy": 0.875},
    {"epoch": 5, "train_loss": 0.478, "eval_loss": 0.501, "accuracy": 1.00},
]

print("Epoch | Train Loss | Eval Loss | Accuracy")
print("-" * 50)
for data in epochs_data:
    bar_length = int(data["accuracy"] * 20)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    print(f"  {data['epoch']}   |   {data['train_loss']:.3f}    |   {data['eval_loss']:.3f}   | {data['accuracy']:.1%} {bar}")

print()
print("📊 Observations:")
print("  ✓ La loss diminue progressivement")
print("  ✓ L'accuracy augmente")
print("  ✓ Epoch 5: 100% de précision ! 🎉")
print()

input("Appuyez sur Entrée pour continuer... ")
print()

# ============================================================================
# PARTIE 7 : COMPARAISON AVANT/APRÈS
# ============================================================================

print("🎭 PARTIE 7 : AVANT vs APRÈS L'ENTRAÎNEMENT")
print("-" * 70)

questions_test = [
    ("Est-ce que l'eau est mouillée ?", True),
    ("Comment optimiser un algorithme ?", False),
    ("1 + 1 ça fait combien ?", True),
]

print("AVANT L'ENTRAÎNEMENT (modèle non entraîné):")
print("-" * 50)
for q, is_bete in questions_test:
    # Simuler des prédictions aléatoires
    random_prob = np.random.uniform(0.4, 0.6)
    prediction = "BÊTE" if random_prob > 0.5 else "NORMALE"
    status = "✅" if (prediction == "BÊTE") == is_bete else "❌"
    print(f"{status} '{q}'")
    print(f"   → {prediction} ({random_prob:.1%} confiance)")
print()

print("APRÈS L'ENTRAÎNEMENT (5 epochs):")
print("-" * 50)
for q, is_bete in questions_test:
    # Simuler des prédictions correctes
    if is_bete:
        prob = np.random.uniform(0.85, 0.95)
        prediction = "BÊTE"
    else:
        prob = np.random.uniform(0.15, 0.25)
        prediction = "NORMALE"
    
    print(f"✅ '{q}'")
    print(f"   → {prediction} ({prob:.1%} confiance)")
print()

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("=" * 70)
print("🎓 RÉSUMÉ : Comment l'IA apprend")
print("=" * 70)
print()

resume = """
1️⃣  TOKENIZATION : Texte → Nombres
    "Question" → [101, 1047, 118, ...] 

2️⃣  EMBEDDINGS : Nombres → Vecteurs de sens
    Chaque token devient un vecteur de 768 dimensions

3️⃣  TRANSFORMERS : Comprendre le contexte
    6 couches d'attention pour analyser les relations

4️⃣  PRÉDICTION : Vecteurs → Probabilités
    Softmax([−0.5, 0.8]) → [37%, 63%] (bête)

5️⃣  CALCUL DE LOSS : Mesurer l'erreur
    Cross-Entropy entre prédiction et vérité

6️⃣  BACKPROPAGATION : Calculer les gradients
    ∂Loss/∂poids pour chacun des 66M paramètres

7️⃣  OPTIMISATION : Ajuster les poids
    AdamW met à jour : poids -= lr × gradient

8️⃣  RÉPÉTER : 5 epochs × 32 exemples
    Le modèle s'améliore progressivement

9️⃣  ÉVALUATION : Tester sur données non vues
    Vérifier la généralisation (8 exemples test)

🎯  RÉSULTAT : 100% de précision !
"""

print(resume)
print()
print("=" * 70)
print("🎉 Maintenant vous savez comment une IA apprend ! 🎉")
print("=" * 70)
