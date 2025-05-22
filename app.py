import streamlit as st
from rag_core import get_transcript_from_url
from dotenv import load_dotenv
import os

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.output_parsers import StructuredOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

# UI Setup
st.set_page_config(page_title="Talk to Your YouTube Video")
st.title("🎙️ Talk to Your YouTube Video")

# Step 1: YouTube URL input
url = st.text_input("📺 Enter the YouTube video URL:")

if url:
    st.success(f"URL received: {url}")

    # Step 2: Language selection
    language = st.selectbox("🌐 Select the language of the video:", ["English", "Hindi"])
    lang_code = {"English": "en", "Hindi": "hi"}[language]

    # Step 3: Check if transcript & vector store are already in session
    if "vector_ready" not in st.session_state or st.session_state.get("url_processed") != url:
        with st.spinner("📄 Fetching and processing transcript..."):
            try:
                # Transcript
                transcript_list = get_transcript_from_url(url, lang_code)
                transcript = " ".join(x['text'] for x in transcript_list)
                st.session_state.transcript = transcript

                # Split into chunks
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = splitter.create_documents([transcript])

                # Embeddings & vector store
                embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                vector_store = FAISS.from_documents(chunks, embedding_model)
                st.session_state.retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

                # Mark ready
                st.session_state.vector_ready = True
                st.session_state.url_processed = url
                st.success("Transcript processed successfully!")

            except Exception as e:
                st.error(f"❌ Failed to fetch transcript: {e}")
                st.stop()

    # Step 4: Ask question
    if st.session_state.get("vector_ready"):
        query = st.text_input("💬 Ask a question about the video:")

        if query:
            # LLM & Chain
            load_dotenv()
            api_key = os.getenv("GROQ_API_KEY")
            model = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)

            def format_docs(retrieved_docs):
                return "\n\n".join(doc.page_content for doc in retrieved_docs)

            prompt = PromptTemplate(
                template="""
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, just say you don't know.

{context}
Question: {question}
""",
                input_variables=['context', 'question']
            )

            parallel_chain = RunnableParallel({
                'context': st.session_state.retriever | RunnableLambda(format_docs),
                'question': RunnablePassthrough()
            })

            #parser = StructuredOutputParser()
            main_chain = parallel_chain | prompt | model 

            with st.spinner("🤖 Generating answer..."):
                try:
                    result = main_chain.invoke(query)
                    st.markdown("### 🧠 Answer:")
                    st.success(result.content)
                except Exception as e:
                    st.error(f"⚠️ Error generating answer: {e}")
else:
    st.warning("📌 Please paste a YouTube video URL above to begin.")
