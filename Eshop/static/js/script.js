// Cart handling

// Add to cart

const products_container = document.getElementById('products-container');

const cart_count = document.getElementById("cart-count");

const csrfToken = document.querySelector("[name = csrfmiddlewaretoken]").value

// add to cart url 
const addUrl = products_container.dataset.addUrl;

// adding event listener onto product cards through their parent container

products_container.addEventListener('click', async function (event) {

    if (!event.target.classList.contains('add-to-cart')) {
        return;
    }

    const btn = event.target;
    const product_card = btn.closest(".product-card");
    const productId = product_card.dataset.productId;

    btn.disabled = true;
    btn.innerText = "Loading...";

    // try to make a POST request
    try {
        const response = await fetch(addUrl, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `product_id=${productId}`
        })
        const data = await response.json();

        // if the backend returns 401 status,
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