from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from services import get_transcript

def chunk_transcript(processed_transcript, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(processed_transcript)

def initialize_groq_llm():
    return ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.5,
        max_tokens=900
    )

def setup_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

def create_faiss_index(chunks, embedding_model):
    return FAISS.from_texts(chunks, embedding_model)

def retrieve(query, faiss_index, k=7):
    return faiss_index.similarity_search(query, k=k)

def create_summary_prompt():
    template = """You are an AI assistant tasked with summarizing YouTube video transcripts. Provide concise, informative summaries that capture the main points of the video content.

Instructions:
1. Summarize the transcript in a single concise paragraph.
2. Ignore any timestamps in your summary.
3. Focus on the spoken content of the video.

Please summarize the following YouTube video transcript:

{transcript}"""
    return PromptTemplate(input_variables=["transcript"], template=template)

def create_qa_prompt_template():
    qa_template = """You are an expert assistant providing detailed answers based on the following video content.

Relevant Video Context: {context}

Based on the above context, please answer the following question:
Question: {question}"""
    return PromptTemplate(input_variables=["context", "question"], template=qa_template)

def generate_answer(question, faiss_index, k=7):
    relevant_context = retrieve(question, faiss_index, k=k)
    llm = initialize_groq_llm()
    prompt_template = create_qa_prompt_template()
    
    qa_chain = prompt_template | llm
    response = qa_chain.invoke({"context": relevant_context, "question": question})
    return response.content

def summarize_video_from_text(processed_transcript):
    llm = initialize_groq_llm()
    summary_prompt = create_summary_prompt()
    
    summary_chain = summary_prompt | llm
    response = summary_chain.invoke({"transcript": processed_transcript})
    return response.content
    
def answer_question(video_url, user_question, faiss_index=None):
    if not video_url:
        return "Please provide a valid YouTube URL.", None
    if not user_question:
        return "Please provide a valid question.", None
        
    if faiss_index is None:
        processed_transcript = get_transcript(video_url)
        if not processed_transcript:
            return "No transcript available. Please ensure English captions are enabled.", None
        chunks = chunk_transcript(processed_transcript)
        embedding_model = setup_embedding_model()
        faiss_index = create_faiss_index(chunks, embedding_model)
        
    answer = generate_answer(user_question, faiss_index)
    return answer, faiss_index