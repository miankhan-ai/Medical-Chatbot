import os
import streamlit as st

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    # Check if path exists to avoid crash
    if not os.path.exists(DB_FAISS_PATH):
        return None
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def main():
    st.title("Ask Chatbot!")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.chat_input("Pass your prompt here")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # --- MOVED TEMPLATE HERE ---
        CUSTOM_PROMPT_TEMPLATE = """
        Use the pieces of information provided in the context to answer user's question.
        If you dont know the answer, just say that you dont know, dont try to make up an answer. 
        Dont provide anything out of the given context

        Context: {context}
        Question: {input}

        Start the answer directly. No small talk please.
        """

        try:
            vectorstore = get_vectorstore()
            if vectorstore is None:
                st.error("Failed to load the vector store")
                return # Stop execution if no DB

            # 1. Setup LLM
            GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
            GROQ_MODEL_NAME = "llama-3.1-8b-instant"
            
            llm = ChatGroq(
                model=GROQ_MODEL_NAME,
                temperature=0.5,
                max_tokens=1024,
                api_key=GROQ_API_KEY, # Fixed param name for some versions
            )

            # 2. Setup Prompt (Changed {question} to {input} to match retrieval chain expectation)
            prompt_template = PromptTemplate(
                template=CUSTOM_PROMPT_TEMPLATE, 
                input_variables=["context", "input"]
            )

            # 3. Create Chains (MUST BE DONE BEFORE INVOKING)
            combine_docs_chain = create_stuff_documents_chain(llm, prompt_template)
            
            retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
            rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

            # 4. Invoke Chain
            # Note: We removed the 'input()' function because that is for console, not Streamlit
            response = rag_chain.invoke({'input': prompt})
            
            result = response["answer"]
            
            st.chat_message('assistant').markdown(result)
            st.session_state.messages.append({'role': 'assistant', 'content': result})

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()