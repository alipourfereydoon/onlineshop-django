function getCsrfToken() {
  // Try to read CSRF from form input; fallback to variable from base.html
  const tokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
  if (tokenEl) return tokenEl.value;
  return window.csrfToken || '';
}

function postJson(url, body) {
  return fetch(url, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify(body)
  }).then(r => r.json());
}

// Add/remove cart actions
document.addEventListener('click', function (e) {

  // Add to cart
  if (e.target.matches('.add-to-cart')) {
    const id = e.target.dataset.id;
    postJson('/api/cart/add/', { product_id: id, quantity: 1 })
      .then(resp => {
        if (resp.ok) {
          alert('Added to cart');
        }
      });
  }

  // Remove from cart
  if (e.target.matches('.remove-from-cart')) {
    const id = e.target.dataset.id;
    postJson('/api/cart/remove/', { product_id: id })
      .then(resp => {
        if (resp.ok) {
          location.reload(); // refresh cart page
        }
      });
  }
});