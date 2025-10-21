document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const messages = document.getElementById('messages');

  if (!form || !input || !messages) {
    console.error('Chat elements not found:', { form, input, messages });
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = (input.value || '').trim();
    if (!text) return;

    appendMessage('You', text);
    input.value = '';

    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({ detail: resp.statusText }));
        appendMessage('Error', err.detail || 'Request failed');
        return;
      }

      const data = await resp.json();
      appendMessage('Agent', data.response ?? JSON.stringify(data));
    } catch (err) {
      appendMessage('Error', err?.message ?? String(err));
    }
  });

  function appendMessage(who, text) {
    const el = document.createElement('div');
    el.className = 'message';
    el.innerHTML = `<strong>${escapeHtml(who)}:</strong> ${escapeHtml(text)}`;
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }
});
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const messages = document.getElementById('messages');

  if (!form || !input || !messages) {
    console.error('Chat elements not found: ', { form, input, messages });
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value ? input.value.trim() : '';
    if (!text) return;

    appendMessage('You', text);
    input.value = '';

    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (!resp.ok) {
        let err = await resp.json().catch(() => ({ detail: resp.statusText }));
        appendMessage('Error', err.detail || 'Request failed');
        return;
      }

      const data = await resp.json();
      appendMessage('Agent', data.response ?? JSON.stringify(data));
    } catch (err) {
      appendMessage('Error', err?.message ?? String(err));
    }
  });

  function appendMessage(who, text) {
    const el = document.createElement('div');
    el.className = 'message';
    el.innerHTML = `<strong>${escapeHtml(who)}:</strong> ${escapeHtml(text)}`;
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>\const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatWindow = document.getElementById('chat-window');

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const userMessage = chatInput.value;
    appendMessage('You', userMessage);
    chatInput.value = '';

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    });

    if (response.ok) {
        const data = await response.json();
        appendMessage('Bot', data.response);
    } else {
        appendMessage('Bot', 'Error: Unable to get response.');
    }
});

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerText = `${sender}: ${message}`;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}