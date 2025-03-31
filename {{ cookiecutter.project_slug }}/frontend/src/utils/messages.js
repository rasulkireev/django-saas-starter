// static/js/utils/messages.js
export function showMessage(message, type = 'error') {
  const messagesContainer = document.querySelector('.messages-container') || createMessagesContainer();

  const messageId = Date.now();
  const messageHTML = `
    <div data-reveal-target="item" data-message-id="${messageId}" class="rounded-lg border ${type === 'error' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'} p-4 shadow-sm transition-all duration-300 ease-in-out opacity-0 transform translate-x-full max-w-sm">
      <div class="flex items-start">
        <div class="flex-shrink-0 mr-3">
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <circle class="text-gray-200" stroke-width="2" stroke="currentColor" fill="transparent" r="10" cx="12" cy="12"/>
            <circle class="${type === 'error' ? 'text-red-600' : 'text-green-600'}" stroke-width="2" stroke="currentColor" fill="transparent" r="10" cx="12" cy="12" data-timer-circle/>
          </svg>
        </div>
        <div class="flex-grow">
          <p class="text-sm ${type === 'error' ? 'text-red-800' : 'text-green-800'}">
            ${message}
          </p>
        </div>
        <div class="flex-shrink-0 ml-3">
          <button onclick="this.closest('[data-reveal-target=item]').remove()" type="button" class="inline-flex justify-center items-center h-5 w-5 rounded-md ${type === 'error' ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'} focus:outline-none focus:ring-2 focus:ring-offset-2 ${type === 'error' ? 'focus:ring-red-500' : 'focus:ring-green-500'}">
            <span class="sr-only">Dismiss</span>
            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  `;

  messagesContainer.insertAdjacentHTML('beforeend', messageHTML);

  const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
  setTimeout(() => {
    messageElement.classList.remove('opacity-0', 'translate-x-full');
    startTimer(messageElement);
  }, 100);
}

function createMessagesContainer() {
  const container = document.createElement('div');
  container.className = 'fixed top-4 right-4 z-50 space-y-4 messages-container';
  document.body.appendChild(container);
  return container;
}

function startTimer(item) {
  const timerCircle = item.querySelector('[data-timer-circle]');
  const radius = 10;
  const circumference = 2 * Math.PI * radius;

  timerCircle.style.strokeDasharray = `${circumference} ${circumference}`;
  timerCircle.style.strokeDashoffset = circumference;

  let progress = 0;
  const interval = setInterval(() => {
    if (progress >= 100) {
      clearInterval(interval);
      hideMessage(item);
    } else {
      progress++;
      const offset = circumference - (progress / 100) * circumference;
      timerCircle.style.strokeDashoffset = offset;
    }
  }, 50);
}

function hideMessage(item) {
  item.classList.add('opacity-0', 'translate-x-full');
  setTimeout(() => {
    item.remove();
  }, 300);
}
