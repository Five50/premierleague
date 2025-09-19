/**
 * Main JavaScript file for Theme Development Project
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Theme Development Project loaded successfully!');
    
    // Initialize page functionality
    initializePageFeatures();
    initializeAnimations();
    initializeFormHandlers();
    initializeTabs();
});

/**
 * Initialize page features
 */
function initializePageFeatures() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize animations
 */
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe sections for animation
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });
}

/**
 * Initialize tab functionality
 */
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    if (tabButtons.length === 0) {
        return; // No tabs on this page
    }
    
    console.log('Initializing tabs:', tabButtons.length, 'buttons found');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const targetTab = this.getAttribute('data-tab');
            
            console.log('Tab clicked:', targetTab);
            
            // Update button states
            tabButtons.forEach(btn => {
                btn.classList.remove('bg-slate-800', 'text-white');
                btn.classList.add('bg-white', 'text-slate-700', 'hover:bg-slate-100');
                btn.setAttribute('aria-selected', 'false');
            });
            
            this.classList.remove('bg-white', 'text-slate-700', 'hover:bg-slate-100');
            this.classList.add('bg-slate-800', 'text-white');
            this.setAttribute('aria-selected', 'true');
            
            // Show/hide tab contents
            tabContents.forEach(content => {
                content.classList.add('hidden');
            });
            
            const targetContent = document.getElementById(targetTab + '-tab');
            if (targetContent) {
                targetContent.classList.remove('hidden');
            } else {
                console.error('Tab content not found:', targetTab + '-tab');
            }
        });
    });
}

/**
 * Initialize form handlers
 */
function initializeFormHandlers() {
    // Handle form submissions with loading states
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 150);
            }
        }, 5000);
    });
}

/**
 * Utility functions
 */
const Utils = {
    /**
     * Show a toast notification
     */
    showToast: function(message, type = 'info') {
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Add toast to container
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = toastContainer.lastElementChild;
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    },
    
    /**
     * Debounce function for performance optimization
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    /**
     * Get CSRF token from cookie
     */
    getCSRFToken: function() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
};

// Make Utils available globally
window.Utils = Utils;

/**
 * Header animation functions for overlays and dropdowns
 */

// Cart drawer animation
window.animateCartDrawer = function(show) {
    const drawer = document.getElementById('cart-drawer');
    if (!drawer) return;

    if (show) {
        drawer.style.display = 'block';
        drawer.style.transform = 'translateX(100%)';
        drawer.style.opacity = '0';

        // Force reflow
        drawer.offsetHeight;

        // Animate in
        drawer.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
        drawer.style.transform = 'translateX(0)';
        drawer.style.opacity = '1';
    } else {
        drawer.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
        drawer.style.transform = 'translateX(100%)';
        drawer.style.opacity = '0';

        setTimeout(() => {
            if (drawer.style.transform === 'translateX(100%)') {
                drawer.style.display = 'none';
            }
        }, 300);
    }
};

// Mobile menu animation
window.animateHeaderMobileMenu = function(show) {
    const menu = document.getElementById('mobile-menu');
    if (!menu) return;

    if (show) {
        menu.style.display = 'flex';
        menu.style.transform = 'translateX(-100%)';
        menu.style.opacity = '0';

        // Force reflow
        menu.offsetHeight;

        // Animate in
        menu.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
        menu.style.transform = 'translateX(0)';
        menu.style.opacity = '1';
    } else {
        menu.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
        menu.style.transform = 'translateX(-100%)';
        menu.style.opacity = '0';

        setTimeout(() => {
            if (menu.style.transform === 'translateX(-100%)') {
                menu.style.display = 'none';
            }
        }, 300);
    }
};

// Search overlay animation
window.animateHeaderSearchOverlay = function(show) {
    const overlay = document.getElementById('search-overlay');
    if (!overlay) return;

    if (show) {
        overlay.style.display = 'flex';
        overlay.style.opacity = '0';

        const content = overlay.querySelector('.search-content');
        if (content) {
            content.style.transform = 'translateY(-20px)';
            content.style.opacity = '0';
        }

        // Force reflow
        overlay.offsetHeight;

        // Animate in
        overlay.style.transition = 'opacity 0.2s ease-out';
        overlay.style.opacity = '1';

        if (content) {
            content.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
            content.style.transform = 'translateY(0)';
            content.style.opacity = '1';
        }

        // Focus search input after animation
        setTimeout(() => {
            const searchInput = overlay.querySelector('input[type="text"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }, 100);
    } else {
        const content = overlay.querySelector('.search-content');

        overlay.style.transition = 'opacity 0.2s ease-out';
        overlay.style.opacity = '0';

        if (content) {
            content.style.transition = 'transform 0.2s ease-out, opacity 0.2s ease-out';
            content.style.transform = 'translateY(-20px)';
            content.style.opacity = '0';
        }

        setTimeout(() => {
            if (overlay.style.opacity === '0') {
                overlay.style.display = 'none';
            }
        }, 200);
    }
};

// Dropdown animation
window.animateHeaderDropdown = function(dropdown, show) {
    if (!dropdown) return;

    if (show) {
        dropdown.style.display = 'block';
        dropdown.style.transform = 'translateY(-10px)';
        dropdown.style.opacity = '0';

        // Force reflow
        dropdown.offsetHeight;

        // Animate in
        dropdown.style.transition = 'transform 0.2s ease-out, opacity 0.2s ease-out';
        dropdown.style.transform = 'translateY(0)';
        dropdown.style.opacity = '1';
    } else {
        dropdown.style.transition = 'transform 0.2s ease-out, opacity 0.2s ease-out';
        dropdown.style.transform = 'translateY(-10px)';
        dropdown.style.opacity = '0';

        setTimeout(() => {
            if (dropdown.style.opacity === '0') {
                dropdown.style.display = 'none';
            }
        }, 200);
    }
}; 

// Cart management functions
window.updateCartQuantity = function(itemId, newQuantity) {
    if (newQuantity <= 0) {
        return removeFromCart(itemId);
    }

    const formData = new FormData();
    formData.append('quantity', newQuantity);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update Alpine.js store if available
            if (window.Alpine && Alpine.store('cart')) {
                // Refresh cart data
                loadCartData();
            }
        } else {
            console.error('Error updating cart:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

window.removeFromCart = function(itemId) {
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update Alpine.js store if available
            if (window.Alpine && Alpine.store('cart')) {
                // Refresh cart data
                loadCartData();
            }
        } else {
            console.error('Error removing from cart:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// Load cart data function
window.loadCartData = function() {
    fetch('/cart/api/data/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && window.Alpine && Alpine.store('cart')) {
            Alpine.store('cart', {
                items: data.items || [],
                subtotal: data.subtotal || 0,
                shipping: data.shipping || 0,
                total: data.total || 0,
                item_count: data.item_count || 0
            });
        }
    })
    .catch(error => {
        console.error('Error loading cart data:', error);
    });
};

// Get CSRF cookie helper function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
