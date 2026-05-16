document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash messages after 5 seconds
    const flashes = document.querySelectorAll('.flash-msg');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });

    // Simple Quantity Increment/Decrement for Product Page
    const qtyInput = document.getElementById('qty-input');
    const btnMinus = document.getElementById('btn-minus');
    const btnPlus = document.getElementById('btn-plus');

    if (qtyInput && btnMinus && btnPlus) {
        btnMinus.addEventListener('click', () => {
            let val = parseInt(qtyInput.value);
            if (val > 1) {
                qtyInput.value = val - 1;
            }
        });

        btnPlus.addEventListener('click', () => {
            let val = parseInt(qtyInput.value);
            let max = parseInt(qtyInput.getAttribute('max') || 100);
            if (val < max) {
                qtyInput.value = val + 1;
            }
        });
    }

    // Dropdown / Kebab Menu Toggle
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const btn = dropdown.querySelector('.kebab-menu');
        const content = dropdown.querySelector('.dropdown-content');
        
        if (btn && content) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                // Close all other dropdowns first
                document.querySelectorAll('.dropdown-content.show').forEach(c => {
                    if (c !== content) c.classList.remove('show');
                });
                content.classList.toggle('show');
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        document.querySelectorAll('.dropdown-content.show').forEach(c => c.classList.remove('show'));
    });
});
