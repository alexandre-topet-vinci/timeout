# 🧠 EXPLICATION DÉTAILLÉE : Comment fonctionne l'entraînement de l'IA

## 📚 Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Étape 1 : Préparation des données](#étape-1--préparation-des-données)
3. [Étape 2 : Le modèle DistilBERT](#étape-2--le-modèle-distilbert)
4. [Étape 3 : Tokenization](#étape-3--tokenization)
5. [Étape 4 : L'entraînement (Fine-tuning)](#étape-4--lentraînement-fine-tuning)
6. [Étape 5 : La prédiction](#étape-5--la-prédiction)
7. [Les mathématiques derrière](#les-mathématiques-derrière)

---

## Vue d'ensemble

```
┌─────────────────┐
│  Questions      │
│  + Labels       │  ──────┐
└─────────────────┘        │
                           ▼
                    ┌──────────────┐
                    │ Tokenization │  (Convertir texte → nombres)
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Modèle     │  (DistilBERT - 66M paramètres)
                    │  Pré-entraîné│
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Fine-tuning │  (Ajuster pour notre tâche)
                    │   5 epochs   │
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Modèle       │  (Classifier: bête ou normale)
                    │ Entraîné     │
                    └──────────────┘
```

---

## Étape 1 : Préparation des données

### 1.1 Qu'est-ce qu'on fait ?

On prépare nos **40 exemples** :
- 20 questions **normales** → Label = 0
- 20 questions **bêtes** → Label = 1

```python
exemples = [
    ("Comment implémenter un algorithme ?", 0),  # Normale
    ("1 + 1 ça fait combien ?", 1),              # Bête
    ("Explique-moi REST vs GraphQL", 0),         # Normale
    ("Est-ce que l'eau est mouillée ?", 1),      # Bête
]
```

### 1.2 Split Train/Test (80/20)

On divise les données :
- **32 exemples** pour l'entraînement (80%)
- **8 exemples** pour le test (20%)

```python
train_texts, test_texts, train_labels, test_labels = train_test_split(
    textes, labels, 
    test_size=0.2,      # 20% pour test
    stratify=labels      # Garder la même proportion de bêtes/normales
)
```

**Pourquoi ?**
- **Train** : Le modèle apprend sur ces données
- **Test** : On vérifie si le modèle généralise bien (évite le sur-apprentissage)

---

## Étape 2 : Le modèle DistilBERT

### 2.1 Qu'est-ce que DistilBERT ?

**DistilBERT** est une version **allégée** de BERT :
- **BERT** : 110 millions de paramètres (lourd)
- **DistilBERT** : 66 millions de paramètres (40% plus léger, 60% plus rapide)
- **Multilingue** : Fonctionne avec le français, anglais, etc.

### 2.2 Pré-entraînement

Le modèle a déjà été **pré-entraîné** sur des millions de textes pour :
- Comprendre la grammaire
- Comprendre le contexte
- Comprendre les relations entre mots

**Analogie** : C'est comme un étudiant qui a déjà une éducation générale, 
maintenant on va lui apprendre une tâche spécifique.

### 2.3 Architecture du modèle

```
Input: "Est-ce que l'eau est mouillée ?"
   │
   ▼
┌─────────────────────────────────────┐
│  Tokenizer                          │  Convertir en tokens
│  ["est", "-", "ce", "que", "l", ...] │
└─────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────┐
│  Embedding Layer                    │  Chaque token → vecteur
│  [0.23, -0.45, 0.67, ...]          │  (768 dimensions)
└─────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────┐
│  6 Transformer Layers               │  Comprendre le contexte
│  (Attention + Feed Forward)         │
└─────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────┐
│  Classification Head                │  
│  2 neurones : [prob_normale, prob_bête] │
│  Output: [0.37, 0.63]               │
└─────────────────────────────────────┘
   │
   ▼
Prédiction: "Question BÊTE" (63% confiance)
```

---

## Étape 3 : Tokenization

### 3.1 Pourquoi tokenizer ?

Les ordinateurs ne comprennent que les **nombres**, pas le texte.
On doit convertir : `texte` → `nombres`

### 3.2 Comment ça marche ?

```python
question = "Est-ce que l'eau est mouillée ?"

# Étape 1: Découper en tokens (sous-mots)
tokens = ["est", "-", "ce", "que", "l", "'", "eau", "est", "mouil", "##lée", "?"]

# Étape 2: Convertir en IDs (nombres du vocabulaire)
input_ids = [1047, 118, 1456, 2034, 156, 112, 2345, 1047, 8923, 4567, 136]

# Étape 3: Ajouter padding si nécessaire (pour avoir la même longueur)
input_ids = [1047, 118, 1456, ..., 0, 0, 0]  # Padding avec des 0

# Étape 4: Créer un attention mask (1 = vrai token, 0 = padding)
attention_mask = [1, 1, 1, ..., 0, 0, 0]
```

### 3.3 Exemple concret

```python
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")

inputs = tokenizer(
    "1 + 1 ça fait combien ?",
    max_length=128,        # Longueur max
    padding='max_length',  # Ajouter des 0 si trop court
    truncation=True,       # Couper si trop long
    return_tensors="pt"    # Retourner des tensors PyTorch
)

# Résultat:
# {
#   'input_ids': tensor([[101, 122, 148, 122, 2567, 3421, 5678, 136, 102, 0, 0, ...]]),
#   'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, ...]])
# }
```

---

## Étape 4 : L'entraînement (Fine-tuning)

### 4.1 Qu'est-ce que le Fine-tuning ?

On **ajuste** les poids du modèle pré-entraîné pour notre tâche spécifique.

**Analogie** : 
- Le modèle sait déjà lire et comprendre le français (pré-entraînement)
- Maintenant on lui apprend à reconnaître les questions bêtes (fine-tuning)

### 4.2 Le processus d'entraînement

```python
# Configuration
TrainingArguments(
    num_train_epochs=5,              # 5 passages sur toutes les données
    per_device_train_batch_size=8,   # 8 exemples à la fois
    learning_rate=5e-5,              # Vitesse d'apprentissage
    weight_decay=0.01,               # Régularisation
)
```

### 4.3 Un epoch en détail

```
EPOCH 1 : Le modèle voit les 32 exemples d'entraînement
┌──────────────────────────────────────────────────────────┐
│ Batch 1 (8 exemples)                                     │
│  1. "Comment implémenter..." → Label: 0 (normale)        │
│  2. "1 + 1 ça fait combien ?" → Label: 1 (bête)         │
│  ... (6 autres exemples)                                 │
│                                                          │
│  Prédiction du modèle: [0.5, 0.5] (random au début)    │
│  Vrai label: [0, 1]                                      │
│  Calcul de l'erreur (loss)                              │
│  Ajustement des poids (backpropagation)                 │
└──────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────┐
│ Batch 2 (8 exemples)                                     │
│  ... même processus ...                                  │
└──────────────────────────────────────────────────────────┘
│
▼
... Batches 3, 4 ...
│
▼
┌──────────────────────────────────────────────────────────┐
│ ÉVALUATION sur les 8 exemples de test                   │
│  Accuracy: 50% (epoch 1), 62.5% (epoch 3), 100% (epoch 5)│
└──────────────────────────────────────────────────────────┘
```

### 4.4 La fonction de perte (Loss)

La **loss** mesure l'erreur du modèle. On utilise **Cross-Entropy Loss** :

```
Loss = - Σ (y_réel × log(y_prédit))

Exemple:
- Vrai label: [0, 1]  (question bête)
- Prédiction: [0.3, 0.7]  (70% bête)
- Loss = -(0 × log(0.3) + 1 × log(0.7)) = 0.36

Si la prédiction était [0.1, 0.9] → Loss = 0.10 (meilleur !)
```

Plus la loss est **petite**, mieux c'est !

### 4.5 Backpropagation (Ajustement des poids)

```
┌─────────────────────────────────────────┐
│  1. Forward Pass                        │
│     Input → Modèle → Prédiction         │
│     Calculer la loss                    │
└─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  2. Backward Pass                       │
│     Calculer le gradient de la loss     │
│     par rapport à chaque poids          │
│     (Dérivées partielles)               │
└─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  3. Mise à jour des poids               │
│     nouveau_poids = ancien_poids        │
│                   - learning_rate × gradient │
└─────────────────────────────────────────┘
```

**Exemple simplifié** :
```python
# Un poids quelconque dans le réseau
poids = 0.5

# Gradient (direction pour réduire l'erreur)
gradient = 0.2  

# Learning rate
lr = 0.01

# Mise à jour
nouveau_poids = 0.5 - (0.01 × 0.2) = 0.498
```

Le modèle fait ça pour **66 millions de paramètres** !

---

## Étape 5 : La prédiction

### 5.1 Comment le modèle prédit ?

```python
question = "Est-ce que l'eau est mouillée ?"

# 1. Tokenization
inputs = tokenizer(question, return_tensors="pt")
# → input_ids: [101, 1047, 118, 1456, 2034, ...]

# 2. Forward pass dans le modèle
outputs = model(**inputs)
# → logits: tensor([[-0.5, 0.8]])  (2 valeurs brutes)

# 3. Softmax pour obtenir des probabilités
probabilities = softmax([-0.5, 0.8])
# → [0.37, 0.63]  (37% normale, 63% bête)

# 4. Décision
if probabilities[1] > 0.5:
    print("Question BÊTE !")
else:
    print("Question normale")
```

### 5.2 Softmax en détail

La fonction **softmax** convertit les valeurs brutes en probabilités :

```
Softmax(x_i) = e^(x_i) / Σ e^(x_j)

Exemple:
logits = [-0.5, 0.8]

e^(-0.5) = 0.606
e^(0.8) = 2.226
total = 0.606 + 2.226 = 2.832

P(normale) = 0.606 / 2.832 = 0.214 = 21.4%
P(bête) = 2.226 / 2.832 = 0.786 = 78.6%
```

---

## Les mathématiques derrière

### 1. Transformer Architecture

Le cœur de DistilBERT : l'**attention mechanism**

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V

Où:
- Q = Query (requête)
- K = Key (clé)
- V = Value (valeur)
- d_k = dimension (768)
```

**Intuition** : Chaque mot "regarde" les autres mots pour comprendre le contexte.

Exemple : "Est-ce que l'**eau** est **mouillée** ?"
- Le mot "eau" va prêter attention à "mouillée"
- Score d'attention : 0.8 (forte relation)

### 2. Feed Forward Network

Après l'attention, chaque position passe par :

```
FFN(x) = max(0, xW₁ + b₁)W₂ + b₂

Où:
- W₁, W₂ = matrices de poids
- b₁, b₂ = biais
- max(0, ...) = fonction ReLU (activation)
```

### 3. Classification finale

```
logits = W_classifier × h_[CLS] + b

Où:
- h_[CLS] = représentation du token spécial [CLS] (768 dimensions)
- W_classifier = matrice (768 × 2)
- logits = [logit_normale, logit_bête]
```

### 4. Fonction de perte (Cross-Entropy)

```
Loss = -log(P(y_réel))

Pour tout le batch:
Loss = -(1/N) Σ [y_i × log(ŷ_i) + (1-y_i) × log(1-ŷ_i)]

Où:
- y_i = label réel (0 ou 1)
- ŷ_i = probabilité prédite
- N = taille du batch
```

### 5. Optimisation (AdamW)

L'algorithme **AdamW** ajuste les poids :

```
m_t = β₁ × m_{t-1} + (1 - β₁) × g_t        # Moyenne mobile du gradient
v_t = β₂ × v_{t-1} + (1 - β₂) × g_t²       # Variance du gradient

m̂_t = m_t / (1 - β₁^t)                     # Correction du biais
v̂_t = v_t / (1 - β₂^t)

θ_t = θ_{t-1} - α × m̂_t / (√v̂_t + ε) - λ × θ_{t-1}

Où:
- g_t = gradient
- α = learning rate (5e-5)
- β₁ = 0.9, β₂ = 0.999
- λ = weight decay (0.01)
- ε = 1e-8
```

---

## 🎯 Résumé visuel complet

```
                    ENTRAÎNEMENT
════════════════════════════════════════════════

┌─────────────────┐
│  "1+1=?"        │  Question
│  Label: 1       │  (bête)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Tokenizer                          │
│  [101, 122, 148, 122, 136, 102]    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Embedding (768 dim par token)      │
│  [[0.23, -0.45, ...], ...]          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Transformer Layer 1                │
│    - Multi-Head Attention           │
│    - Feed Forward                   │
└────────┬────────────────────────────┘
         │
         ▼
    ... (layers 2-6) ...
         │
         ▼
┌─────────────────────────────────────┐
│  Pooling [CLS] token                │
│  Vecteur contextualisé (768 dim)    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Classification Head                │
│  Logits: [-0.5, 0.8]                │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Softmax                            │
│  Probas: [0.37, 0.63]               │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Calcul Loss                        │
│  Vrai: [0, 1]                       │
│  Prédit: [0.37, 0.63]               │
│  Loss = 0.46                        │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Backpropagation                    │
│  Calculer ∂Loss/∂poids              │
│  pour 66M paramètres                │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Mise à jour poids (AdamW)          │
│  poids_new = poids - lr × gradient  │
└─────────────────────────────────────┘
         │
         ▼
    Répéter 5 epochs × 4 batches = 20 itérations
         │
         ▼
┌─────────────────────────────────────┐
│  Modèle final : 100% accuracy ! 🎉  │
└─────────────────────────────────────┘
```

---

## 🔑 Points clés à retenir

1. **Pré-entraînement** : Le modèle connaît déjà le langage
2. **Fine-tuning** : On l'ajuste pour notre tâche spécifique (40 exemples)
3. **Tokenization** : Convertir texte → nombres que l'ordinateur comprend
4. **Forward Pass** : Données → Modèle → Prédiction
5. **Loss** : Mesure de l'erreur
6. **Backpropagation** : Calculer comment ajuster les poids
7. **Optimisation** : AdamW met à jour les 66M paramètres
8. **Epochs** : Répéter 5 fois sur toutes les données
9. **Évaluation** : Tester sur données non vues (8 exemples)
10. **Résultat** : 100% de précision ! 🎉

---

## 🚀 Pour aller plus loin

### Concepts avancés

1. **Attention Mechanism** : Comment le modèle "comprend" le contexte
2. **Dropout** : Régularisation pour éviter le sur-apprentissage
3. **Learning Rate Scheduling** : Ajuster le taux d'apprentissage pendant l'entraînement
4. **Data Augmentation** : Créer plus d'exemples à partir des données existantes
5. **Transfer Learning** : Utiliser les connaissances d'une tâche pour une autre

### Ressources

- 📖 [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (paper original Transformer)
- 📖 [BERT Paper](https://arxiv.org/abs/1810.04805)
- 📖 [DistilBERT Paper](https://arxiv.org/abs/1910.01108)
- 🎓 [Hugging Face Course](https://huggingface.co/course)
- 🎓 [Fast.ai Deep Learning](https://course.fast.ai/)

---

**Créé avec ❤️ pour comprendre comment entraîner une IA**
