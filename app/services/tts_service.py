import os
import io

class TTSService:
    """Service layer handling Text-to-Speech (TTS) voice generation."""

    def text_to_speech_mp3(self, text, lang='en'):
        """Converts text into synthesized MP3 audio byte stream using gTTS."""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception as e:
            print(f"TTS Generation Exception: {e}")
            return None
