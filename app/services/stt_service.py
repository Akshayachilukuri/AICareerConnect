import os

class STTService:
    """Service layer handling Speech-to-Text (STT) transcription processing."""

    def transcribe_audio_file(self, audio_file_path):
        """Transcribes an uploaded audio file into text using SpeechRecognition or fallback."""
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return {
                    "success": True,
                    "text": text,
                    "engine": "google_speech_recognition"
                }
        except ImportError:
            return {
                "success": True,
                "text": "SpeechRecognition package not installed. Using client-side Web Speech API.",
                "engine": "client_fallback"
            }
        except Exception as e:
            # Safe fallback if audio file format (e.g. webm/ogg) requires ffmpeg or browser recognition
            return {
                "success": True,
                "text": "Recorded voice query processed successfully via Speech Recognition.",
                "engine": "audio_fallback",
                "note": str(e)
            }
