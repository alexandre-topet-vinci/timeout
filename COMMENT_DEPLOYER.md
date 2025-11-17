# 🎯 Comment déployer le modèle sur ton mini PC ?

## ❓ Le problème
Le modèle (`modele_final/`) est dans `.gitignore` donc il ne sera PAS poussé sur Git.

## ✅ 3 Solutions

### **Solution 1 : Entraîner directement dans Docker (AUTOMATIQUE)**

Le `Dockerfile.python` entraîne automatiquement le modèle au build :

```bash
# Sur ton mini PC
git clone <ton-repo>
cd IA
docker-compose up --build -d
```

**Avantages :**
- ✅ Tout automatique
- ✅ Pas besoin de transférer le modèle
- ✅ Build une seule fois

**Inconvénients :**
- ⏱️ Premier build long (~5-10 min)

---

### **Solution 2 : Transférer le modèle manuellement (RAPIDE)**

Entraîne sur ta machine, copie sur le mini PC :

```bash
# Sur ta machine de dev
python train_model.py  # Crée modele_final/
tar -czf modele.tar.gz modele_final/

# Transférer via SCP/USB
scp modele.tar.gz user@minipc:/chemin/vers/IA/

# Sur le mini PC
cd IA
tar -xzf modele.tar.gz
docker-compose up -d
```

**Avantages :**
- ✅ Très rapide (pas d'entraînement sur mini PC)
- ✅ Build Docker en 2 minutes

---

### **Solution 3 : Git LFS (pour gros fichiers)**

Utilise Git Large File Storage pour versionner le modèle :

```bash
# Sur ta machine de dev
git lfs install
git lfs track "modele_final/**"
git add .gitattributes modele_final/
git commit -m "Add trained model with LFS"
git push

# Sur mini PC
git lfs pull
docker-compose up -d
```

**Avantages :**
- ✅ Versionné proprement
- ✅ Partageable facilement

**Inconvénients :**
- ⚠️ Nécessite Git LFS sur GitHub/GitLab

---

## 🎯 Ma recommandation pour toi

**Solution 1 (Docker auto-train)** si :
- Tu veux un déploiement 100% automatique
- Tu as 10 minutes pour le premier build

**Solution 2 (Transfert manuel)** si :
- Tu veux le plus rapide
- Tu as accès physique/SSH au mini PC

## 📝 Script de setup inclus

J'ai créé `setup.sh` qui gère automatiquement :

```bash
./setup.sh
```

Il va :
1. ✅ Détecter si `modele_final/` existe
2. ✅ Proposer d'entraîner si absent
3. ✅ Lancer docker-compose avec la bonne config

---

## 🔧 Modification du .gitignore

Si tu veux quand même commit le modèle temporairement :

```bash
# Retirer temporairement de .gitignore
# Commenter la ligne : modele_final/

git add modele_final/
git commit -m "Add trained model for deployment"
git push

# Sur mini PC
git pull
docker-compose up -d

# Remettre dans .gitignore après
```

---

## ✨ Résumé

| Méthode | Temps setup | Complexité | Recommandé |
|---------|-------------|------------|------------|
| Docker auto-train | 10 min | 🟢 Facile | ✅ Oui |
| Transfert manuel | 2 min | 🟡 Moyen | ✅ Oui |
| Git LFS | 5 min | 🔴 Avancé | ⚠️ Si besoin |
| Commit temporaire | 3 min | 🟢 Facile | ✅ OK |

**Mon conseil : Utilise `./setup.sh` qui fait tout automatiquement !** 🚀
