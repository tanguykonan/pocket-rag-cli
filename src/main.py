import click
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from src.groq_query import generate_response
from src.config_manager import ConfigManager
from src.chunk_builder import load_and_chunk_file
from src.vector_db import init_local_vector_db, search_in_vector_db

console = Console()
manager = ConfigManager()

@click.group(invoke_without_command = True)
@click.option('-d', '--doc')
@click.pass_context
def cli(ctx, doc):
    """
        Main entry point for the Pocket-RAG CLI.

    If the `-d/--doc` option is provided, directly launches the RAG
    If no subcommand is invoked and no document is provided, displays the
    CLI help message.
    """

    if doc:
        use_config: dict = manager.get_config()
        api: str = use_config['groq_api_key']
        model: str = use_config['groq_model']
        chunk_size: int = use_config['chunk_size']
        top_n: int = use_config['top_n']

        console.print(" [POCKET-RAG]: Start of rag system initialization...", style="bold yellow")
        chunks = load_and_chunk_file(file_path=doc, chunk_size=chunk_size)
        collection = init_local_vector_db(chunks=chunks)
        console.print(' [POCKET-RAG]: End of rag system initialization', style="bold green")

        while True:
            try:
                question = Prompt.ask("[bold cyan] [POCKET-RAG]: o(*￣︶￣*)o Have you a question? Ask your question or exit.[/]")
        
                if question.lower().strip() == 'exit':
                    console.print(' [POCKET-RAG]: つ﹏⊂ Thank you for your test. We have after (≧﹏ ≦)', style="bold blue")
                    exit(0)
        
                with console.status("[bold green] [POCKET-RAG]: (*^▽^*) Searching the database and generating the response... [/]"):
                    internal_response = search_in_vector_db(collection=collection, question=question, top_n=top_n)
                    context = "\n\n".join(internal_response)
                    llm_response = generate_response(question=question, context=context, api=api, model=model)

                if llm_response == '' or not llm_response:
                    console.print(' [POCKET-RAG]: {{{(>_<)}}} There are problem with generate response method.', style="bold yellow")
                    exit(1)

                console.print(Panel(llm_response, title="[bold green](★‿★) Assistant Response[/]", border_style="cyan"))
        
            except KeyboardInterrupt:
                exit(0)


    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.group()
def config():
    """
        Command group dedicated to configuration management.

    Acts as a container for the `get` and `reset` subcommands.
    Contains no logic of its own.
    """
    pass

@config.command()
def get():
    """
        Displays the current configuration as a table.

    Retrieves the configuration via `ConfigManager.get_config()` and
    displays it in a formatted table (rich.Table) with two columns:
    key and value, sorted alphabetically by key.
    """

    use_config: dict = manager.get_config()

    table = Table(title="[bold green] (★‿★) Your current setup [/]", border_style="cyan")
    table.add_column("Key", style="cyan", justify="center")
    table.add_column("Value", style="green")

    for key, value in sorted(use_config.items()):
        table.add_row(str(key), str(value))

    console.print(table)

@config.command()
def reset():
    """
        Resets the configuration to its default values.

    Calls `ConfigManager.reset_config()` to restore the configuration
    to its initial state and start config setup.
    """
    manager.reset_config()

if __name__ == "__main__":
    cli()
            

