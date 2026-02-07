// Cart handling

// Add to cart
const products_container = document.getElementById('products-container');
const cart_count = document.getElementById("cart-count");

const csrfToken = document.querySelector("[name = csrfmiddlewaretoken]").value;

// Run ONLY if products_container exists
if (products_container) {

    const addUrl = products_container.dataset.addUrl;

    products_container.addEventListener('click', async function (event) {

        if (!event.target.classList.contains('add-to-cart')) {
            return;
        }

        const btn = event.target;
        const product_card = btn.closest(".product-card");
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

            if (response.status === 401 && data.redirect_url) {
                window.location.href = data.redirect_url;
                return;
            }

            if (data.cart_count !== undefined) {
                cart_count.innerText = data.cart_count;
            }
        }
        catch (error) {
            console.error("Cart error:", error);
        }
        finally {
            btn.disabled = false;
            btn.innerText = "Add to Cart";
        }
    });
}



// ==============================
// Update Quantity in Cart Page
// ==============================

document.addEventListener("click", async function (event) {

    const btn = event.target.closest(".update-qty");
    if (!btn) return;  // Do nothing if clicked outside the qty buttons

    const itemId = btn.dataset.item;
    const action = btn.dataset.action;

    console.log("Updating item:", itemId, "Action:", action);

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

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
        location.reload();
        return;
    }

    document.getElementById(`qty-${itemId}`).innerText = data.quantity;
    location.reload();
});



// ==============================
// Remove Item from Cart
// ==============================

document.addEventListener("click", async function (event) {

    const btn = event.target.closest(".update-remove");
    if (!btn) return;

    const itemId = btn.dataset.item;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    console.log("Removing item:", itemId);

    const response = await fetch("/cart/remove-item/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `item_id=${itemId}`
    });

    const data = await response.json();

    if (data.deleted) {
        document.getElementById(`cart-item-${itemId}`).remove();
        location.reload();
    }
});


//  for Alert msg notify me product if available
document.addEventListener("DOMContentLoaded", function () {
    let notifyButtons = document.querySelectorAll(".notify-btn");

    notifyButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            let notifyModal = new bootstrap.Modal(document.getElementById("notifyModal"));
            notifyModal.show();
        });
    });
});



// ==========================
// Load Cart Count on page load
// ==========================
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

