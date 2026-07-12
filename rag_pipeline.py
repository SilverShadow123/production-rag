from langchain.chat_models import init_chat_model
from langchain_classic.agents.agent_toolkits import vectorstore
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.output_parsers import  StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import tempfile
import os

load_dotenv()

embeddings_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
)

KNOWLEDGE_BASE = """# LangChain Framework

LangChain is a framework for developing applications powered by language models. It was created by Harrison Chase in October 2022.

## Core Components

1. **Models**: LangChain supports various LLM providers including OpenAI, Anthropic, and local models.

2. **Prompts**: Templates for structuring inputs to language models.

3. **Chains**: Sequences of calls to models and other components.

4. **Agents**: Systems that use LLMs to determine which actions to take.

5. **Memory**: Components for persisting state between chain/agent calls.

## LangGraph

LangGraph is a library for building stateful, multi-actor applications. Key features:
- State management
- Cycles and loops
- Human-in-the-loop
- Persistence

## Pricing

LangChain itself is open source and free. LangSmith (the observability platform) has a free tier and paid plans starting at $39/month.

## Getting Started

Install with: pip install langchain langchain-openai
Create your first chain in under 10 lines of code.
"""

llm = init_chat_model(model='openai/gpt-4o-mini', model_provider='openrouter')

def create_kb():
    """Create a knowledge base from a list of documents."""

    spliter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    doc= Document(page_content=KNOWLEDGE_BASE, metadata={"source": "langchain_knowledge_base.md"})

    chunks = spliter.split_documents([doc])

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        collection_name='langchain_knowledge_base',
    )
    return vector_store


def demo_basic_rag():
    vector_store = create_kb()
    retriver = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    llm = init_chat_model(model='openai/gpt-4o-mini',temperature=0.2, model_provider='openrouter')
    prompt = ChatPromptTemplate.from_template(
        """
 Answer the question based only on the following context:

 {context}

 Question: {question}

 Answer:


 Make sure to answer in a concise manner, 
 and if you don't know the answer, just say "I don't know."""
    )

    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    rag_chain = (
        {"context": retriver | format_docs, 'question': RunnablePassthrough()}
        |prompt
        |llm
        |StrOutputParser()
    )

    questions = [
        "What is LangChain?",
        "Who created LangChain?",
        "What is LangGraph used for?",
    ]

    print("Basic RAG Demo:\n")
    for q in questions:
        answer = rag_chain.invoke(q)
        print(f"Q: {q}")
        print(f"A: {answer}\n")


def demo_rag_with_sources():

    vectorstore = create_kb()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template(
        """
Answer the question based on the context below. Include which sources you used.

Context:
{context}

Question: {question}

Answer (include sources):"""
    )

    def format_docs_with_sources(docs):
        formatted = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "unknown")
            formatted.append(f"[{i+1}] {source}:\n{doc.page_content}")
        return "\n\n".join(formatted)

    rag_chain = (
        {
            "context": retriever | format_docs_with_sources,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("RAG with Sources:\n")
    answer = rag_chain.invoke("What are the core components of LangChain?")
    print(f"Q: What are the core components?\n")
    print(f"A: {answer}")



if __name__ == "__main__":
    # demo_basic_rag()
    demo_rag_with_sources()