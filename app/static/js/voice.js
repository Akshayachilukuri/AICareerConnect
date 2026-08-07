// Voice Controller handling Speech-to-Text (STT) mic capture and Text-to-Speech (TTS) playback
class VoiceManager {
  constructor() {
    this.recognition = null;
    this.isRecording = false;
    this.audioPlayer = new Audio();

    this.initSpeechRecognition();
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';
    } else {
      console.warn("Browser SpeechRecognition API not supported. Using server STT fallback.");
    }
  }

  startListening(onResultCallback, onEndCallback) {
    if (!this.recognition) {
      showToast("Speech Recognition not supported natively in this browser.", "warning");
      return;
    }

    this.isRecording = true;

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (onResultCallback) onResultCallback(transcript);
    };

    this.recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      this.isRecording = false;
      if (onEndCallback) onEndCallback();
    };

    this.recognition.onend = () => {
      this.isRecording = false;
      if (onEndCallback) onEndCallback();
    };

    this.recognition.start();
  }

  stopListening() {
    if (this.recognition && this.isRecording) {
      this.recognition.stop();
      this.isRecording = false;
    }
  }

  async speakText(text) {
    // 1. Try Browser Web Speech Synthesis for ultra-fast response
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel(); // Stop ongoing speech
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
      return;
    }

    // 2. Fallback to Flask backend TTS Endpoint (/api/voice/tts)
    try {
      const response = await fetch('/api/voice/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      });

      if (response.ok) {
        const blob = await response.blob();
        const audioUrl = URL.createObjectURL(blob);
        this.audioPlayer.src = audioUrl;
        this.audioPlayer.play();
      }
    } catch (error) {
      console.error("TTS backend fetch failed:", error);
    }
  }
}

window.voiceManager = new VoiceManager();
