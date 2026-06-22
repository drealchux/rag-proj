import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from get_vector_db import get_vector_db

LLM_MODEL = os.getenv('LLM_MODEL')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

def get_prompt():
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI assistant. Generate five reworded versions of the user question
        to improve document retrieval. Original question: {question}""",
    )
    template = "Answer the question based ONLY on this context:\n{context}\nQuestion: {question}"
    prompt = ChatPromptTemplate.from_template(template)
    return QUERY_PROMPT, prompt

def query(input):
    if input:
        llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_HOST)
        db = get_vector_db()

        QUERY_PROMPT, prompt = get_prompt()
        query_chain = QUERY_PROMPT | llm | StrOutputParser()
        variants_raw = query_chain.invoke({"question": input})

        variants = [input] + [q.strip() for q in variants_raw.split("\n") if q.strip()]

        retriever = db.as_retriever(search_kwargs={"k": 3})
        seen = set()
        docs = []
        for q in variants[:4]:
            for doc in retriever.invoke(q):
                if doc.page_content not in seen:
                    seen.add(doc.page_content)
                    docs.append(doc)

        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"context": docs, "question": input})
    return None