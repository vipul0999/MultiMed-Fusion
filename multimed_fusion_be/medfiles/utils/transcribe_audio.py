def transcribe_audio_to_text(path: str) -> str:
    """
    Transcribe audio to text using faster-whisper (optimized & lightweight).
    Supports: MP3, WAV, M4A, OGG, FLAC, OPUS
    Returns empty string if transcription fails.
    """
    try:
        from faster_whisper import WhisperModel

        # Use 'base' model for fast processing on normal laptops
        # Change to 'small', 'medium' for better accuracy but slower
        model = WhisperModel("base", device="cpu", compute_type="int8")

        segments, info = model.transcribe(path, language="en")

        # Collect all transcribed text
        text_parts = []
        for segment in segments:
            if segment.text.strip():
                text_parts.append(segment.text.strip())

        return "\n".join(text_parts).strip()
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""
