import os
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_core.messages import convert_to_messages

MODEL = 'gpt-4o-mini'
CHROMA_COLLECTION_NAME = 'notion_notes'
CHROMA_DB_NAME = 'personal_vector_db'

load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
    
# Initialize Chroma vector store
vectorstore = Chroma(
    collection_name=CHROMA_COLLECTION_NAME,
    embedding_function=OpenAIEmbeddings(),
    persist_directory=CHROMA_DB_NAME
)

# create a new Chat with OpenAI
llm = ChatOpenAI(temperature=0.7, model_name=MODEL)

# the retriever is an abstraction over the VectorStore that will be used during RAG
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# putting it together: set up the conversation chain with the GPT 3.5 LLM and the vector store
conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

def message_text(content):
    """Gradio 6 stores message content as a list of parts; keep only the text."""
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") for part in content if part.get("type") == "text")

def chat(question, history):
    # Gradio passes this session's prior messages; keep only what LangChain needs
    chat_history = convert_to_messages(
        [{"role": m["role"], "content": message_text(m["content"])} for m in history]
    )
    result = conversation_chain.invoke({"question": question, "chat_history": chat_history})
    return result["answer"]

view = gr.ChatInterface(chat).launch(inbrowser=True)
