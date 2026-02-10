/* ======================================================
   TOAST (AUTO CREATE)
====================================================== */

function createToastBox() {
    let toast = document.createElement("div");
    toast.id = "toast-msg";
    document.body.appendChild(toast);
}
createToastBox();

function showToast(message, type = "default") {
    const toast = document.getElementById("toast-msg");

    toast.className = "";
    toast.innerText = message;

    // Always visible over modals
    toast.style.zIndex = "9999999";

    toast.classList.add("show");

    if (type === "success") toast.classList.add("toast-success");
    else if (type === "danger") toast.classList.add("toast-danger");
    else if (type === "warning") toast.classList.add("toast-warning");
    else if (type === "dark") toast.classList.add("toast-dark");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2000);
}



/* ======================================================
   CONFIRM POPUP (AUTO CREATE)
====================================================== */

function createConfirmBox() {
    let box = document.createElement("div");
    box.id = "confirm-popup";

    box.innerHTML = `
        <p>Are you sure to remove?</p>
        <button id="confirm-yes">Yes</button>
        <button id="confirm-no">No</button>
    `;

    document.body.appendChild(box);
}
createConfirmBox();

let pendingRemoveId = null;

function showConfirm(itemId) {
    pendingRemoveId = itemId;
    document.getElementById("confirm-popup").classList.add("show");
}

function hideConfirm() {
    document.getElementById("confirm-popup").classList.remove("show");
}



// YES → Remove
document.addEventListener("click", async function (event) {
    if (event.target.id === "confirm-yes") {

        hideConfirm();

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const response = await fetch("/cart/remove-item/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `item_id=${pendingRemoveId}`
        });

        const data = await response.json();

        if (data.deleted) {
            document.getElementById(`cart-item-${pendingRemoveId}`).remove();
            showToast("Product removed!", "danger");
            setTimeout(() => location.reload(), 400);
        }
    }

    if (event.target.id === "confirm-no") {
        hideConfirm();
    }
});



/* ======================================================
   ADD TO CART
====================================================== */

const products_container = document.getElementById('products-container');
const cart_count = document.getElementById("cart-count");

const csrfToken = document.querySelector("[name = csrfmiddlewaretoken]").value;

if (products_container) {

    const addUrl = products_container.dataset.addUrl;

    products_container.addEventListener('click', async function (event) {

        if (!event.target.classList.contains('add-to-cart')) return;

        const btn = event.target;
        const product_card = btn.closest(".product-card-section");
        const productId = product_card.dataset.productId;

        btn.disabled = true;
        btn.innerText = "Loading...";

        try {
            const response = await fetch(addUrl, {
                method: "POST",
                headers: {
                    'X-CSRFToken': csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `product_id=${productId}`
            });

            const data = await response.json();

            if (data.cart_count !== undefined) {
                cart_count.innerText = data.cart_count;
            }

            showToast(data.message || "Product added!", "success");
        }
        catch {
            showToast("Error adding product!", "danger");
        }
        finally {
            btn.disabled = false;
            btn.innerText = "Add to Cart";
        }
    });
}



/* ======================================================
   UPDATE QTY (Increase / Decrease Toast)
====================================================== */

document.addEventListener("click", async function (event) {

    const btn = event.target.closest(".update-qty");
    if (!btn) return;

    const itemId = btn.dataset.item;
    const action = btn.dataset.action;

    const response = await fetch("/cart/update-qty/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `item_id=${itemId}&action=${action}`
    });

    const data = await response.json();

    if (data.deleted) {
        document.getElementById(`cart-item-${itemId}`).remove();
        showToast("Item removed", "danger");

        setTimeout(() => {
            location.reload();
        }, 900);
        return;
    }

    if (action === "increase") showToast("Quantity increased", "success");
    if (action === "decrease") showToast("Quantity decreased", "warning");

    setTimeout(() => {
        location.reload();
    }, 900);
});



/* ======================================================
   REMOVE BUTTON → SHOW CONFIRM
====================================================== */

document.addEventListener("click", function (event) {

    const btn = event.target.closest(".update-remove");
    if (!btn) return;

    const itemId = btn.dataset.item;
    showConfirm(itemId);
});



/* ======================================================
   NOTIFY BUTTON → TOAST ALERT
====================================================== */

document.addEventListener("click", function (event) {

    const notifyBtn = event.target.closest(".notify-btn");
    if (!notifyBtn) return;

    const productId = notifyBtn.dataset.product;

    showToast("We will notify you when the product is back in stock!", "dark");
});



/* ======================================================
   LOAD CART COUNT
====================================================== */

document.addEventListener("DOMContentLoaded", async function () {

    const cartCountElement = document.getElementById("cart-count");

    if (cartCountElement) {
        const url = cartCountElement.dataset.countUrl;

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (data.cart_count !== undefined) {
                cartCountElement.innerText = data.cart_count;
            }
        } catch (error) {
            console.error("Cart count load error:", error);
        }
    }
});


/* ======================================================
   NAVBAR INTERACTIVE EFFECTS
====================================================== */

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('mainNavbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add active class on hover for nav items
document.querySelectorAll('.navbar-nav .nav-item').forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.querySelector('.nav-link').classList.add('hover-active');
    });
    item.addEventListener('mouseleave', function() {
        this.querySelector('.nav-link').classList.remove('hover-active');
    });
});

// Dropdown menu animation enhancement
document.querySelectorAll('.dropdown-menu').forEach(menu => {
    menu.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

// Cart badge pulse animation on update
function pulseCartBadge() {
    const cartBadge = document.getElementById('cart-count');
    if (cartBadge) {
        cartBadge.style.transform = 'scale(1.3)';
        setTimeout(() => {
            cartBadge.style.transform = 'scale(1)';
        }, 200);
    }
}

// Call this function when cart is updated
window.pulseCartBadge = pulseCartBadge;

// for after click send messge 

document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Simple success alert
    alert("Your message was sent successfully!");

    // Reset form after alert
    this.reset();
});

