/**
 * main.js - PlantSense AI Frontend JavaScript
 * =============================================
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- Navbar scroll effect ---
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 20);
        });
    }

    // --- Mobile menu toggle ---
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('open');
            navToggle.classList.toggle('active');
        });

        // Close menu when clicking a link
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('open');
                navToggle.classList.remove('active');
            });
        });
    }

    // --- Scroll animations (IntersectionObserver) ---
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    if (animateElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-slide-up');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animateElements.forEach(el => observer.observe(el));
    }

    // --- Form validation ---
    const predictForm = document.getElementById('predictForm');
    if (predictForm) {
        predictForm.addEventListener('submit', (e) => {
            const inputs = predictForm.querySelectorAll('input[type="number"]');
            let valid = true;

            inputs.forEach(input => {
                if (input.value === '' || isNaN(parseFloat(input.value))) {
                    input.style.borderColor = '#ef4444';
                    input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
                    valid = false;
                } else {
                    input.style.borderColor = '';
                    input.style.boxShadow = '';
                }
            });

            if (!valid) {
                e.preventDefault();
                showAlert('Please fill in all biosensor values.', 'error');
            }
        });

        // Clear error styling on input focus
        predictForm.querySelectorAll('input').forEach(input => {
            input.addEventListener('focus', () => {
                input.style.borderColor = '';
                input.style.boxShadow = '';
            });
        });
    }

    // --- Probability bar animations ---
    const probBars = document.querySelectorAll('.probability-bar-fill');
    if (probBars.length > 0) {
        const barObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const width = entry.target.dataset.width;
                    setTimeout(() => {
                        entry.target.style.width = width + '%';
                    }, 300);
                    barObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        probBars.forEach(bar => {
            bar.style.width = '0%';
            barObserver.observe(bar);
        });
    }

    // --- Counter animation for stats ---
    const statValues = document.querySelectorAll('.stat-value[data-count]');
    if (statValues.length > 0) {
        const countObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCount(entry.target);
                    countObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statValues.forEach(el => countObserver.observe(el));
    }

});

/**
 * Animate a number count-up effect
 */
function animateCount(element) {
    const target = parseInt(element.dataset.count);
    const suffix = element.dataset.suffix || '';
    const duration = 1500;
    const start = performance.now();

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // Ease out cubic
        const current = Math.floor(eased * target);
        element.textContent = current.toLocaleString() + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/**
 * Show an alert message
 */
function showAlert(message, type = 'error') {
    const existing = document.querySelector('.alert-dynamic');
    if (existing) existing.remove();

    const icons = {
        error: 'fas fa-exclamation-circle',
        success: 'fas fa-check-circle',
        warning: 'fas fa-exclamation-triangle'
    };

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dynamic animate-slide-up`;
    alert.innerHTML = `<i class="${icons[type]}"></i> ${message}`;

    const form = document.getElementById('predictForm');
    if (form) {
        form.parentNode.insertBefore(alert, form);
    }

    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 300);
    }, 4000);
}
