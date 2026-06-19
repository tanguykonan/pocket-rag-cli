import chromadb

def init_local_vector_db(chunks: list):
    """
        Initialization and Indexing of the vector database.
    Creation of the database that turns texts into numbers.
    @chunks: The chuncks obtain with chunk_builder module.
    """
    # NOTE: We create the ChromaDB client in 'Ephemeral' mode (in RAM for testing).
    chroma_client = chromadb.EphemeralClient() 
    '''
        We create a collection witch a unique name
    NOTE: A collection is the equivalent of a sql table.
    '''
    collection = chroma_client.create_collection(name="hands_on_training")
    '''
        List comprehension of mandatory genereted IDs
    '''
    ids = [f'id_{i}' for i in range(len(chunks))]
    '''
        Automatic indexing
    NOTE: It's AT THAT EXACT MOMENT that ChromaDB calls its internal embedding model,
    calculates the numbers (vectors) for each chunk, and stores them in its geometric index.
    '''
    collection.add(
        documents=chunks,
        ids=ids
    )

    return collection

def search_in_vector_db(collection, question: str, top_n: int=2):
    '''
        The semantic query
    @collection: The collection obtain with init_local_vector_db function.
    @question : The input of a question.
    @top_n: Used to limit the number of texte piece that the database will return.
    '''
    results = collection.query(
        query_texts=[question],
        n_results=top_n
    )
    '''
        NOTE: query() function will do:
            - Turning the question into numbers.
            - Calculating the geometric distance with the numbers of the stored pieces.
            - Sorts it and sends back the 'top_n' closest pieces.
    '''
    # NOTE: Return structure of ChromaDB : List of list into the 'documents' key.
    '''We neatly extract the list of texts found.'''
    best_chunks = results['documents'][0]

    return best_chunks

