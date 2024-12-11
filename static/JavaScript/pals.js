const messageInput = document.querySelector('textarea');
const sendButton = document.querySelector('button');
const chatMessages = document.querySelector('.chat-messages');

sendButton.addEventListener('click', () => {
  const message = messageInput.value;
  if (message.trim() !== '') {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', 'user');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    messageInput.value = '';
  }
});

const textarea = document.getElementById('myTextarea');

textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = (textarea.scrollHeight) + 'px';
});

function clearTextArea() {
  document.getElementById("myTextArea").value = "";
}
