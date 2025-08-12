// JavaScript for Anantya 2025 Website

document.addEventListener('DOMContentLoaded', function() {

    // Initialize form validation
    initializeFormValidation();

    // Initialize smooth scrolling
    initializeSmoothScrolling();

    // Initialize navbar scroll effect
    initializeNavbarScrollEffect();

    // Initialize animation on scroll
    initializeScrollAnimations();

});

// Form validation and submission
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation, #registrationForm');

    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Add loading state to submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('loading');
                    submitBtn.textContent = 'Processing...';
                }
            }

            form.classList.add('was-validated');
        }, false);
    });

    // Real-time validation for email
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const email = this.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (email && !emailRegex.test(email)) {
                this.setCustomValidity('Please enter a valid email address');
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // Real-time validation for phone number
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            // Remove non-numeric characters
            this.value = this.value.replace(/[^0-9]/g, '');

            // Limit to 10 digits
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });

        phoneInput.addEventListener('blur', function() {
            if (this.value.length !== 10) {
                this.setCustomValidity('Phone number must be exactly 10 digits');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                e.preventDefault();

                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Navbar scroll effect
function initializeNavbarScrollEffect() {
    const navbar = document.querySelector('.navbar');

    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(13, 110, 253, 0.98)';
                navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
            } else {
                navbar.style.background = 'rgba(13, 110, 253, 0.95)';
                navbar.style.boxShadow = 'none';
            }
        });
    }
}

// Animation on scroll
function initializeScrollAnimations() {
    const animatedElements = document.querySelectorAll('.card, .display-4, .display-5');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'all 0.6s ease';
            }
        });
    }, observerOptions);

    animatedElements.forEach(function(element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        observer.observe(element);
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Handle form errors
function handleFormError(message) {
    showAlert(message, 'danger');

    // Remove loading state from submit button
    const submitBtn = document.querySelector('button[type="submit"].loading');
    if (submitBtn) {
        submitBtn.classList.remove('loading');
        submitBtn.textContent = 'Complete Registration';
    }
}

// Handle form success
function handleFormSuccess(message) {
    showAlert(message, 'success');
}

// Preloader (if needed)
function showPreloader() {
    const preloader = document.createElement('div');
    preloader.id = 'preloader';
    preloader.innerHTML = `
        <div class="d-flex justify-content-center align-items-center min-vh-100">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    document.body.appendChild(preloader);
}

function hidePreloader() {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.remove();
    }
}

// Export functions for global access
window.AnanyaWebsite = {
    showAlert,
    handleFormError,
    handleFormSuccess,
    showPreloader,
    hidePreloader
};