import json
from groq import Groq
from pathlib import Path
from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console
from platformdirs import user_config_dir

console = Console()
'''Instantiation of the main object of the rich library'''

class ConfigManager:
    def __init__(self) -> None:
        self.app_name = "PocketRag"
        self.config_dir = Path(user_config_dir(self.app_name))
        self.config_file = self.config_dir / "config.json"

    def _default_config(self) -> dict:
        """
            Default config structure and values.
        """

        return {
            "groq_api_key":'',
            "groq_model":'',
            "chunk_size": 150,
            "top_n": 3
        }
    
    def _load_config(self) -> dict:
        """
            Config loader to return config values.
        """

        if not self.config_file.exists():
            return {}
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def _save_config(self, config: dict) -> None:
        """
            Save a new configuration in the path.
        @config: The config value.
        """

        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)

    def _is_valid_config(self, config: dict) -> bool:
        """
            Verified if is valid config.
        @config: The config value.
        """
        return bool(config.get("groq_api_key")) and bool(config.get("groq_model"))

    def _config_setup(self) -> dict:
        """
            Interactive first-time configuration matching PocketRag style.
        """
        try:
            config = self._default_config()
            console.print("[bold yellow] [POCKET-RAG]: (≧﹏ ≦) Hello, before to continue, I will help you to config me.[/]")
        
            while True:

                api_key = Prompt.ask("[bold cyan] [POCKET-RAG]: (¬‿¬) First, copy and paste your Groq API key here.[/]").strip()
                with console.status("[bold green] [POCKET-RAG]: (*^▽^*) Verifying API key with Groq... [/]"):
                    try:
                        client = Groq(api_key=api_key)
                        models = client.models.list()
                        break
                    except Exception:
                        console.print(" [POCKET-RAG]: {{{(>_<)}}} Sorry but this Groq API key is invalid. Try again ^^", style="bold red",)

            available_models = sorted([model.id for model in models.data])
            table = Table(title="[bold green] (★‿★) Available Groq Models [/]", border_style="cyan")
            table.add_column("Number", style="cyan", justify="center")
            table.add_column("Model", style="green")

            for idx, model_name in enumerate(available_models, start=1):
                table.add_row(str(idx), model_name)

            console.print(table)
            choice = Prompt.ask("[bold cyan] [POCKET-RAG]: (o(*￣︶￣*)o) Choose a model by entering its number[/]")
            selected_model = available_models[int(choice) - 1]

            console.print(" [POCKET-RAG]: (⌐■_■) Now, let's set up the retrieval settings (Press Enter for defaults)...", style="bold yellow")
        
            chunk_size = Prompt.ask("[bold cyan] [POCKET-RAG]: (¬‿¬) Enter chunk size[/]", default=str(config["chunk_size"]),)
            while not chunk_size.isdigit() or int(chunk_size) <= 0:
                console.print(  "[POCKET-RAG]: {{{(>_<)}}} Chunk size must be greater than 0.", style="bold yellow")
                chunk_size = Prompt.ask(
                    "[bold cyan] [POCKET-RAG]: (¬‿¬) Enter chunk size[/]",
                    default=str(config["chunk_size"]),
                )

            top_n = Prompt.ask("[bold cyan] [POCKET-RAG]: (¬‿¬) Enter Top N retrieved chunks[/]", default=str(config["top_n"]),)
            while not top_n.isdigit() or int(top_n) < 2:
                console.print(  "[POCKET-RAG]: {{{(>_<)}}} Top N must be at least 2.", style="bold yellow")
                top_n = Prompt.ask(
                    "[bold cyan] [POCKET-RAG]: (¬‿¬) Enter Top N retrieved chunks[/]",
                    default=str(config["top_n"]),
                )

            config["chunk_size"] = int(chunk_size)
            config["top_n"] = int(top_n)
            config["groq_api_key"] = api_key
            config["groq_model"] = selected_model

            self._save_config(config)

            console.print(" [POCKET-RAG]: (⌐■_■) Congratulations, The setup was a success !", style="bold green")
            return config
        
        except KeyboardInterrupt:
            exit(0)

    def get_config(self) ->  dict:
        """
            Get config value.
        This method call setup config method to the first query.
        """
        config = self._load_config()
        if not config or not self._is_valid_config(config):
            config = self._config_setup()
        
        return config
    
    def reset_config(self) -> dict:
        """
            Reset config and force reconfiguration.
        The default config is not usable.
        """
        
        self._save_config(self._default_config())

        return self._config_setup()