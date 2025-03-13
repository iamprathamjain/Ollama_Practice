import time
import psutil
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ✅ Track memory usage
process = psutil.Process()
print(f"🔹 Initial Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")

# ✅ Load Existing ChromaDB
persist_directory = "./chroma_db"
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_db = Chroma(
    persist_directory=persist_directory, 
    embedding_function=embedding_model,
    collection_name="simple-rag"  # 🔥 Make sure this matches what you used during storage
)


print("✅ ChromaDB loaded successfully.")
print(f"🔹 Total Documents in DB: {vector_db._collection.count()}")

# ✅ Load LLM (You can switch models here)
llm = ChatOllama(model="llama3.2:latest")  # Switch to "deepseek-r1:8b" or "gemma:2b" if needed

# ✅ Define RAG Prompt
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

# ✅ Set up the RAG Chain (Retrieval + LLM Response)
chain = (
    {"context": vector_db.as_retriever(), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ✅ Ask a question and track response time
question = "Summarize the key points of the document in 300 words."

start_time = time.time()  # Start time tracking
response = chain.invoke(input=question)
end_time = time.time()  # End time tracking

# ✅ Print response and response time
print("\n🔹 **Response:**")
print(response)
print(f"\n⏱️ **Response Time:** {end_time - start_time:.2f} seconds")
print(f"🔹 Final Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")
