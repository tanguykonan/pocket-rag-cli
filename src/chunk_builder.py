import os
from colorama import Style, Fore, init

init(autoreset=True)


def load_and_chunk_file(file_path: str, chunk_size: int = 150):
    """
        The small function witch cutting file content in
    chunk list.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(Fore.RED + f'[ERROR]: File {file_path} does not exist !' + Style.RESET_ALL)
    
    if os.path.getsize(file_path) <= 500:
        print(Fore.RED + f"[WARNING]: File {file_path} does not have valid size !" + Style.RESET_ALL)
        exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    words = file_content.split() # divide file_content to obtain words list 
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i + chunk_size] # cut the words list into portions
        '''
            Example:
                len(words) = 1000
                - first round (chunk 1): chunk_words = words[0 : 0 + 150]  => (0-149) words
                - second round (chunk 2): chunk_words = words[150 : 150 + 150] => (150-299) words
                - etc...
        '''
        chunk_text = ' '.join(chunk_words)
        chunks.append(chunk_text)

    return chunks