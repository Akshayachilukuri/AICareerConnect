import unittest
from app.services.mistral_service import MistralService
from app.services.stt_service import STTService
from app.services.tts_service import TTSService

class ServicesTestCase(unittest.TestCase):
    def test_mistral_fallback_service(self):
        mistral = MistralService(api_key="")
        response = mistral.generate_chat_response("What is Flask?")
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_mistral_resume_analysis(self):
        mistral = MistralService(api_key="")
        analysis = mistral.analyze_resume("Python developer with 5 years experience in Flask", "Flask Backend Engineer")
        self.assertIn("Match Score", analysis)

    def test_tts_service_generation(self):
        tts = TTSService()
        audio_bytes = tts.text_to_speech_mp3("Hello welcome to AI Career Connect")
        self.assertIsNotNone(audio_bytes)
        self.assertTrue(len(audio_bytes) > 0)

if __name__ == '__main__':
    unittest.main()
