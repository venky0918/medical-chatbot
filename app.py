from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt

app = Flask(__name__)

# Load environment variables
load_dotenv()
os.environ["PINECONE_API_KEY"] = os.getenv('PINECONE_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv('GEMINI_API_KEY')

# Load embeddings & retriever
embeddings = download_hugging_face_embeddings()
docsearch = PineconeVectorStore.from_existing_index(
    index_name="medical-chatbot",
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Chat model
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt setup
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])
question_answer_chain = create_stuff_documents_chain(chat_model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form.get("msg", "").strip()
    if not user_msg:
        return "Please enter a message."

    try:
        response = rag_chain.invoke({"input": user_msg})
        return str(response.get("answer", "Sorry, I couldn't find an answer."))
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
