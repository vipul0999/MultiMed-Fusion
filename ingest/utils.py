import os
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import magic
from pydub import AudioSegment
import speech_recognition as sr

def extract_text(file_path):
    mime_type = magic.from_file(file_path, mime=True)

    if mime_type == 'application/pdf':
        return extract_text_from_pdf(file_path)
    elif mime_type.startswith('image/'):
        return extract_text_from_image(file_path)
    elif mime_type.startswith('text/'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif mime_type.startswith('audio/'):
        return extract_text_from_audio(file_path)
    else:
        return ''

def extract_text_from_pdf(file_path):
    text = ''
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + '\n'
    except Exception as e:
        print(f"PDF parse error: {e}")
    return text

def extract_text_from_image(file_path):
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"OCR error: {e}")
        return ''

def extract_text_from_audio(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        audio.export("temp.wav", format="wav")
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
        os.remove("temp.wav")
        return text
    except Exception as e:
        print(f"Audio parse error: {e}")
        return ''
