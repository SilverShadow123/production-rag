# import os
#
# from langchain_chroma import Chroma
# from langchain_classic.retrievers import EnsembleRetriever
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.retrievers import BM25Retriever
# from langchain_core.documents import Document
#
# from dotenv import load_dotenv
# from oauthlib.openid.connect.core.grant_types import hybrid
#
# load_dotenv()
#
# embeddings = OpenAIEmbeddings(
#     model="openai/text-embedding-3-small",
#     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
#     openai_api_base="https://openrouter.ai/api/v1",
# )
#
# documents = [
#     Document(
#         page_content='Product SKU-7742X is our flagship router. It supports'
#                      'gigabit speeds and advanced QoS features.',
#         metadata={'type': 'product'}
#     ),
#
#     Document(
#         page_content='For network connectivity issues, first check the '
#                      'ethernet cable and router status lights.',
#         metadata={'type': 'troubleshooting'}
#     ),
#
#     Document(
#         page_content='Error code E_CONN_REFUSED indicates the server '
#                      'rejected the connection. Check firewall settings.',
#         metadata={'type': 'error'}
#     ),
#     Document(
#         page_content='The authentication process requires valid credentials. '
#                      'Use 0Auth2 for secure API access.',
#         metadata={'type': 'auth'}
#     ),
#     Document(
#         page_content='Router configuration guide: Access the admin panel'
#                      'at 192.168.1.1 to modify settings.',
#         metadata={'type': 'config'}
#     ),
#     Document(
#         page_content='WCAG 2.1 compliance requires all images to have '
#                      'alt text and sufficient color contrast.',
#         metadata={'type': 'compliance'}
#     ), ]
#
# print(f'Loaded {len(documents)} documents')
#
# def rebuild_bm25():
#     global bm25_retriever
#     global ensemble_retriever
#
#     print("Rebuilding BM25...")
#
#     bm25_retriever = BM25Retriever.from_documents(
#         documents,
#         k=3
#     )
#
#     ensemble_retriever = EnsembleRetriever(
#         retrievers=[
#             bm25_retriever,
#             vector_retriever
#         ],
#         weights=[0.5, 0.5]
#     )
#
# vectorstore = Chroma.from_documents(
#     documents,
#     embeddings,
#     collection_name="hybrid_test"
# )
# vector_retriever = vectorstore.as_retriever(
#     search_kwargs={
#         "k": 3
#     }
# )
#
# bm25_retriever = BM25Retriever.from_documents(
#     documents,
#     k=3
# )
# ensemble_retriever = EnsembleRetriever(
#     retrievers=[bm25_retriever, vector_retriever],
#     weights=[0.5, 0.5]
# )
#
# def test_query(query, name, retriever):
#     '''Test a query and show results'''
#     results = retriever. invoke(query)
#     print(f'\\n{name} - Query: \"{query}\"')
#     for i, doc in enumerate(results [:3] ) :
#         preview = doc.page_content [: 80] + ' ... '
#         print(f' {i+1}. {preview}')
#     return results
#
# test_queries = [
# 'SKU-7742X specifications',
# 'E_CONN_REFUSED error',
# 'How do I authenticate?',
# 'WCAG compliance',
# 'router configuration',
# ]
#
# for query in test_queries:
#     vector_results = test_query(query, 'Vector', vector_retriever)
#     bm25_results = test_query(query, 'BM25', bm25_retriever)
#     hybrid_results = test_query(query, 'Ensemble', ensemble_retriever)
#
#
# import os
#
# from dotenv import load_dotenv
#
# from langchain_core.documents import Document
# from langchain_openai import OpenAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_community.retrievers import BM25Retriever
# from langchain_classic.retrievers import EnsembleRetriever
#
# load_dotenv()
#
# # ---------------------------
# # Embedding Model
# # ---------------------------
#
# embeddings = OpenAIEmbeddings(
#     model="openai/text-embedding-3-small",
#     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
#     openai_api_base="https://openrouter.ai/api/v1",
# )
#
# # ---------------------------
# # Documents
# # ---------------------------
#
# documents = [
#     Document(
#         page_content="Product SKU-7742X is our flagship router. It supports gigabit speeds and advanced QoS features.",
#         metadata={"type": "product"},
#     ),
#     Document(
#         page_content="For network connectivity issues, first check the ethernet cable and router status lights.",
#         metadata={"type": "troubleshooting"},
#     ),
#     Document(
#         page_content="Error code E_CONN_REFUSED indicates the server rejected the connection.",
#         metadata={"type": "error"},
#     ),
# ]
#
# print(f"Loaded {len(documents)} documents")
#
# # ---------------------------
# # Vector Store
# # ---------------------------
#
# vectorstore = Chroma.from_documents(
#     documents=documents,
#     embedding=embeddings,
#     collection_name="hybrid_demo",
# )
#
# vector_retriever = vectorstore.as_retriever(
#     search_kwargs={"k": 3}
# )
#
# # ---------------------------
# # Build BM25
# # ---------------------------
#
# bm25_retriever = BM25Retriever.from_documents(
#     documents,
#     k=3,
# )
#
# # ---------------------------
# # Build Ensemble
# # ---------------------------
#
# ensemble_retriever = EnsembleRetriever(
#     retrievers=[bm25_retriever, vector_retriever],
#     weights=[0.5, 0.5],
# )
#
# # ============================================================
# # Rebuild Function
# # ============================================================
#
# def rebuild_bm25():
#     global bm25_retriever
#     global ensemble_retriever
#
#     print("\nRebuilding BM25 Index...\n")
#
#     # Build NEW BM25 index
#     bm25_retriever = BM25Retriever.from_documents(
#         documents,
#         k=3,
#     )
#
#     # Build NEW Ensemble
#     ensemble_retriever = EnsembleRetriever(
#         retrievers=[bm25_retriever, vector_retriever],
#         weights=[0.5, 0.5],
#     )
#
# # ============================================================
# # Helper Function
# # ============================================================
#
# def search(query):
#     print(f"\nQuery: {query}")
#
#     docs = ensemble_retriever.invoke(query)
#
#     for i, doc in enumerate(docs, 1):
#         print(f"{i}. {doc.page_content}")
#
# # ============================================================
# # BEFORE ADDING NEW DOCUMENT
# # ============================================================
#
# search("WiFi 7 router")
#
# # ============================================================
# # NEW DOCUMENT ARRIVES
# # ============================================================
#
# new_doc = Document(
#     page_content="Our latest WiFi 7 router supports 10Gbps speeds and WPA3 security.",
#     metadata={"type": "product"},
# )
#
# print("\nAdding new document...\n")
#
# # Step 1
# documents.append(new_doc)
#
# # Step 2
# vectorstore.add_documents([new_doc])
#
# # Step 3
# rebuild_bm25()
#
# # ============================================================
# # AFTER REBUILD
# # ============================================================
#
# search("WiFi 7 router")

import os
from typing import List

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

load_dotenv()


class HybridRetriever:

    def __init__(
        self,
        documents: List[Document],
        bm25_weight: float = 0.5,
        k: int = 4,
    ):

        self.k = k
        self.bm25_weight = bm25_weight

        # Embedding model
        self.embeddings = OpenAIEmbeddings(
            model="openai/text-embedding-3-small",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
        )

        # Vector Database
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name="hybrid_demo",
        )

        self.vector_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.k}
        )

        # Build BM25
        self._rebuild_bm25()

    # ----------------------------------------
    # Internal function
    # ----------------------------------------
    def _rebuild_bm25(self):

        print("Rebuilding BM25 Index...")

        all_docs = self.vectorstore.get()

        bm25_docs = [
            Document(page_content=text)
            for text in all_docs["documents"]
        ]

        self.bm25_retriever = BM25Retriever.from_documents(
            bm25_docs,
            k=self.k,
        )

        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[
                self.bm25_retriever,
                self.vector_retriever,
            ],
            weights=[
                self.bm25_weight,
                1 - self.bm25_weight,
            ],
        )

    # ----------------------------------------
    # Add new documents
    # ----------------------------------------
    def add_documents(self, documents: List[Document]):

        print(f"\nAdding {len(documents)} new document(s)...")

        # Update Vector DB
        self.vectorstore.add_documents(documents)

        # Rebuild BM25
        self._rebuild_bm25()

    # ----------------------------------------
    # Search
    # ----------------------------------------
    def search(self, query: str):

        return self.ensemble_retriever.invoke(query)


# ===================================================
# Initial Documents
# ===================================================

documents = [

    Document(
        page_content="Product SKU-7742X is our flagship router with gigabit speeds.",
        metadata={"type": "product"},
    ),

    Document(
        page_content="Router configuration guide. Login to 192.168.1.1",
        metadata={"type": "config"},
    ),

    Document(
        page_content="Error code E_CONN_REFUSED means the server rejected the connection.",
        metadata={"type": "error"},
    ),
]

# ===================================================
# Create Retriever
# ===================================================

retriever = HybridRetriever(
    documents=documents,
    bm25_weight=0.5,
    k=3,
)

# ===================================================
# Search Before Adding New Document
# ===================================================

print("\nBEFORE ADDING DOCUMENT\n")

results = retriever.search("WiFi 7 router")

for doc in results:
    print("-", doc.page_content)

# ===================================================
# Add New Document
# ===================================================

new_docs = [

    Document(
        page_content="Our newest WiFi 7 router supports WPA3 and 10Gbps Ethernet.",
        metadata={"type": "product"},
    )

]

retriever.add_documents(new_docs)

# ===================================================
# Search Again
# ===================================================

print("\nAFTER REBUILD\n")

results = retriever.search("WiFi 7 router")

for doc in results:
    print("-", doc.page_content)