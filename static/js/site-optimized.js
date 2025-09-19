// Site-wide Optimized JavaScript - Consolidated from all templates
(function() {
  'use strict';

  // ========================================
  // Utility Functions
  // ========================================
  
  // Debounce function for performance
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Format number with Swedish locale
  function formatNumber(num, decimals = 0) {
    const rounded = decimals > 0 ? num.toFixed(decimals) : Math.round(num);
    const parts = rounded.toString().split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    return parts.join(',');
  }

  // Parse number from formatted string
  function parseNumber(str) {
    return parseFloat(String(str).replace(/\s/g, '').replace(',', '.')) || 0;
  }

  // ========================================
  // Component Initializers
  // ========================================

  // Initialize FAQ Accordions
  function initFAQAccordions() {
    // Handle details/summary elements
    const detailsAccordions = document.querySelectorAll('details.faq-item');
    
    detailsAccordions.forEach(accordion => {
      const summary = accordion.querySelector('summary');
      if (!summary) return;
      
      // Add keyboard support
      summary.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          accordion.open = !accordion.open;
        }
      });
    });
    
    // Handle button-based accordions with data attributes
    const accordionButtons = document.querySelectorAll('[data-accordion-button]');
    
    accordionButtons.forEach(button => {
      button.addEventListener('click', function() {
        const accordionItem = button.closest('.accordion-item');
        const content = accordionItem.querySelector('.accordion-content, [data-accordion-content]');
        const icon = button.querySelector('.accordion-icon, svg');
        const isOpen = !content.classList.contains('hidden');
        
        // Get parent accordion container
        const accordionContainer = button.closest('[data-accordion]');
        
        // Close all other accordions in the same group if exclusive
        if (accordionContainer && accordionContainer.dataset.accordionMultiple !== 'true') {
          accordionContainer.querySelectorAll('.accordion-content, [data-accordion-content]').forEach(item => {
            if (item !== content) {
              item.classList.add('hidden');
              const otherIcon = item.parentElement.querySelector('.accordion-icon, svg');
              if (otherIcon) otherIcon.classList.remove('rotate-180', 'rotate-45');
            }
          });
        }
        
        // Toggle current accordion
        if (isOpen) {
          content.classList.add('hidden');
          if (icon) icon.classList.remove('rotate-180', 'rotate-45');
        } else {
          content.classList.remove('hidden');
          if (icon) icon.classList.add('rotate-180');
        }
      });
      
      // Add keyboard support
      button.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          button.click();
        }
      });
    });
  }

  // Initialize Range Sliders
  function initRangeSliders() {
    const sliders = document.querySelectorAll('input[type="range"].slider');
    
    sliders.forEach(slider => {
      const displayId = slider.getAttribute('data-display');
      const display = displayId ? document.getElementById(displayId) : null;
      
      const updateSlider = debounce(() => {
        const value = slider.value;
        const min = slider.min;
        const max = slider.max;
        const percentage = ((value - min) / (max - min)) * 100;
        
        slider.style.setProperty('--value', percentage + '%');
        
        if (display) {
          display.value = formatNumber(value);
        }
        
        // Trigger custom event
        slider.dispatchEvent(new CustomEvent('rangeupdate', { 
          detail: { value, percentage } 
        }));
      }, 10);
      
      slider.addEventListener('input', updateSlider);
      
      if (display) {
        display.addEventListener('input', debounce(function() {
          const value = parseNumber(this.value);
          const min = parseFloat(slider.min);
          const max = parseFloat(slider.max);
          
          if (value >= min && value <= max) {
            slider.value = value;
            updateSlider();
          }
        }, 300));
      }
      
      // Initial update
      updateSlider();
    });
  }

  // Initialize Loan Calculators
  function initLoanCalculators() {
    const calculators = document.querySelectorAll('[data-calculator]');
    
    calculators.forEach(calculator => {
      const amountInput = calculator.querySelector('[data-amount]');
      const rateInput = calculator.querySelector('[data-rate]');
      const termInput = calculator.querySelector('[data-term]');
      const monthlyDisplay = calculator.querySelector('[data-monthly]');
      const totalDisplay = calculator.querySelector('[data-total]');
      const interestDisplay = calculator.querySelector('[data-interest]');
      
      if (!amountInput || !rateInput || !termInput) return;
      
      const calculate = debounce(() => {
        const principal = parseNumber(amountInput.value) || 0;
        const annualRate = parseNumber(rateInput.value) || 0;
        const months = parseNumber(termInput.value) || 0;
        
        if (principal <= 0 || annualRate <= 0 || months <= 0) {
          if (monthlyDisplay) monthlyDisplay.textContent = '0 kr';
          if (totalDisplay) totalDisplay.textContent = '0 kr';
          if (interestDisplay) interestDisplay.textContent = '0 kr';
          return;
        }
        
        const monthlyRate = annualRate / 100 / 12;
        const monthlyPayment = principal * (monthlyRate * Math.pow(1 + monthlyRate, months)) / 
                              (Math.pow(1 + monthlyRate, months) - 1);
        const totalPayment = monthlyPayment * months;
        const totalInterest = totalPayment - principal;
        
        requestAnimationFrame(() => {
          if (monthlyDisplay) monthlyDisplay.textContent = formatNumber(monthlyPayment, 2) + ' kr';
          if (totalDisplay) totalDisplay.textContent = formatNumber(totalPayment, 2) + ' kr';
          if (interestDisplay) interestDisplay.textContent = formatNumber(totalInterest, 2) + ' kr';
        });
      }, 150);
      
      amountInput.addEventListener('input', calculate);
      rateInput.addEventListener('input', calculate);
      termInput.addEventListener('input', calculate);
      
      calculate();
    });
  }

  // Initialize Sortable Tables
  function initSortableTables() {
    const tables = document.querySelectorAll('table[data-sortable]');
    
    tables.forEach(table => {
      const headers = table.querySelectorAll('th[data-sort]');
      
      headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.setAttribute('tabindex', '0');
        header.setAttribute('role', 'button');
        
        const sortTable = () => {
          const tbody = table.querySelector('tbody');
          if (!tbody) return;
          
          const rows = Array.from(tbody.querySelectorAll('tr'));
          const isAscending = header.classList.contains('sorted-asc');
          
          // Remove all sorted classes
          headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
          
          // Sort rows
          rows.sort((a, b) => {
            const aValue = a.cells[index]?.getAttribute('data-sort-value') || 
                          a.cells[index]?.textContent || '';
            const bValue = b.cells[index]?.getAttribute('data-sort-value') || 
                          b.cells[index]?.textContent || '';
            
            const aNum = parseFloat(aValue);
            const bNum = parseFloat(bValue);
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
              return isAscending ? bNum - aNum : aNum - bNum;
            }
            
            return isAscending ? 
              bValue.localeCompare(aValue, 'sv-SE') : 
              aValue.localeCompare(bValue, 'sv-SE');
          });
          
          header.classList.add(isAscending ? 'sorted-desc' : 'sorted-asc');
          
          // Use DocumentFragment for better performance
          const fragment = document.createDocumentFragment();
          rows.forEach(row => fragment.appendChild(row));
          tbody.appendChild(fragment);
        };
        
        header.addEventListener('click', sortTable);
        header.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            sortTable();
          }
        });
      });
    });
  }

  // Initialize Tab Navigation
  function initTabs() {
    const tabContainers = document.querySelectorAll('[data-tabs]');
    
    tabContainers.forEach(container => {
      const buttons = container.querySelectorAll('[data-tab-button]');
      const panels = container.querySelectorAll('[data-tab-panel]');
      
      buttons.forEach(button => {
        button.addEventListener('click', () => {
          const targetId = button.getAttribute('data-tab-button');
          
          // Update buttons
          buttons.forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
          });
          button.classList.add('active');
          button.setAttribute('aria-selected', 'true');
          
          // Update panels
          panels.forEach(panel => {
            if (panel.getAttribute('data-tab-panel') === targetId) {
              panel.classList.remove('hidden');
              panel.setAttribute('aria-hidden', 'false');
            } else {
              panel.classList.add('hidden');
              panel.setAttribute('aria-hidden', 'true');
            }
          });
        });
      });
    });
  }

  // Initialize Scroll Indicators for Tables
  function initScrollIndicators() {
    const containers = document.querySelectorAll('.overflow-x-auto');
    
    containers.forEach(container => {
      const wrapper = container.closest('.table-container');
      if (!wrapper) return;
      
      const checkScroll = debounce(() => {
        const maxScroll = container.scrollWidth - container.clientWidth;
        const currentScroll = container.scrollLeft;
        
        wrapper.classList.toggle('scrolled-left', currentScroll > 10);
        wrapper.classList.toggle('scrolled-right', currentScroll >= maxScroll - 10);
      }, 10);
      
      container.addEventListener('scroll', checkScroll, { passive: true });
      
      // Check on resize
      window.addEventListener('resize', checkScroll, { passive: true });
      
      // Initial check
      checkScroll();
    });
  }

  // Initialize Lazy Loading for Images
  function initLazyLoading() {
    // Native lazy loading fallback
    if ('loading' in HTMLImageElement.prototype) {
      const images = document.querySelectorAll('img[loading="lazy"]');
      images.forEach(img => {
        if (!img.complete) {
          img.classList.add('loading');
          img.addEventListener('load', () => {
            img.classList.remove('loading');
            img.classList.add('loaded');
          });
        }
      });
    } else {
      // Fallback for browsers that don't support native lazy loading
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('loading');
            img.classList.add('loaded');
            observer.unobserve(img);
          }
        });
      });
      
      const images = document.querySelectorAll('img[data-src]');
      images.forEach(img => imageObserver.observe(img));
    }
  }

  // Initialize Smooth Scroll for Anchors
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          const offset = 80; // Account for fixed header
          const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
          
          // Update URL without triggering scroll
          history.pushState(null, null, targetId);
        }
      });
    });
  }

  // Initialize Form Validation
  function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
      form.addEventListener('submit', function(e) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
          if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            
            // Show error message
            let errorMsg = input.parentElement.querySelector('.error-message');
            if (!errorMsg) {
              errorMsg = document.createElement('span');
              errorMsg.className = 'error-message text-red-500 text-sm mt-1';
              errorMsg.textContent = 'This field is required';
              input.parentElement.appendChild(errorMsg);
            }
          } else {
            input.classList.remove('error');
            const errorMsg = input.parentElement.querySelector('.error-message');
            if (errorMsg) errorMsg.remove();
          }
        });
        
        if (!isValid) {
          e.preventDefault();
        }
      });
    });
  }

  // ========================================
  // Main Initialization
  // ========================================
  
  function init() {
    initFAQAccordions();
    initRangeSliders();
    initLoanCalculators();
    initSortableTables();
    initTabs();
    initScrollIndicators();
    initLazyLoading();
    initSmoothScroll();
    initFormValidation();
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export utilities for use in other scripts
  window.SiteUtils = {
    debounce,
    formatNumber,
    parseNumber,
    init
  };

})();