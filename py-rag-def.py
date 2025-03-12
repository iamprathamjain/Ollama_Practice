## 1. Ingest PDF Files
# 2. Extract Text from PDF Files and split into small chunks
# 3. Send the chunks to the embedding model
# 4. Save the embeddings to a vector database
# 5. Perform similarity search on the vector database to find similar documents
# 6. retrieve the similar documents and present them to the user
## run pip install -r requirements.txt to install the required packages

import psutil

process = psutil.Process()
print(f" Point 1 Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")


from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader

# doc_path = 'data\Brochure_Star_Comprehensive_Insurance_Policy_V_15_Web_633bcfcaaf.pdf'
doc_path = r"./data/India Salary Guide 2025 Michael Page India (15).pdf"
# doc_path = r"./data/notice_eng_je_01102020.pdf"
# doc_path = "./data/BOI.pdf"

# model= 'deepseek-r1:8b'
# model= 'gemma:2b'
model='llama3.2:latest'


# Local PDF file uploads
if doc_path:
   
    loader = UnstructuredPDFLoader(file_path=doc_path)


    data = loader.load()
    print("done loading....",type(data),type(loader))
    print(f" Point 2 reading pdf Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")
else:
    print("Upload a PDF file")


content = data[0].page_content

# print(content)

# ==== End of PDF Ingestion ====


# ==== Extract Text from PDF Files and Split into Small Chunks ====

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print(f" Point 3 splliting chunks Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")

print("done splitting....")

print(f"Number of chunks: {len(chunks)}")
# print(f"Example chunk: {chunks[0]}")


# ===== Add to vector database ===

import ollama

ollama.pull("nomic-embed-text")
persist_directory = "./chroma_db"


vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="simple-rag",

)
print("done adding to vector database....")
print(vector_db._persist_directory,'vector_db._persist_directory')  # If None, it's in-memory
print("Total Documents:", vector_db._collection.count())
print(f" Point 4  adding to vector database  Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")


## === Retrieval ===

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

# set up our model to use
llm = ChatOllama(model=model)


QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
    different versions of the given user question to retrieve relevant documents from
    a vector database. By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}""",
)


retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
)


# RAG prompt
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

res = chain.invoke(input=("what is the document about in 300 words?",))
# res = chain.invoke(input=("explain me about the tax benifit as a CA with an example ",))
# res = chain.invoke(
#     input=("what are the main points as a business owner I should be aware of?",)
# )
# res = chain.invoke(input=("how to report BOI?",))

print(res)