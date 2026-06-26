# Pocket-RAG

**Pocket-RAG** est une application en ligne de commande permettant d'effectuer de la recherche documentaire augmentée par génération (RAG) de manière entièrement locale, rapide et sécurisée. Le système s'appuie sur ChromaDB pour l'indexation sémantique et utilise l'API Groq pour l'inférence du modèle de langage.

## Prérequis

Avant de lancer l'application, assurez-vous de disposer des éléments suivants :

* Python 3.13 ou version supérieure.
* Un environnement virtuel configuré et activé.
* Une clé [API Groq valide](https://console.groq.com/keys).

## Installation

1. Clonez le dépôt dans votre répertoire de travail.
2. Créez votre environnement virtuel.
3. Activez votre environnement virtuel.
4. Installez les dépendances nécessaires.
5. Installez l'outil.

```bash
git clone <repository-url>
cd pocket-rag-cli

python -m venv .venv

# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt

pip install .

```

> **Note :** Vous ne pourrez exécuter l'outil que dans votre environnement virtuel, à moins de l'installer globalement dans votre environnement Python principal.

## Configuration

Après avoir installé l'outil, exécutez la commande suivante :

```bash
pocket-rag config get

```

Le processus de configuration se lancera automatiquement si une configuration essentielle est manquante.

## Utilisation

Exécutez la commande ci-dessous en remplaçant `"your-doc"` par le chemin vers votre document :

```bash
pocket-rag -d "your-doc" 
pocket-rag --doc "your-doc"

```

Lors du premier lancement, ChromaDB téléchargera localement le modèle d'embedding (`all-MiniLM-L6-v2`). Les démarrages suivants seront instantanés.

### Commandes utilitaires

```bash
pocket-rag --help
pocket-rag config get
pocket-rag config reset
pocket-rag -d "your-doc"
pocket-rag --doc "your-doc"

```

## Sécurité et limites de responsabilité

Ce système effectue un traitement local de vos documents pour la partie vectorielle. Par défaut, seuls les segments textuels pertinents (Contexte) liés à votre question sont transmis à l'API Groq. Veillez à ne pas indexer de données confidentielles ou sensibles si vous n'êtes pas autorisé à utiliser des API tierces.
