// Main Application Helper & Global Event Handlers
document.addEventListener('DOMContentLoaded', () => {
  console.log("⚡ AI Career Connect initialized.");
  
  // Highlight active link in sidebar
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});

// Toast notification helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast toast-${type} glass-card`;
  toast.style.cssText = `
    padding: 1rem 1.25rem;
    margin-top: 0.5rem;
    border-left: 4px solid ${type === 'success' ? '#10b981' : type === 'danger' ? '#ef4444' : '#06b6d4'};
    color: white;
    font-size: 0.9rem;
    animation: fadeIn 0.3s ease-in-out;
  `;
  toast.innerText = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 4000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column;';
  document.body.appendChild(container);
  return container;
}
