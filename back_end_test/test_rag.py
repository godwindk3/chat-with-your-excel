import getpass
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, StateGraph
from typing import List, TypedDict
from langchain_chroma import Chroma

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    model_provider="google_genai",
)
# response = llm.invoke("Hello, how are you?")
# print(response.content)

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# vector_store = InMemoryVectorStore(embeddings)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

#### Tạo văn bản test

docs = [
    Document(
        page_content="Đây là văn bản test của tôi, Phong rất đẹp trai, cao 3m",
        metadata={"source": "local"}
    )
]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

_ = vector_store.add_documents(documents=all_splits)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Bạn là một trợ lý AI chuyên trả lời câu hỏi dựa trên ngữ cảnh đã cho."),
    ("human", "Ngữ cảnh:\n{context}\n\nCâu hỏi: {question}")
])

# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


response = graph.invoke({"question": "Thông tin về anh Phong"})
print(response["answer"])
