/**
 * KARTMART — Client-side Interactivity Script
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initFilterPills();
    checkLiveHealth();
    initFlashClose();
});

// Mobile Navigation Toggle
function initMobileNav() {
    const toggleBtn = document.getElementById('mobile-toggle-btn');
    const navMenu = document.getElementById('nav-menu');
    
    if (toggleBtn && navMenu) {
        toggleBtn.addEventListener('click', () => {
            const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
            toggleBtn.setAttribute('aria-expanded', !isExpanded);
            navMenu.classList.toggle('open');
        });
    }
}

// Category Filter Pills
function initFilterPills() {
    const pills = document.querySelectorAll('.filter-pills .pill');
    const cards = document.querySelectorAll('.products-grid .product-card');
    
    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            
            const filter = pill.getAttribute('data-filter');
            cards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Simulated Cart Counter & Toast Notification
let cartCount = 0;
function simulateAddToCart(productName) {
    cartCount++;
    const countBadge = document.getElementById('cart-item-count');
    if (countBadge) {
        countBadge.textContent = cartCount;
        countBadge.style.transform = 'scale(1.3)';
        setTimeout(() => {
            countBadge.style.transform = 'scale(1)';
        }, 200);
    }
    
    showToast(`Added "${productName}" to shopping cart!`);
}

// Toast Notification
function showToast(message) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.style.cssText = `
        background: #1e293b;
        color: #f8fafc;
        border: 1px solid rgba(99, 102, 241, 0.4);
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease;
    `;
    toast.innerHTML = `<span>🛒</span> <span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2800);
}

// Live Health Check Fetch
async function checkLiveHealth() {
    const statusDisplay = document.getElementById('db-status-display');
    const apiPreview = document.getElementById('api-health-preview');
    
    if (statusDisplay) statusDisplay.textContent = 'Pinging server...';
    
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (apiPreview) {
            apiPreview.textContent = JSON.stringify(data);
        }
        
        if (statusDisplay) {
            if (data.database && data.database.status === 'connected') {
                statusDisplay.textContent = `Connected (${data.database.engine})`;
                statusDisplay.className = 'tile-value status-text-online';
            } else {
                statusDisplay.textContent = `Offline (${data.database.engine})`;
                statusDisplay.className = 'tile-value status-text-degraded';
            }
        }
    } catch (err) {
        if (apiPreview) apiPreview.textContent = 'Failed to fetch /health';
        if (statusDisplay) {
            statusDisplay.textContent = 'Connection Error';
            statusDisplay.className = 'tile-value status-text-degraded';
        }
    }
}

// Flash Message Close Handlers
function initFlashClose() {
    document.querySelectorAll('.flash-close').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const alert = e.target.closest('.flash-alert');
            if (alert) alert.remove();
        });
    });
}
