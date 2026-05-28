document.addEventListener('DOMContentLoaded', () => {

    // ─── Navbar Scroll Effect ───
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 30);
        }, { passive: true });
    }

    // ─── Auto-dismiss Flash Messages ───
    const flashes = document.querySelectorAll('.flash-msg');
    flashes.forEach((flash, i) => {
        setTimeout(() => {
            flash.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(120%)';
            setTimeout(() => flash.remove(), 400);
        }, 4000 + i * 500);
    });

    // ─── Quantity +/- on Product Page ───
    const qtyInput = document.getElementById('qty-input');
    const btnMinus = document.getElementById('btn-minus');
    const btnPlus = document.getElementById('btn-plus');

    if (qtyInput && btnMinus && btnPlus) {
        btnMinus.addEventListener('click', () => {
            let val = parseInt(qtyInput.value);
            if (val > 1) {
                qtyInput.value = val - 1;
                pulseBtn(btnMinus);
            }
        });
        btnPlus.addEventListener('click', () => {
            let val = parseInt(qtyInput.value);
            let max = parseInt(qtyInput.getAttribute('max') || 100);
            if (val < max) {
                qtyInput.value = val + 1;
                pulseBtn(btnPlus);
            }
        });
    }

    function pulseBtn(btn) {
        btn.style.transform = 'scale(1.2)';
        setTimeout(() => { btn.style.transform = 'scale(1)'; }, 150);
    }

    // ─── Dropdown / Kebab Toggle ───
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const btn = dropdown.querySelector('.kebab-menu');
        const content = dropdown.querySelector('.dropdown-content');
        if (btn && content) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                document.querySelectorAll('.dropdown-content.show').forEach(c => {
                    if (c !== content) c.classList.remove('show');
                });
                content.classList.toggle('show');
            });
        }
    });

    document.addEventListener('click', () => {
        document.querySelectorAll('.dropdown-content.show').forEach(c => c.classList.remove('show'));
    });

    // ─── Scroll Reveal for Product Cards ───
    const revealElements = document.querySelectorAll('.product-card, .stat-card, .cart-summary, .cart-table');
    if (revealElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 80);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(el);
        });
    }

    // ─── Add-to-cart button feedback ───
    document.querySelectorAll('form[action*="add_to_cart"]').forEach(form => {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            if (btn) {
                btn.style.transform = 'scale(0.9)';
                setTimeout(() => { btn.style.transform = ''; }, 200);
            }
        });
    });
});
