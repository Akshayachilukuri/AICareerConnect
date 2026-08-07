// AI Career Chat & Audio Toggle Controller
document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const micBtn = document.getElementById('micBtn');

  if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (!message) return;

      chatInput.value = '';
      appendMessage('user', message);
      await sendChatMessage(message);
    });
  }

  if (micBtn) {
    micBtn.addEventListener('click', () => {
      if (window.voiceManager.isRecording) {
        window.voiceManager.stopListening();
        micBtn.classList.remove('recording');
        micBtn.style.color = 'var(--text-secondary)';
      } else {
        micBtn.classList.add('recording');
        micBtn.style.color = 'var(--danger)';
        showToast("Listening... Speak your career question.", "info");

        window.voiceManager.startListening(
          (transcript) => {
            chatInput.value = transcript;
            appendMessage('user', transcript, 'voice');
            sendChatMessage(transcript, 'voice');
          },
          () => {
            micBtn.classList.remove('recording');
            micBtn.style.color = 'var(--text-secondary)';
          }
        );
      }
    });
  }
});

async function sendChatMessage(messageText, msgType = 'text') {
  const typingIndicator = appendTypingIndicator();

  try {
    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: messageText, message_type: msgType })
    });

    const data = await response.json();
    typingIndicator.remove();

    if (data.success) {
      appendMessage('assistant', data.reply);
      
      // Auto-read response if input was spoken
      if (msgType === 'voice') {
        window.voiceManager.speakText(data.reply);
      }
    } else {
      appendMessage('assistant', "Sorry, I ran into an issue generating guidance. Please try again.");
    }
  } catch (error) {
    typingIndicator.remove();
    console.error("Chat API error:", error);
    appendMessage('assistant', "Connection error. Please check your network or API settings.");
  }
}

function appendMessage(role, text, msgType = 'text') {
  const chatMessages = document.getElementById('chatMessages');
  if (!chatMessages) return;

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-bubble ${role}-bubble glass-card`;
  msgDiv.style.cssText = `
    margin-bottom: 1rem;
    max-width: 80%;
    align-self: ${role === 'user' ? 'flex-end' : 'flex-start'};
    background: ${role === 'user' ? 'rgba(99, 102, 241, 0.25)' : 'var(--card-bg)'};
    border-left: 3px solid ${role === 'user' ? 'var(--accent-cyan)' : 'var(--accent-violet)'};
  `;

  const metaText = msgType === 'voice' ? ' 🎙️ (Voice Query)' : '';
  msgDiv.innerHTML = `
    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem;">
      ${role === 'user' ? 'You' : 'Mistral AI Career Coach'}${metaText}
    </div>
    <div style="white-space: pre-wrap; line-height: 1.5;">${escapeHtml(text)}</div>
    ${role === 'assistant' ? `<button onclick="window.voiceManager.speakText(\`${escapeHtml(text).replace(/`/g, '')}\`)" style="margin-top: 0.5rem; background: transparent; border: none; color: var(--accent-cyan); cursor: pointer; font-size: 0.8rem;">🔊 Listen</button>` : ''}
  `;

  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendTypingIndicator() {
  const chatMessages = document.getElementById('chatMessages');
  const indicator = document.createElement('div');
  indicator.className = 'chat-bubble assistant-bubble glass-card';
  indicator.style.cssText = 'margin-bottom: 1rem; max-width: 80%; align-self: flex-start; font-style: italic; color: var(--text-secondary);';
  indicator.innerText = "Mistral AI is thinking...";
  chatMessages.appendChild(indicator);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return indicator;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.innerText = text;
  return div.innerHTML;
}
