/**
 * KARTMART — Modern Client-Side Interactivity Script
 * Handles Cart Drawer, AJAX Add-to-Cart, Coupon Copy, Countdown Timers, and System Health.
 */

// Initialize theme immediately before DOM to avoid flicker
(function initTheme() {
    const saved = localStorage.getItem('km_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', () => {
    initThemeIcon();
    initMobileNav();
    initFilterPills();
    initCartDrawer();
    initDealTimer();
    initFestiveTimer();
    initFlashClose();
    checkLiveHealth();
});

// ==========================================
// Theme Management (Light / Dark Mode)
// ==========================================
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('km_theme', newTheme);
    updateThemeIcon(newTheme);
    showToast(`Switched to ${newTheme === 'dark' ? 'Dark' : 'Light'} Mode`, 'info');
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

function initThemeIcon() {
    const saved = localStorage.getItem('km_theme') || 'dark';
    updateThemeIcon(saved);
}

// ==========================================
// Wishlist AJAX Toggle
// ==========================================
async function toggleWishlist(productId, btnEl) {
    try {
        const response = await fetch(`/account/wishlist/toggle/${productId}`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        if (data.status === 'unauthorized') {
            window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname);
            return;
        }
        if (data.action === 'added') {
            if (btnEl) {
                btnEl.classList.add('active');
                btnEl.setAttribute('aria-pressed', 'true');
            }
            showToast(data.message || 'Saved to Wishlist ❤️', 'success');
        } else if (data.action === 'removed') {
            if (btnEl) {
                btnEl.classList.remove('active');
                btnEl.setAttribute('aria-pressed', 'false');
            }
            showToast(data.message || 'Removed from Wishlist', 'info');
            // If on wishlist page, remove the card smoothly
            const rowCard = document.getElementById(`wishlist-card-${productId}`);
            if (rowCard) {
                rowCard.style.opacity = '0';
                rowCard.style.transform = 'scale(0.9)';
                setTimeout(() => rowCard.remove(), 250);
            }
        }
    } catch (e) {
        console.error('Wishlist error:', e);
        showToast('Could not update wishlist', 'error');
    }
}

// Festive Countdown Timer
function initFestiveTimer() {
    const timerEls = document.querySelectorAll('.festive-countdown, #diwali-timer-clock');
    if (!timerEls.length) return;

    let totalSeconds = 3 * 86400 + 14 * 3600 + 32 * 60 + 10;
    setInterval(() => {
        totalSeconds--;
        if (totalSeconds <= 0) return;

        const days = Math.floor(totalSeconds / 86400);
        const hours = Math.floor((totalSeconds % 86400) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        const str = `${days}d : ${String(hours).padStart(2, '0')}h : ${String(minutes).padStart(2, '0')}m : ${String(seconds).padStart(2, '0')}s`;
        timerEls.forEach(el => el.textContent = str);
    }, 1000);
}

// ==========================================
// 1. Mobile Navigation & Account Dropdowns
// ==========================================
function initMobileNav() {
    const toggleBtn = document.getElementById('mobile-toggle-btn');
    const navMenu = document.querySelector('.nav-actions-menu');
    
    if (toggleBtn && navMenu) {
        toggleBtn.addEventListener('click', () => {
            const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
            toggleBtn.setAttribute('aria-expanded', !isExpanded);
            navMenu.classList.toggle('open');
        });
    }

    // Account dropdown click support for mobile/touch
    const accountTrigger = document.getElementById('account-trigger');
    const accountDropdown = document.getElementById('account-dropdown');
    if (accountTrigger && accountDropdown) {
        accountTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            accountDropdown.classList.toggle('active');
        });

        document.addEventListener('click', () => {
            accountDropdown.classList.remove('active');
        });
    }
}

// ==========================================
// 2. Category Filter Pills (Front-end Filtering)
// ==========================================
function initFilterPills() {
    const pills = document.querySelectorAll('.filter-pills .pill');
    const cards = document.querySelectorAll('.products-grid .product-card');
    
    if (!pills.length) return;

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

// ==========================================
// 3. Cart Drawer Flyout & AJAX Cart Management
// ==========================================
function initCartDrawer() {
    const openBtn = document.getElementById('open-cart-drawer-btn');
    const closeBtn = document.getElementById('close-cart-drawer-btn');
    const overlay = document.getElementById('cart-drawer-overlay');
    const drawer = document.getElementById('cart-drawer');

    if (!drawer) return;

    if (openBtn) {
        openBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openCartDrawer();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeCartDrawer);
    }

    if (overlay) {
        overlay.addEventListener('click', closeCartDrawer);
    }

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && drawer.classList.contains('open')) {
            closeCartDrawer();
        }
    });
}

function openCartDrawer() {
    const drawer = document.getElementById('cart-drawer');
    if (drawer) {
        drawer.classList.add('open');
        drawer.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden'; // Prevent background scroll
        loadCartDrawer();
    }
}

function closeCartDrawer() {
    const drawer = document.getElementById('cart-drawer');
    if (drawer) {
        drawer.classList.remove('open');
        drawer.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }
}

// Fetch Cart Data and Render inside Slide-out Drawer
async function loadCartDrawer() {
    const itemsContainer = document.getElementById('cart-drawer-items');
    const drawerCount = document.getElementById('drawer-cart-count');
    const globalCount = document.getElementById('global-cart-count');
    const subtotalEl = document.getElementById('drawer-subtotal');
    const deliveryEl = document.getElementById('drawer-delivery');
    const totalEl = document.getElementById('drawer-total');
    const progressFill = document.getElementById('delivery-progress-fill');
    const thresholdMsg = document.getElementById('delivery-threshold-msg');
    const checkoutBtn = document.getElementById('drawer-checkout-btn');

    if (!itemsContainer) return;

    itemsContainer.innerHTML = '<div class="drawer-loading"><span>Loading your cart...</span></div>';

    try {
        const response = await fetch('/cart/api/drawer');
        if (!response.ok) throw new Error('Network error');
        const data = await response.json();

        // Update counts
        if (drawerCount) drawerCount.textContent = data.total_items;
        if (globalCount) globalCount.textContent = data.total_items;

        // Update amounts
        const currency = '₹';
        if (subtotalEl) subtotalEl.textContent = `${currency}${data.subtotal.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        if (deliveryEl) deliveryEl.textContent = data.delivery_fee === 0 ? 'FREE' : `${currency}${data.delivery_fee.toFixed(2)}`;
        if (totalEl) totalEl.textContent = `${currency}${data.total.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

        // Free Delivery Progress calculation (Threshold: ₹499)
        const freeThreshold = 499.0;
        if (progressFill && thresholdMsg) {
            if (data.subtotal >= freeThreshold && data.total_items > 0) {
                progressFill.style.width = '100%';
                thresholdMsg.innerHTML = '🎉 You unlocked <strong>FREE Delivery!</strong>';
            } else if (data.total_items === 0) {
                progressFill.style.width = '0%';
                thresholdMsg.innerHTML = 'Add items to unlock <strong>FREE Delivery</strong>';
            } else {
                const diff = (freeThreshold - data.subtotal).toFixed(2);
                const percent = Math.min(100, Math.round((data.subtotal / freeThreshold) * 100));
                progressFill.style.width = `${percent}%`;
                thresholdMsg.innerHTML = `Add <strong>₹${diff}</strong> more for <strong>FREE Delivery</strong>`;
            }
        }

        // Render Items
        if (!data.items || data.items.length === 0) {
            itemsContainer.innerHTML = `
                <div class="drawer-empty-state">
                    <span class="empty-icon">🛒</span>
                    <p>Your shopping cart is empty.</p>
                    <a href="/products" class="btn btn-secondary btn-sm" onclick="closeCartDrawer()">Shop Today's Deals</a>
                </div>
            `;
            if (checkoutBtn) {
                checkoutBtn.classList.add('disabled');
                checkoutBtn.setAttribute('aria-disabled', 'true');
                checkoutBtn.style.pointerEvents = 'none';
                checkoutBtn.style.opacity = '0.5';
            }
            return;
        }

        if (checkoutBtn) {
            checkoutBtn.classList.remove('disabled');
            checkoutBtn.removeAttribute('aria-disabled');
            checkoutBtn.style.pointerEvents = 'auto';
            checkoutBtn.style.opacity = '1';
        }

        let html = '';
        data.items.forEach(item => {
            html += `
                <div class="drawer-item-row" id="drawer-item-${item.id}">
                    <div class="drawer-item-img-wrap">
                        <img src="${item.product_image || '/static/img/products/fallback.jpg'}" alt="${escapeHtml(item.product_name)}" class="drawer-item-img" onerror="this.onerror=null;this.src='/static/img/products/fallback.jpg';">
                    </div>
                    <div class="drawer-item-info">
                        <h4 class="drawer-item-name">${escapeHtml(item.product_name)}</h4>
                        <div class="drawer-item-price-line">
                            ${currency}${item.product_price.toLocaleString('en-IN', {minimumFractionDigits: 2})} &times; ${item.quantity} = <strong>${currency}${item.subtotal.toLocaleString('en-IN', {minimumFractionDigits: 2})}</strong>
                        </div>
                        <div class="drawer-item-actions">
                            <div class="drawer-qty-stepper">
                                <button type="button" class="drawer-step-btn" onclick="updateCartItemQty(${item.id}, ${item.quantity - 1})" ${item.quantity <= 1 ? 'disabled' : ''}>-</button>
                                <span class="drawer-qty-val">${item.quantity}</span>
                                <button type="button" class="drawer-step-btn" onclick="updateCartItemQty(${item.id}, ${item.quantity + 1})" ${item.quantity >= item.stock ? 'disabled' : ''}>+</button>
                            </div>
                            <button type="button" class="drawer-item-del-btn" onclick="removeCartItem(${item.id})">Delete</button>
                        </div>
                    </div>
                </div>
            `;
        });
        itemsContainer.innerHTML = html;

    } catch (err) {
        console.error('Failed to load cart drawer:', err);
        itemsContainer.innerHTML = '<div class="drawer-empty-state"><p>Could not load cart. Please try again.</p></div>';
    }
}

// 1-Click Quick Add To Cart with Live Drawer Feedback
async function quickAddToCart(productId, productName) {
    try {
        const formData = new FormData();
        formData.append('quantity', 1);

        const response = await fetch(`/cart/add/${productId}?format=json`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();

        if (data.success) {
            // Update badge with bounce animation
            const badge = document.getElementById('global-cart-count');
            if (badge) {
                badge.textContent = data.cart_count;
                badge.style.transform = 'scale(1.35)';
                setTimeout(() => badge.style.transform = 'scale(1)', 250);
            }

            showToast(`Added "${productName}" to shopping cart!`, 'success');
            // Auto open drawer to provide Flipkart/Amazon instant feedback
            openCartDrawer();
        } else {
            showToast(data.message || 'Could not add item to cart', 'warning');
        }
    } catch (err) {
        console.error('Add to cart failed:', err);
        showToast('Network error while adding to cart', 'error');
    }
}

// Update item quantity from inside Drawer
async function updateCartItemQty(itemId, newQty) {
    if (newQty < 1) return;

    try {
        const formData = new FormData();
        formData.append('quantity', newQty);

        const res = await fetch(`/cart/update/${itemId}`, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (res.ok) {
            loadCartDrawer();
        }
    } catch (err) {
        console.error('Failed to update quantity:', err);
    }
}

// Remove item from inside Drawer
async function removeCartItem(itemId) {
    try {
        const res = await fetch(`/cart/remove/${itemId}`);
        if (res.ok) {
            showToast('Item removed from cart', 'info');
            loadCartDrawer();
        }
    } catch (err) {
        console.error('Failed to remove item:', err);
    }
}

// ==========================================
// 4. Copy Coupon Code with Toast
// ==========================================
function copyCoupon(code) {
    if (!code) return;

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(() => {
            showToast(`Coupon code "${code}" copied to clipboard! Paste at checkout.`, 'success');
        }).catch(() => {
            fallbackCopy(code);
        });
    } else {
        fallbackCopy(code);
    }
}

function fallbackCopy(code) {
    const input = document.createElement('input');
    input.value = code;
    document.body.appendChild(input);
    input.select();
    try {
        document.execCommand('copy');
        showToast(`Coupon code "${code}" copied!`, 'success');
    } catch (e) {
        showToast(`Coupon code: ${code}`, 'info');
    }
    document.body.removeChild(input);
}

// ==========================================
// 5. Deal of the Day Countdown Timer
// ==========================================
function initDealTimer() {
    const timerEl = document.getElementById('deal-timer-clock');
    if (!timerEl) return;

    // Set end time 7 hours 34 mins from first load or stored time
    let totalSeconds = 7 * 3600 + 34 * 60 + 22;

    const interval = setInterval(() => {
        totalSeconds--;
        if (totalSeconds <= 0) {
            clearInterval(interval);
            timerEl.textContent = '00h : 00m : 00s';
            return;
        }

        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        const hStr = String(hours).padStart(2, '0');
        const mStr = String(minutes).padStart(2, '0');
        const sStr = String(seconds).padStart(2, '0');

        timerEl.textContent = `${hStr}h : ${mStr}m : ${sStr}s`;
    }, 1000);
}

// ==========================================
// 6. Modern Toast Notifications
// ==========================================
function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast-card toast-${type}`;

    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    else if (type === 'warning') icon = '⚠️';
    else if (type === 'error') icon = '❌';

    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-msg">${escapeHtml(message)}</span>
        <button type="button" class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(12px)';
        toast.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

// ==========================================
// 7. System Architecture Live Health Diagnostics
// ==========================================
async function checkLiveHealth() {
    const statusDisplay = document.getElementById('db-status-display');
    if (!statusDisplay) return;

    try {
        const response = await fetch('/api/health');
        if (!response.ok) throw new Error('API degraded');
        const data = await response.json();

        if (data.database && data.database.status === 'connected') {
            statusDisplay.textContent = `Connected (${data.database.engine.toUpperCase()})`;
            statusDisplay.className = 'metric-val text-success';
        } else {
            statusDisplay.textContent = `Degraded (${data.database.engine})`;
            statusDisplay.className = 'metric-val text-danger';
        }
    } catch (err) {
        statusDisplay.textContent = 'Server Check Offline';
        statusDisplay.className = 'metric-val text-muted';
    }
}

// ==========================================
// 8. Flash Alerts Dismissal
// ==========================================
function initFlashClose() {
    document.querySelectorAll('.alert-dismiss').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const alert = e.target.closest('.alert');
            if (alert) alert.remove();
        });
    });
}

// Helper: Escape HTML to prevent XSS
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
