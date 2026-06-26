# Pocket-RAG

**Pocket-RAG** is a command-line application designed to perform Retrieval-Augmented Generation (RAG) entirely locally, quickly, and securely. The system relies on ChromaDB for semantic indexing and uses the Groq API for language model inference.

## Prerequisites

Before running the application, ensure you have the following:

* Python 3.13 or higher.
* A configured and activated virtual environment.
* A valid [Groq API key](https://console.groq.com/keys).

## Installation

1. Clone the repository into your working directory.
2. Create your virtual environment.
3. Activate your virtual environment.
4. Install the required dependencies.
5. Install the tool.

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

> **Note:** You will only be able to run the tool within your virtual environment unless you install it globally in your main Python environment.

## Configuration

After installing the tool, run the following command:

```bash
pocket-rag config get

```

The configuration process will start automatically if any critical configuration is missing.

## Usage

Run the command below, replacing `"your-doc"` with the path to your document:

```bash
pocket-rag -d "your-doc" 
pocket-rag --doc "your-doc"

```

During the first run, ChromaDB will download the embedding model (`all-MiniLM-L6-v2`) locally. Subsequent startups will be instantaneous.

### Utility Commands

```bash
pocket-rag --help
pocket-rag config get
pocket-rag config reset
pocket-rag -d "your-doc"
pocket-rag --doc "your-doc"

```

## Security and Disclaimer

This system processes your documents locally for the vectorization part. By default, only the relevant text segments (Context) related to your prompt are sent to the Groq API. Please ensure you do not index sensitive or confidential data if you are not authorized to use third-party APIs.
