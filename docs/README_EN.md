# Pocket-RAG

**Pocket-RAG** is a command-line application designed to perform Retrieval-Augmented Generation (RAG) entirely locally, quickly, and securely. The system relies on ChromaDB for semantic indexing and uses the Groq API by default for language model inference.

## Prerequisites

Before running the application, make sure you have the following:

* Python 3.13 or later.
* A configured and activated virtual environment.
* A valid [Groq API key](https://console.groq.com/keys) (default configuration).

## Installation

1. Clone the repository into your working directory.
2. Create your virtual environment.
3. Activate your virtual environment.
4. Install the required dependencies.

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

Create a `.env` file from `.env.example` in the project's root directory and add your credentials:

```env
GROQ_API_KEY=your_api_key_here
GROQ_LLM_MODEL=your_model_of_choice
```

Place the text file you want to index in the dedicated subdirectory. By default, the system looks for the following path: **res/document.txt**.

## Project Architecture

The project follows the modular structure below:

```txt
pocket-rag-cli/
    res/
        document.txt : The source document containing the information.
    src/
        prompt.py : Contains the strict system instructions (System Prompt) that govern the language model's behavior.
        chunk_builder.py : Handles reading and chunking the source document.
        vector_db.py : Manages the local ChromaDB vector database (indexing and retrieval).
        groq_query.py : Handles Groq API requests with strict type validation.
    main.py : Main entry point responsible for system initialization and the interactive user loop.
```

## Usage

To start the application, run the following command from your terminal:

```bash
python main.py
```

On the first launch, ChromaDB will download the embedding model (`all-MiniLM-L6-v2`) locally. Subsequent launches will start instantly.

Available commands:

```md
Type your question directly into the terminal to query your document.
Type exit to gracefully close the application.
```

## Security and Disclaimer

This system processes your documents locally for vectorization and retrieval. Only the relevant text segments (Context) associated with your query are sent to the Groq API by default. Do not index confidential data unless you are authorized to use third-party APIs.
