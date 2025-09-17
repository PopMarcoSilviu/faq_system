from text_completion.text_completer import TextCompleter
from vector_db.pg_vector_db import PGVectorDB



class QASystem:

    def __init__(self, vector_db: PGVectorDB, llm_completion: TextCompleter):
        self.vector_db = vector_db
        self.llm_completion = llm_completion
        
        self.high_confidence_threshold = 0.8
        self.low_confidence_threshold = 0.6


    def answer(self, query:str) -> dict[str,str]:

        results = self.vector_db.search(query=query, top_k=1)
        score = 0.0
        source = None
        matched_question = None
        answer = None

        if results:
            score = results[0]['score']

        # Use openai api call with no context
        if score <=self.low_confidence_threshold:
            source = 'openai'
            matched_question = 'N/A'
            answer = self.llm_completion.complete(query=query).content[0]['text'] # type: ignore
            
        if self.low_confidence_threshold < score < self.high_confidence_threshold:
            source = 'openai_with_local_context'
            matched_question = results[0]['content']
            answer = self.llm_completion.complete(query=query, context=answer).content[0]['text'] # type: ignore
        
        if score > self.high_confidence_threshold:
            source = 'local'
            matched_question = results[0]['content']
            answer = results[0]['metadata']['answer']
            

        output = {
            'source': source,
            'matched_question': matched_question,
            'answer': answer
        }

        return output

        

    
        