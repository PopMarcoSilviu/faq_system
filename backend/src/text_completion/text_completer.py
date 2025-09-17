from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_core.messages.base import BaseMessage

class TextCompleter:
    def __init__(self) -> None:
        load_dotenv()
        model = os.getenv('TEXT_COMPLETION_MODEL', '')

        self.llm = ChatOpenAI(
            model = model,
            temperature=0.0,
            max_completion_tokens=1500,
            max_retries=2,
            timeout=60,
            reasoning={"effort":"low"},
            verbosity="low", 

        )

        self.prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            "You are a helpful assistant that answers questions. Keep asnwers short and don't ask additional questions, assume this is the entire information you will get.\n{context}",
        ),
        ("human", "{input}"),
        ])

        self.chain = self.prompt | self.llm

    def complete(self,query:str ,context:str|None=None) -> BaseMessage:

        if context:
            context = f"Here is information which might be helpful: {context}"
        else:
            context = ""

        answer =self.chain.invoke(
            {
                "context": context,
                "input" : query
            }   
        )

        return answer
    
