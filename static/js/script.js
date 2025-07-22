document.addEventListener('DOMContentLoaded', function() {
    // Add mobile bottom navigation if screen is small
    if (window.innerWidth <= 768) {
        addMobileBottomNav();
    }
    
    // Add event listeners to form elements
    setupFormValidation();
    
    // Initialize Bootstrap tooltips and popovers
    initBootstrapComponents();
});

/**
 * Adds a mobile bottom navigation bar for small screens
 */
function addMobileBottomNav() {
    // Check if we're on a page that's not login/register/etc.
    if (document.querySelector('.navbar-nav')) {
        const nav = document.createElement('div');
        nav.className = 'mobile-bottom-nav';
        
        // Get the current path
        const currentPath = window.location.pathname;
        
        // Add navigation items
        nav.innerHTML = `
            <a href="/" class="${currentPath === '/' ? 'active' : ''}">
                <i class="fas fa-home"></i>
                <span>Home</span>
            </a>
            <a href="/users" class="${currentPath.startsWith('/users') ? 'active' : ''}">
                <i class="fas fa-users"></i>
                <span>Applicants</span>
            </a>
            <a href="/users/new" class="">
                <i class="fas fa-plus-circle"></i>
                <span>Add</span>
            </a>
            <a href="/matches" class="${currentPath.startsWith('/matches') ? 'active' : ''}">
                <i class="fas fa-handshake"></i>
                <span>Matches</span>
            </a>
            <a href="#" class="js-profile-menu">
                <i class="fas fa-user"></i>
                <span>Profile</span>
            </a>
        `;
        
        document.body.appendChild(nav);
        
        // Profile menu click handler
        document.querySelector('.js-profile-menu').addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = document.querySelector('.dropdown-menu');
            if (dropdown) {
                dropdown.classList.toggle('show');
            }
        });
    }
}

/**
 * Sets up client-side form validation
 */
function setupFormValidation() {
    // Get all forms that need validation
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Initializes Bootstrap components
 */
function initBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Functions for match pages
 */
function initMatchFilters() {
    const matchMinScore = document.getElementById('matchMinScore');
    const matchCards = document.querySelectorAll('.match-card');
    
    if (matchMinScore && matchCards.length > 0) {
        matchMinScore.addEventListener('input', function() {
            const minScore = parseInt(this.value);
            document.getElementById('scoreValue').textContent = minScore;
            
            matchCards.forEach(card => {
                const score = parseInt(card.getAttribute('data-score'));
                if (score >= minScore) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
} 