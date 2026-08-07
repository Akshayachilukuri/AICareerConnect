import os
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from app.services.stt_service import STTService
from app.services.tts_service import TTSService

voice_bp = Blueprint('voice', __name__)
stt_service = STTService()
tts_service = TTSService()

@voice_bp.route('/stt', methods=['POST'])
def speech_to_text():
    """
    Speech-to-Text Endpoint.
    Receives an uploaded audio file (or audio blob from microphone recorder),
    transcribes it, and returns the recognized text string.
    """
    if 'audio' not in request.files:
        # If text fallback or raw JSON is posted
        data = request.get_json() or {}
        raw_text = data.get('transcription', '')
        if raw_text:
            return jsonify({"success": True, "text": raw_text, "engine": "client_speech_recognition"})
        return jsonify({"error": "No audio file or text provided"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "Empty audio filename"}), 400

    filename = secure_filename(audio_file.filename)
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(upload_path)

    # Process STT
    result = stt_service.transcribe_audio_file(upload_path)
    
    # Cleanup file after processing
    try:
        if os.path.exists(upload_path):
            os.remove(upload_path)
    except Exception:
        pass

    return jsonify(result)

@voice_bp.route('/tts', methods=['POST'])
def text_to_speech():
    """
    Text-to-Speech Endpoint.
    Receives JSON containing text, synthesizes an MP3 audio file using TTSService,
    and returns the audio/mpeg media stream to the client.
    """
    data = request.get_json() or {}
    text = data.get('text', '').strip()

    if not text:
        return jsonify({"error": "Text payload is required for speech synthesis"}), 400

    audio_bytes = tts_service.text_to_speech_mp3(text)
    
    if not audio_bytes:
        return jsonify({"error": "Failed to synthesize speech"}), 500

    import io
    return send_file(
        io.BytesIO(audio_bytes),
        mimetype="audio/mpeg",
        as_attachment=False,
        download_name="speech.mp3"
    )
