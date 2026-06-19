import os
from typing import Iterable
from src.prompt import groq_prompt_en
from dotenv import load_dotenv
from groq import Groq, GroqError
from colorama import Style, Fore, init
from groq.types.chat import ChatCompletionMessageParam

init(autoreset=True)
load_dotenv()

def generate_response(question: str, context: str)-> str:
    ''''
        Generate response with groq llm model using API KEY
    @question: A question about documents content.
    @context: The best answer return buy the search in vector_db
    '''
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        model = str(os.getenv('GROQ_LLM_MODEL'))

        test_messages: Iterable[ChatCompletionMessageParam] = [
            {"role": "system", "content": groq_prompt_en},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"}
        ]

        ''''Process of response generation'''
        completion = client.chat.completions.create(
            model=model,
            messages=test_messages,
            max_tokens=1024,
            temperature=0.1
        )

        response = completion.choices[0].message.content
        if not response:
            return ''
        return response.strip()

    except GroqError as error:
        print(Fore.RED + f'[GROQ ERROR]: An groq exception has leved, {error}' + Style.RESET_ALL)
        return ''