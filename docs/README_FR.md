# Pocket-RAG

**Pocket-RAG** est une application en ligne de commande permettant d'effectuer de la recherche documentaire augmentée par génération (RAG) de manière entièrement locale, rapide et sécurisée. Le système s'appuie sur ChromaDB pour l'indexation sémantique et utilise, par défaut, l'API Groq pour l'inférence au modèle de langage.

## Prérequis

Avant de lancer l'application, assurez-vous de disposer des éléments suivants :

- Python 3.13 ou version supérieure.
- Un environnement virtuel configuré et activé.
- Une clé [API Groq valide](https://console.groq.com/keys) (configuration par défaut).

## Installation

1. Clonez le dépôt dans votre répertoire de travail.
2. Créez votre environnement virtuel.
3. Activez votre environnement virtuel.
4. Installez les dépendances nécessaires

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

Créez un fichier .env à partir du fichier .env.example à la racine du projet et ajoutez-y vos identifiants :

```.env
GROQ_API_KEY=votre_cle_api_ici
GROQ_LLM_MODEL=le_model_de_votre_choix
```

Placez le fichier texte que vous souhaitez indexer dans le sous-dossier dédié. Par défaut, le système recherche le chemin suivant : **res/document.txt**.

## Architecture du Projet

Le projet est structuré selon l'organisation modulaire suivante :

```txt
pocket-rag-cli/
    res/
        document.txt : Le document de vérité contenant les informations.
    src/
        prompt.py : Contient les instructions système strictes (System Prompt) dictant le comportement du modèle de langage.
        chunk_builder.py : Module chargé de la lecture et de la segmentation du fichier source.
        vector_db.py : Gestionnaire de la base de données vectorielle locale ChromaDB (indexation et recherche).
        groq_query.py : Gestionnaire des appels vers l'API Groq avec validation stricte des types.
    main.py : Point d'entrée principal orchestrant l'initialisation du système et la boucle interactive utilisateur.
```

## Utilisation

Pour démarrer l'application, exécutez la commande suivante depuis votre terminal :

```bash
python main.py
```

Lors du premier lancement, ChromaDB téléchargera localement le modèle d'embedding (all-MiniLM-L6-v2). Les démarrages suivants seront instantanés.

Commandes disponibles dans l'interface :

```md
Saisissez votre question directement dans le terminal pour interroger votre document.
Tapez exit pour fermer proprement l'application.
```

## Sécurité et Limites de Responsabilité

Ce système effectue un traitement local de vos documents pour la partie vectorielle. Seuls les segments textuels pertinents (Context) liés à votre question sont transmis à l'API Groq par défaut. Veillez à ne pas indexer de données confidentielles si vous n'êtes pas autorisé à utiliser des API tierces.
