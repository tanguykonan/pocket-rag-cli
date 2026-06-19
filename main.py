from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from src.groq_query import generate_response
from src.chunk_builder import load_and_chunk_file
from src.vector_db import init_local_vector_db, search_in_vector_db

console = Console()
'''Instantiation of the main object of the rich library'''

''''-------------------------------------------------------------------
-------------------------- CONSTANTS ----------------------------------
--------------------------------------------------------------------'''
FILE_PATH = "res/document.txt"
CHUNK_SIZE = 150
'''Default value is 150'''
TOP_N = 3
'''Default value is 2'''


''''-------------------------------------------------------------------
---------------------------- PROCESS ----------------------------------
--------------------------------------------------------------------'''
if __name__ == "__main__":
    
    console.print("[POCKET-RAG]: Start of rag system initialization...", style="bold yellow")
    chunks = load_and_chunk_file(file_path=FILE_PATH, chunk_size=CHUNK_SIZE)
    if not chunks:
        console.print(f"[POCKET-RAG]: The file {FILE_PATH} don't have a content", style="bold underline red")
        exit(1)
    collection = init_local_vector_db(chunks=chunks)
    console.print('[POCKET-RAG]: End of rag system initialization', style="bold green")

    is_used = True
    while is_used:

        question = Prompt.ask("[bold cyan] o(*￣︶￣*)o -> Have you a question? Ask your question or exit.[/]")
        
        if question.lower().strip() == 'exit':
            console.print('[POCKET-RAG]: Thank you for your test. We have after (≧﹏ ≦)', style="bold blue")
            is_used = False
            exit(0)
        
        with console.status("[bold green] (*^▽^*)-> Searching the database and generating the response... [/]"):
            internal_response = search_in_vector_db(collection=collection, question=question, top_n=TOP_N)
            context = "\n\n".join(internal_response)
            llm_response = generate_response(question=question, context=context)

        if llm_response == '' or not llm_response:
            console.print('{{{(>_<)}}} -> There are problem with your generate_response method.', style="bold yellow")
            is_used = False
            exit(1)

        console.print(Panel(llm_response, title="[bold green](★‿★) -> Assistant Response[/]", border_style="cyan"))
            

