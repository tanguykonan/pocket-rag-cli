from typing import Iterable
from groq import Groq, GroqError
from colorama import Style, Fore
from src.prompt import groq_prompt
from groq.types.chat import ChatCompletionMessageParam

def generate_response(question: str, context: str, api: str, model: str)-> str:
    ''''
        Generate response with groq llm model using API KEY
    @question: A question about documents content.
    @context: The best answer return buy the search in vector_db.
    @api: The configured api key.
    @model: The configured model.
    '''

    try:
        client = Groq(api_key=api)

        query_messages: Iterable[ChatCompletionMessageParam] = [
            {"role": "system", "content": groq_prompt},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"}
        ]

        ''''Process of response generation'''
        completion = client.chat.completions.create(
            model=model,
            messages=query_messages,
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