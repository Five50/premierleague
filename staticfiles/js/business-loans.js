// Business Loans Optimized JavaScript
(function() {
  'use strict';

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

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBusinessLoans);
  } else {
    initBusinessLoans();
  }

  function initBusinessLoans() {
    initTableOfContents();
    initLoanSlider();
    initLoanCalculator();
    initTableSorting();
    initScrollIndicators();
  }

  // Table of Contents - Optimized
  function initTableOfContents() {
    const tocList = document.getElementById('toc-list');
    if (!tocList) return;

    const headings = document.querySelectorAll('h2:not(#loan-filter-heading), h3, h4');
    if (!headings.length) {
      const tocContainer = document.getElementById('dynamic-toc');
      if (tocContainer) tocContainer.style.display = 'none';
      return;
    }

    const fragment = document.createDocumentFragment();
    
    headings.forEach(heading => {
      const text = heading.textContent.trim();
      if (!text) return;
      
      if (!heading.id) {
        heading.id = text.toLowerCase()
          .replace(/[åä]/g, 'a')
          .replace(/ö/g, 'o')
          .replace(/[^\w\s-]/g, '')
          .replace(/\s+/g, '-')
          .replace(/-+/g, '-')
          .trim();
      }
      
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + heading.id;
      a.className = 'text-blue-400 hover:text-blue-300 transition-colors';
      a.textContent = text;
      
      if (heading.tagName === 'H3') {
        li.style.marginLeft = '1rem';
      } else if (heading.tagName === 'H4') {
        li.style.marginLeft = '2rem';
      }
      
      li.appendChild(a);
      fragment.appendChild(li);
    });
    
    tocList.appendChild(fragment);
  }

  // Loan Amount Slider - Optimized
  function initLoanSlider() {
    const slider = document.getElementById('loanAmountSlider');
    const display = document.getElementById('loanAmountDisplay');
    if (!slider || !display) return;

    function formatNumber(num) {
      return Math.round(num).toLocaleString('sv-SE').replace(/,/g, ' ');
    }

    const updateSlider = debounce(() => {
      const value = slider.value;
      const min = slider.min;
      const max = slider.max;
      const percentage = ((value - min) / (max - min)) * 100;
      
      display.value = formatNumber(value);
      slider.style.setProperty('--value', percentage + '%');
      
      // Update loan amounts in cards
      document.querySelectorAll('.loan-amount').forEach(el => {
        el.textContent = formatNumber(value) + ' SEK';
      });
    }, 10);

    slider.addEventListener('input', updateSlider);
    
    display.addEventListener('input', debounce(function() {
      const value = parseInt(this.value.replace(/\s/g, '')) || 0;
      if (value >= 10000 && value <= 30000000) {
        slider.value = value;
        updateSlider();
      }
    }, 300));
    
    display.addEventListener('blur', updateSlider);
    updateSlider();
  }

  // Loan Calculator - Optimized
  function initLoanCalculator() {
    const loanAmountInput = document.getElementById('loanAmount');
    const interestRateInput = document.getElementById('interestRate');
    const loanTermInput = document.getElementById('loanTerm');
    
    if (!loanAmountInput || !interestRateInput || !loanTermInput) return;

    function formatNumber(num, decimals = 0) {
      const rounded = decimals > 0 ? num.toFixed(decimals) : Math.round(num);
      const parts = rounded.toString().split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
      return parts.join(',');
    }

    function parseNumber(str) {
      return parseFloat(String(str).replace(/\s/g, '').replace(',', '.')) || 0;
    }

    const calculateLoan = debounce(() => {
      const principal = parseNumber(loanAmountInput.value) || 0;
      const annualRate = parseNumber(interestRateInput.value) || 0;
      const months = parseNumber(loanTermInput.value) || 0;
      
      const monthlyPaymentEl = document.getElementById('monthlyPayment');
      const totalLoanAmountEl = document.getElementById('totalLoanAmount');
      const totalInterestEl = document.getElementById('totalInterest');
      const totalPaymentEl = document.getElementById('totalPayment');
      
      if (!monthlyPaymentEl || !totalLoanAmountEl || !totalInterestEl || !totalPaymentEl) return;
      
      if (principal <= 0 || annualRate <= 0 || months <= 0) {
        monthlyPaymentEl.textContent = '0 kr';
        totalLoanAmountEl.textContent = '0 kr';
        totalInterestEl.textContent = '0 kr';
        totalPaymentEl.textContent = '0 kr';
        return;
      }
      
      const monthlyRate = annualRate / 100 / 12;
      const monthlyPayment = principal * (monthlyRate * Math.pow(1 + monthlyRate, months)) / 
                            (Math.pow(1 + monthlyRate, months) - 1);
      
      const totalPayment = monthlyPayment * months;
      const totalInterest = totalPayment - principal;
      
      // Use requestAnimationFrame for smooth updates
      requestAnimationFrame(() => {
        monthlyPaymentEl.textContent = formatNumber(monthlyPayment, 2) + ' kr';
        totalLoanAmountEl.textContent = formatNumber(principal) + ' kr';
        totalInterestEl.textContent = formatNumber(totalInterest, 2) + ' kr';
        totalPaymentEl.textContent = formatNumber(totalPayment, 2) + ' kr';
      });
    }, 150);

    loanAmountInput.addEventListener('input', calculateLoan);
    interestRateInput.addEventListener('input', calculateLoan);
    loanTermInput.addEventListener('input', calculateLoan);
    
    calculateLoan();
  }

  // Table Sorting - Optimized
  function initTableSorting() {
    const headers = document.querySelectorAll('#best-business-loans th[scope="col"]');
    if (!headers.length) return;

    headers.forEach((header, index) => {
      header.style.cursor = 'pointer';
      header.addEventListener('click', function() {
        const tbody = document.querySelector('#best-business-loans tbody');
        if (!tbody) return;
        
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAscending = header.classList.contains('sorted-asc');
        
        headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
        
        rows.sort((a, b) => {
          const aValue = a.cells[index].getAttribute('data-sort-value') || a.cells[index].textContent;
          const bValue = b.cells[index].getAttribute('data-sort-value') || b.cells[index].textContent;
          
          return isAscending ? 
            bValue.localeCompare(aValue) : 
            aValue.localeCompare(bValue);
        });
        
        header.classList.add(isAscending ? 'sorted-desc' : 'sorted-asc');
        
        // Use DocumentFragment for better performance
        const fragment = document.createDocumentFragment();
        rows.forEach(row => fragment.appendChild(row));
        tbody.appendChild(fragment);
      });
    });
  }

  // Scroll Indicators - Optimized
  function initScrollIndicators() {
    const container = document.querySelector('.table-container .overflow-x-auto');
    if (!container) return;
    
    const wrapper = container.closest('.table-container');
    if (!wrapper) return;

    const checkScroll = debounce(() => {
      const maxScroll = container.scrollWidth - container.clientWidth;
      const currentScroll = container.scrollLeft;
      
      wrapper.classList.toggle('scrolled-left', currentScroll > 10);
      wrapper.classList.toggle('scrolled-right', currentScroll >= maxScroll - 10);
    }, 10);

    container.addEventListener('scroll', checkScroll, { passive: true });
    checkScroll();
  }
})();