import streamlit as st
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

persist_directory = 'pdf_persist'
collection_name = 'pdf_collection'

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

chain = load_qa_chain(llm, chain_type="refine")

vectorstore = None


def main():
    # 配置界面
    st.set_page_config(page_title="PDF QA ChatBot",
                       page_icon=":robot:")

    st.header("LangChain pdf QA ChatBot")
    st.markdown('The source code for this app can be found in this GitHub repo: [https://github.com/vveizhang/chatPDF](https://github.com/vveizhang/chatPDF).')

    # 初始化
    # session_state是Streamlit提供的用于存储会话状态的功能
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.title("PDF Chatbot")

    with st.container():
        uploaded_files = st.file_uploader("Upload your PDF files", type="pdf", accept_multiple_files=True)
        if not uploaded_files:
            vectorstore = None
            st.write("Please upload your PDF files")

        else:
            paths = []
            docs = []
            for file in uploaded_files:
                path  = os.path.join('.', file.name)
                paths.append(path)
                with open(path, 'wb') as f:
                    f.write(file.getbuffer())
                    doc = PyMuPDFLoader(path)
                    docs.extend(doc.load())
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            split_docs = text_splitter.split_documents(docs)

            vectorstore = Chroma.from_documents(split_docs, embeddings, collection_name=collection_name, persist_directory=persist_directory)
            vectorstore.persist()

            st.write("Done")
        
    with st.container():
        question = st.text_input("Question")
        if vectorstore is not None and question is not None and question != "":
            docs = vectorstore.similarity_search(question,6,include_metadata =True)
            answer = chain.run(input_documents = docs, question = question)
            st.write(answer)


if __name__ == "__main__":
    main()






