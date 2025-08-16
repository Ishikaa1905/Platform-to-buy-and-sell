// Simple client-side interactions & validation
document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            const u = registerForm.querySelector("input[name='username']").value.trim();
            const p = registerForm.querySelector("input[name='password']").value.trim();
            if (u.length < 3) { alert("Username must be at least 3 characters."); e.preventDefault(); }
            if (p.length < 6) { alert("Password must be at least 6 characters."); e.preventDefault(); }
        });
    }

    const productForm = document.getElementById("productForm");
    if (productForm) {
        productForm.addEventListener("submit", function (e) {
            const name = productForm.querySelector("input[name='name']").value.trim();
            const price = parseFloat(productForm.querySelector("input[name='price']").value);
            if (!name) { alert("Product name cannot be empty."); e.preventDefault(); }
            if (!(price > 0)) { alert("Price must be greater than 0."); e.preventDefault(); }
        });
    }

    document.querySelectorAll('.product-item').forEach((el) => {
        el.addEventListener('click', () => {
            alert('You clicked on ' + el.dataset.name);
        });
    });
});
