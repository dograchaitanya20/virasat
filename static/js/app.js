/**
 * Virasat (विरासत) - Main Client Script
 * Handles Theme Toggling, Glass Navbar, Search Palette, Toast Notifications, and Smooth Animations.
 */

// Initialize Theme from localStorage or system preference
(function initTheme() {
  const savedTheme = localStorage.getItem('virasat-theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
})();

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('virasat-theme', isDark ? 'dark' : 'light');
  window.dispatchEvent(new CustomEvent('theme-changed', { detail: { isDark } }));
}

// Navbar shrink & elevation on scroll
document.addEventListener('DOMContentLoaded', () => {
  const nav = document.getElementById('main-nav');
  if (nav) {
    const handleScroll = () => {
      if (window.scrollY > 40) {
        nav.classList.add('nav-scrolled');
      } else {
        nav.classList.remove('nav-scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // Keyboard shortcut for Global Search (Ctrl+K or Cmd+K)
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const searchModal = document.getElementById('global-search-modal');
      if (searchModal && window.Alpine) {
        Alpine.$data(searchModal).openModal();
      }
    }
  });

  // Reinitialize GSAP / GLightbox after HTMX swaps
  document.body.addEventListener('htmx:afterSwap', () => {
    if (window.initGLightbox) {
      window.initGLightbox();
    }
    if (window.ScrollTrigger) {
      ScrollTrigger.refresh();
    }
  });
});

// Toast Notification Helper
function showToast(message, type = 'info') {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) return;

  const toast = document.createElement('div');
  const bgColors = {
    success: 'bg-emerald-900/90 border-emerald-500 text-emerald-100',
    error: 'bg-rose-900/90 border-rose-500 text-rose-100',
    warning: 'bg-amber-900/90 border-amber-500 text-amber-100',
    info: 'bg-slate-900/90 border-amber-500/50 text-slate-100',
  };

  toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl border shadow-xl backdrop-blur-md text-sm transition-all duration-300 transform translate-y-4 opacity-0 ${bgColors[type] || bgColors.info}`;
  toast.innerHTML = `
    <span class="text-lg">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
    <span class="flex-1">${message}</span>
    <button onclick="this.parentElement.remove()" class="text-xs opacity-70 hover:opacity-100">&times;</button>
  `;

  toastContainer.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-4', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('opacity-0', '-translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
