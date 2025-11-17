#!/usr/bin/env python3
"""
Script pour générer un dataset massif de questions bêtes et normales
"""

import json
import random

# ============================================================================
# QUESTIONS BÊTES - Templates pour générer massivement
# ============================================================================

questions_betes_base = [
    # Questions dev basiques (1ère année)
    "Comment on crée une variable en Python ?",
    "C'est quoi HTML ?",
    "Comment je fais un print en Python ?",
    "C'est quoi une boucle for ?",
    "Comment on fait un if en JavaScript ?",
    "C'est quoi Git ?",
    "Pourquoi mon code marche pas ?",
    "C'est quoi une fonction ?",
    "Comment on installe Python ?",
    "C'est quoi un array ?",
    "Comment on fait une liste en Python ?",
    "C'est quoi JSON ?",
    "Comment on ouvre un fichier ?",
    "C'est quoi une classe ?",
    "Comment on fait un return ?",
    "C'est quoi CSS ?",
    "Comment on fait une variable en Java ?",
    "C'est quoi un string ?",
    "Comment on fait une addition en code ?",
    "C'est quoi SQL ?",
    "Pourquoi j'ai une erreur de syntaxe ?",
    "C'est quoi un integer ?",
    "Comment on fait un commentaire ?",
    "C'est quoi localhost ?",
    "Comment on démarre un serveur ?",
    "C'est quoi Node.js ?",
    "Comment on crée un objet ?",
    "C'est quoi un IDE ?",
    "Comment on fait un input ?",
    "C'est quoi React ?",
    "Pourquoi mon HTML s'affiche pas ?",
    "C'est quoi un bug ?",
    "Comment on fait un while ?",
    "C'est quoi une API ?",
    "Comment on import un module ?",
    "C'est quoi un framework ?",
    "Comment on fait un else ?",
    "C'est quoi TypeScript ?",
    "Comment on déclare une constante ?",
    "C'est quoi Docker ?",
    "Pourquoi j'ai undefined ?",
    "C'est quoi npm ?",
    "Comment on fait un tableau ?",
    "C'est quoi Bootstrap ?",
    "Comment on compile ?",
    "C'est quoi MongoDB ?",
    "Comment on fait une condition ?",
    "C'est quoi REST ?",
    "Comment on crée une base de données ?",
    "C'est quoi Kubernetes ?",
]

# Templates pour générer des variations
templates_betes = [
    "C'est quoi {concept} ?",
    "Comment on fait {action} ?",
    "Pourquoi j'ai {erreur} ?",
    "Comment on {verbe} un {objet} ?",
    "C'est quoi la différence entre {concept1} et {concept2} ?",
    "Comment on installe {outil} ?",
    "{concept} ça sert à quoi ?",
    "Pourquoi {probleme} ?",
    "Comment on utilise {outil} ?",
    "C'est quoi le truc pour {action} ?",
]

concepts_basiques = [
    "une variable", "une fonction", "une classe", "un objet", "une boucle",
    "un tableau", "une liste", "un dictionnaire", "un set", "une string",
    "un integer", "un float", "un boolean", "un null", "un undefined",
    "HTML", "CSS", "JavaScript", "Python", "Java", "C++", "C#", "Ruby",
    "PHP", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "SQL",
    "un serveur", "un client", "une API", "REST", "GraphQL", "JSON",
    "XML", "YAML", "un framework", "une librairie", "un package",
    "Git", "GitHub", "GitLab", "npm", "pip", "Maven", "Gradle",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Heroku",
    "React", "Angular", "Vue", "Svelte", "Next.js", "Nuxt.js",
    "Node.js", "Express", "Flask", "Django", "Spring", "Laravel",
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
    "un IDE", "VS Code", "IntelliJ", "Eclipse", "PyCharm",
    "localhost", "un port", "HTTP", "HTTPS", "TCP", "UDP",
    "le frontend", "le backend", "Full Stack", "DevOps",
]

actions_basiques = [
    "créer une variable", "déclarer une fonction", "appeler une méthode",
    "ouvrir un fichier", "lire un fichier", "écrire dans un fichier",
    "faire une boucle", "faire une condition", "retourner une valeur",
    "importer un module", "installer un package", "démarrer un serveur",
    "faire un print", "faire un input", "convertir un type",
    "comparer deux valeurs", "concaténer des strings", "parser du JSON",
]

erreurs_communes = [
    "une erreur de syntaxe", "undefined", "null", "une erreur 404",
    "une erreur 500", "un warning", "une exception", "un stack overflow",
    "un memory leak", "un segmentation fault", "un null pointer",
    "une boucle infinie", "un timeout", "un CORS error", "un 403 forbidden",
]

# ============================================================================
# QUESTIONS NORMALES - Templates pour générer massivement
# ============================================================================

questions_normales_base = [
    "Comment optimiser les performances d'un algorithme de tri sur de grandes volumétries ?",
    "Quelle est la différence entre un processus et un thread en programmation concurrente ?",
    "Comment implémenter un arbre binaire de recherche équilibré avec rotation AVL ?",
    "Explique-moi le fonctionnement de l'apprentissage par renforcement avec Q-learning",
    "Comment fonctionne le handshake TLS dans le protocole HTTPS ?",
    "Comment configurer Docker multi-stage builds pour optimiser les images ?",
    "Comment implémenter une API RESTful avec validation de schéma et gestion d'erreurs ?",
    "Comment gérer le RAII et les smart pointers en C++ moderne ?",
    "Comment fonctionne la backpropagation dans un réseau de neurones ?",
    "Comment sécuriser une application web contre les injections SQL et XSS ?",
]

templates_normales = [
    "Comment optimiser {aspect} dans {contexte} ?",
    "Quelle est la différence entre {concept1} et {concept2} en termes de {critere} ?",
    "Comment implémenter {pattern} avec {technologie} ?",
    "Explique-moi le fonctionnement de {concept} dans le contexte de {domaine}",
    "Comment gérer {probleme} dans une architecture {architecture} ?",
    "Quelle stratégie adopter pour {objectif} avec {contrainte} ?",
    "Comment configurer {outil} pour {cas_usage} en production ?",
    "Explique-moi le principe de {concept_avance} et son application pratique",
    "Comment déboguer {probleme_complexe} dans un système {type_systeme} ?",
    "Quelle est la meilleure approche pour {tache_complexe} en considérant {facteurs} ?",
]

aspects_avances = [
    "les performances", "la scalabilité", "la sécurité", "la résilience",
    "la disponibilité", "la cohérence", "la latence", "le throughput",
    "la consommation mémoire", "l'utilisation CPU", "les I/O",
]

contextes_avances = [
    "un système distribué", "une architecture microservices", "une application cloud-native",
    "un environnement de production", "une base de données relationnelle",
    "un système temps réel", "une application mobile", "un système embarqué",
]

patterns_avances = [
    "le pattern Repository", "le pattern Factory", "le pattern Singleton",
    "le pattern Observer", "le pattern Strategy", "le pattern Decorator",
    "le pattern Adapter", "le pattern Facade", "le pattern Proxy",
    "le pattern Chain of Responsibility", "le circuit breaker",
    "le pattern Saga", "CQRS", "Event Sourcing",
]

# ============================================================================
# GÉNÉRATEUR DE QUESTIONS
# ============================================================================

def generer_questions_betes(nombre=1000):
    """Génère des questions bêtes variées"""
    questions = list(questions_betes_base)
    
    # On génère sans vérifier l'unicité (plus rapide)
    for _ in range(nombre - len(questions)):
        template = random.choice(templates_betes)
        
        try:
            if "{concept}" in template and "{concept1}" not in template:
                question = template.format(concept=random.choice(concepts_basiques))
            elif "{concept1}" in template and "{concept2}" in template:
                concepts = random.sample(concepts_basiques, 2)
                question = template.format(concept1=concepts[0], concept2=concepts[1])
            elif "{action}" in template:
                question = template.format(action=random.choice(actions_basiques))
            elif "{erreur}" in template:
                question = template.format(erreur=random.choice(erreurs_communes))
            elif "{verbe}" in template and "{objet}" in template:
                verbes = ["créer", "modifier", "supprimer", "lire", "écrire"]
                objets = ["fichier", "dossier", "variable", "fonction", "classe"]
                question = template.format(verbe=random.choice(verbes), objet=random.choice(objets))
            elif "{probleme}" in template:
                problemes = ["mon code marche pas", "ça bug", "j'ai une erreur", "ça compile pas"]
                question = template.format(probleme=random.choice(problemes))
            elif "{outil}" in template:
                outils = ["Python", "Java", "Node.js", "Docker", "Git", "npm", "pip"]
                question = template.format(outil=random.choice(outils))
            else:
                continue
            
            questions.append(question)
        except:
            continue
    
    return questions[:nombre]

def generer_questions_normales(nombre=1000):
    """Génère des questions normales avancées"""
    questions = list(questions_normales_base)
    
    concepts_avances = [
        "l'algorithme de consensus Raft", "le garbage collector", "la backpropagation",
        "le virtual DOM", "les websockets", "le load balancing", "le sharding",
        "les transactions ACID", "le théorème CAP", "les index B-Tree",
        "l'optimistic locking", "le lazy loading", "le eager loading",
        "les closures", "les promises", "les generateurs", "les decorators",
    ]
    
    technologies = [
        "Kubernetes", "Docker", "Redis", "PostgreSQL", "MongoDB",
        "React", "Angular", "Vue.js", "Next.js", "Node.js",
        "Spring Boot", "Django", "Flask", "Express", "FastAPI",
        "GraphQL", "gRPC", "RabbitMQ", "Kafka", "Elasticsearch",
    ]
    
    architectures = [
        "microservices", "event-driven", "serverless", "monolithique modulaire",
        "hexagonale", "clean architecture", "layered", "CQRS",
    ]
    
    # Générer sans vérifier l'unicité
    for _ in range(nombre - len(questions)):
        template = random.choice(templates_normales)
        
        try:
            if "{aspect}" in template and "{contexte}" in template:
                question = template.format(
                    aspect=random.choice(aspects_avances),
                    contexte=random.choice(contextes_avances)
                )
            elif "{concept1}" in template and "{concept2}" in template:
                concepts = random.sample(concepts_avances, 2)
                criteres = ["performance", "scalabilité", "complexité", "fiabilité"]
                question = template.format(
                    concept1=concepts[0],
                    concept2=concepts[1],
                    critere=random.choice(criteres)
                )
            elif "{pattern}" in template and "{technologie}" in template:
                question = template.format(
                    pattern=random.choice(patterns_avances),
                    technologie=random.choice(technologies)
                )
            elif "{concept}" in template and "{domaine}" in template:
                domaines = ["systèmes distribués", "bases de données", "réseaux",
                           "sécurité", "machine learning", "cloud computing"]
                question = template.format(
                    concept=random.choice(concepts_avances),
                    domaine=random.choice(domaines)
                )
            elif "{probleme}" in template and "{architecture}" in template:
                problemes = ["la cohérence des données", "les transactions distribuées",
                           "le monitoring", "la scalabilité horizontale", "la résilience"]
                question = template.format(
                    probleme=random.choice(problemes),
                    architecture=random.choice(architectures)
                )
            else:
                continue
            
            questions.append(question)
        except:
            continue
    
    return questions[:nombre]

# ============================================================================
# RÉPONSES SARCASTIQUES
# ============================================================================

reponses_sarcastiques = [
    "T'es sérieux là ? T'es en 3ème année et tu poses cette question ? 🤦",
    "Euh... c'était pas dans le cours de première année ça ?",
    "Wow, impressionnant. Tu veux que je te montre comment ouvrir VS Code aussi ?",
    "C'est une blague ? Dis-moi que c'est une blague...",
    "Tu sais qu'il y a Google, la documentation, Stack Overflow... mais tu préfères me déranger avec ça ?",
    "Franchement, si tu sais pas ça après 3 ans, je m'inquiète pour ton diplôme",
    "Laisse-moi deviner, t'as séché tous les cours depuis septembre ?",
    "Niveau question, on est plus proche de la première semaine de première année là",
    "T'as pensé à lire NE SERAIT-CE QUE le premier chapitre de ton cours ?",
    "Je sais pas ce qui est pire : ta question ou le fait que t'assumes de la poser",
    "Attends, t'es vraiment en bachelier informatique toi ?",
    "C'est le genre de truc qu'on apprend littéralement le premier jour",
    "Tu devrais peut-être envisager une reconversion professionnelle",
    "La documentation existe. Les tutoriels existent. Ton cerveau, apparemment, moins",
    "Bravo champion, tu viens de prouver que ChatGPT ne peut pas tout résoudre",
    "Même mon neveu de 12 ans qui fait du Scratch saurait ça",
    "T'as vraiment réussi tes exams des années précédentes ou t'as juste copié ?",
    "Niveau question débile, tu viens de battre un record",
    "Je pensais pas qu'on pouvait poser une question aussi basique en 3ème année",
    "Tu sais qu'il y a une différence entre 'poser une question' et 'faire perdre du temps' ?",
    "Félicitations, tu es officiellement la personne avec le moins d'initiative que je connaisse",
    "C'est littéralement dans le README. TU SAIS, LE FICHIER QU'ON LIT EN PREMIER ?",
    "Laisse-moi te présenter mon ami Google, vous allez bien vous entendre",
    "Sérieusement, cette question mérite un award de la flemme intellectuelle",
    "Tu veux que je te fasse un dessin avec des couleurs aussi ?",
    "On est en 2025, pas en 1995. La documentation est gratuite et accessible",
    "J'ai vu des juniors plus débrouillards que toi",
    "Tu réalises que tu vas bientôt être diplômé et bosser en vrai ?",
    "C'est le genre de question qu'on pose à StackOverflow pour se faire lyncher",
    "Toi + Google + 30 secondes = réponse. Essaye, c'est magique",
    "Je compatis avec tes futurs collègues de stage",
    "Tu sais que 'RTFM' ça veut dire 'Read The F***ing Manual' ?",
    "Niveau autonomie : -12/10",
    "T'es le genre de dev qui demande comment on quitte Vim ?",
    "Cette question... je... non. Juste non.",
    "Tu fais un stage où cet été ? Je préviens tout de suite la boîte",
    "C'est beau de voir quelqu'un qui a absolument RIEN retenu en 3 ans",
    "Tu veux mon cours de première année ? Apparemment t'en as besoin",
    "La réponse est littéralement dans le nom du concept. LIT-TÉ-RA-LE-MENT.",
    "Je suis une IA et même moi je suis gênée pour toi",
    "T'as pensé à lire la doc ? Ou c'est trop demander ?",
    "Félicitations, tu viens de faire perdre 10 secondes à tout le monde",
    "Laisse-moi deviner : tu codes avec Copilot à 100% et t'as jamais rien compris ?",
    "C'est pas Google qui est en panne, c'est ton initiative",
    "Tu sais qu'on peut aussi RÉFLÉCHIR avant de poser une question ?",
    "Niveau effort : 0. Niveau attentes : infini.",
    "T'as tapé le même texte sur Google ? Non ? Pourquoi ?",
    "Je me demande comment t'as réussi à arriver en 3ème année sans savoir ça",
    "C'est mignon, tu découvres l'informatique en 3ème année",
    "Tu veux que je te fasse aussi tes TPs pendant que j'y suis ?",
    "Allez, un petit effort. Juste UN. Je crois en toi. Enfin presque.",
    "MDR. Non sérieusement, MDR.",
    "C'est dans le syllabus. PAGE 2. CHAPITRE 1. SECTION 1.",
    "Ta question est tellement basique que j'ai mal pour toi",
    "Laisse-moi deviner : tu lis jamais les messages d'erreur non plus ?",
    "Tu cherches vraiment ou tu veux juste qu'on fasse le boulot à ta place ?",
    "C'est quoi la prochaine étape, me demander comment on allume un PC ?",
    "Flemme niveau : expert. Compétences : à développer.",
    "Je suis déçu mais pas surpris",
    "C'est marrant, d'habitude c'est les stagiaires qui posent ce genre de questions",
    "Je vais te donner un conseil : ctrl+F dans la doc, c'est ton ami",
    "T'as vraiment fait 3 ans d'études pour en arriver là ?",
    "Okay je vais être sympa : ouvre la documentation et LIS",
    "C'est pas possible, t'es un troll, avoue",
    "Ta question est le genre de truc qui fait dire aux gens que les dev sont fainéants",
    "Allez, un petit effort de recherche. Juste 2 minutes. S'il te plaît.",
    "Je sens que ton stage va être... intéressant",
    "Tu codes comme tu poses des questions : sans réfléchir",
]

# ============================================================================
# GÉNÉRATION ET SAUVEGARDE
# ============================================================================

def generer_dataset(nb_betes=2000, nb_normales=2000):
    """Génère un dataset complet"""
    print(f"🚀 Génération de {nb_betes + nb_normales} questions...")
    
    print(f"\n📝 Génération de {nb_betes} questions bêtes...")
    questions_betes = generer_questions_betes(nb_betes)
    print(f"✅ {len(questions_betes)} questions bêtes générées")
    
    print(f"\n📝 Génération de {nb_normales} questions normales...")
    questions_normales = generer_questions_normales(nb_normales)
    print(f"✅ {len(questions_normales)} questions normales générées")
    
    dataset = {
        "questions_betes": questions_betes,
        "questions_normales": questions_normales,
        "reponses_sarcastiques": reponses_sarcastiques
    }
    
    print(f"\n💾 Sauvegarde dans training_data.json...")
    with open('training_data.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dataset sauvegardé !")
    print(f"\n📊 Statistiques :")
    print(f"   - Questions bêtes : {len(questions_betes)}")
    print(f"   - Questions normales : {len(questions_normales)}")
    print(f"   - Réponses sarcastiques : {len(reponses_sarcastiques)}")
    print(f"   - TOTAL : {len(questions_betes) + len(questions_normales)} exemples")

if __name__ == "__main__":
    # Commencer avec 1000 de chaque type pour tester
    # Tu pourras augmenter ensuite si ça marche bien
    generer_dataset(nb_betes=1000, nb_normales=1000)
