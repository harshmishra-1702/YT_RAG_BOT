import streamlit as st
from dotenv import load_dotenv
from services import get_transcript
from rag_engine import (
    summarize_video_from_text,
    chunk_transcript,
    setup_embedding_model,
    create_faiss_index,
    answer_question
)

# Load variables at layout start execution runtime
load_dotenv()

st.set_page_config(page_title="YouTube Transcript Q&A Bot", layout="wide")
st.title("📺 YouTube Video Transcript Q&A Assistant")
st.markdown("---")

if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
if "summary" not in st.session_state:
    st.session_state.summary = ""

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.header("🔗 Input Configuration")
    video_url = st.text_input("Paste YouTube Video URL here:", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("🚀 Fetch and Summarize Video", use_container_width=True):
        if video_url:
            with st.spinner("Analyzing video transcript and generating summary..."):
                try:
                    processed_transcript = get_transcript(video_url)
                    if processed_transcript:
                        st.session_state.summary = summarize_video_from_text(processed_transcript)
                        chunks = chunk_transcript(processed_transcript)
                        embedding_model = setup_embedding_model()
                        st.session_state.faiss_index = create_faiss_index(chunks, embedding_model)
                    else:
                        st.error("No transcript available. Unable to transcribe this video layout structure.")
                except Exception as pipeline_err:
                    st.error(f"System Pipeline Failure: {pipeline_err}")
        else:
            st.error("Please enter a valid YouTube URL first!")
            
    if st.session_state.summary:
        st.subheader("📝 Video Summary")
        st.info(st.session_state.summary)

with col2:
    st.header("💬 Ask Questions About the Video")
    user_question = st.text_input("Enter your question:", placeholder="What does the speaker say about...")
    
    if st.button("🔍 Get Answer", use_container_width=True):
        if not video_url:
            st.warning("Please configure a YouTube URL on the left side first.")
        elif not user_question:
            st.warning("Please type a question before submitting.")
        else:
            with st.spinner("Searching transcript context..."):
                try:
                    answer, updated_index = answer_question(
                        video_url=video_url, 
                        user_question=user_question, 
                        faiss_index=st.session_state.faiss_index
                    )
                    st.session_state.faiss_index = updated_index
                    st.subheader("💡 Answer:")
                    st.success(answer)
                except Exception as qa_err:
                    st.error(f"Execution Error: {qa_err}")