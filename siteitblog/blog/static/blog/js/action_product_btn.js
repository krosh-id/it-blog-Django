
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Проверяем, начинается ли куки с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteProductCart(button, csrftoken, productId){
    return fetch(`/cart/remove/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },  // Устанавливаем CSRF-токен в заголовке запроса
                body: JSON.stringify({productId: productId}),
                dataType: 'json'
                })
}

function addProductCart(button, csrftoken, productId){
    return fetch(`/cart/add/`,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },  // Устанавливаем CSRF-токен в заголовке запроса
            body: JSON.stringify({productId: productId}),
            dataType: 'json'
        })
}

$(document).ready(function() {
    const buttons = document.querySelectorAll('.items-named__product-button');
    const buttons_remove = document.querySelectorAll('.items-named__cart-button-remove');

    const total_price_value = document.querySelector('.items-named__product-cart__total-value');
    const order_btn = document.querySelector('.items-named__product-cart-btn');

    buttons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const productId = event.target.parentNode.id;
            const inCart = event.target.dataset.inCart;
            const csrftoken = getCookie('csrftoken');

            if(inCart !== 'false'){
                deleteProductCart(button, csrftoken, productId).then(response => {
                    if (response.ok) {
                        button.classList.remove('remove-btn')
                        button.textContent = 'Купить'
                        } else {
                            alert('Произошла ошибка при удалении товара из корзины.');
                        }
                        })
                        .catch(error => {
                            console.error('Ошибка:', error);
                        });
            }
            else{
                addProductCart(button, csrftoken, productId).then(response => {
                    if (response.ok) {
                        button.classList.add('remove-btn')
                        button.textContent = 'Добавлено в корзину'
                    } else {
                        alert('Произошла ошибка при добавлении товара в корзину.');
                    }
                    })
                    .catch(error => {
                        console.error('Ошибка:', error);
                    });
            }
        });
    });

    buttons_remove.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const productCart = event.target.closest('.items-named__product-cart');
            const productId = productCart.id;
            const priceValue = parseFloat(productCart.querySelector('.items-named__product-cart__price-value').textContent.slice(0, -1));

            const csrftoken = getCookie('csrftoken');

            deleteProductCart(button, csrftoken, productId).then(response => {
                if(response.ok){
                    productCart.remove();
                    total_price_value.textContent = String(parseFloat(total_price_value.textContent) - priceValue)
                    if(total_price_value.textContent === "0"){
                        order_btn.remove()
                    }
                }
                else{
                    alert('Произошла ошибка при удалении товара из корзины.');
                }
            })
            .catch(error => {
                    console.error('Ошибка:', error);
                })
        });
    });
})



