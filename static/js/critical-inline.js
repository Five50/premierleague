// Critical inline JavaScript - Only what's needed for initial render
// This should be inlined in the HTML to prevent render blocking

// Prevent FOUC (Flash of Unstyled Content) for theme switching
(function() {
    // Check for saved theme preference or default to 'light'
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.classList.add(theme);
})();

// Critical mobile menu functionality
function initMobileMenu() {
    const button = document.getElementById('mobile-menu-button');
    const menu = document.getElementById('mobile-menu');
    const openIcon = document.getElementById('menu-open');
    const closeIcon = document.getElementById('menu-close');
    
    if (button && menu) {
        button.addEventListener('click', function() {
            const isOpen = !menu.classList.contains('hidden');
            menu.classList.toggle('hidden');
            openIcon?.classList.toggle('hidden');
            closeIcon?.classList.toggle('hidden');
            button.setAttribute('aria-expanded', !isOpen);
        });
    }
}

// Run critical functions immediately
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileMenu);
} else {
    initMobileMenu();
}