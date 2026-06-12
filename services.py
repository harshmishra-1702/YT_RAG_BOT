import os
import re
import yt_dlp
import assemblyai as aai



def get_video_id(url):    
    pattern = r'(?:v=|\/shorts\/|\/youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(url):
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    video_id = get_video_id(url)
    if not video_id:
        return None
        
    audio_template = f"{video_id}.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': audio_template,
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            actual_filename = ydl.prepare_filename(info)
            
        if not os.path.exists(actual_filename):
            return None
            
        transcriber = aai.Transcriber()
        transcript_response = transcriber.transcribe(actual_filename)
        
        if os.path.exists(actual_filename):
            os.remove(actual_filename)
            
        if transcript_response.status == aai.TranscriptStatus.error:
            raise Exception(f"AssemblyAI Processing Error: {transcript_response.error}")
            
        return transcript_response.text.strip()
        
    except Exception as e:
        try:
            for file in os.listdir('.'):
                if file.startswith(video_id):
                    os.remove(file)
        except:
            pass
        raise e