
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

$(document).ready(function() {
    const buttons = document.querySelectorAll('.items-named__product-button');
    buttons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const productId = event.target.parentNode.id;
            const inCart = event.target.dataset.inCart;
            const csrftoken = getCookie('csrftoken');

            if(inCart !== 'false'){
                fetch(`/cart/remove/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },  // Устанавливаем CSRF-токен в заголовке запроса
                body: JSON.stringify({productId: productId}),
                dataType: 'json'
                })
                .then(response => {
                    if (response.ok) {
                        alert('Товар успешно удалён из корзины!');
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
                fetch(`/cart/add/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },  // Устанавливаем CSRF-токен в заголовке запроса
                body: JSON.stringify({productId: productId}),
                dataType: 'json'
                })
                .then(response => {
                    if (response.ok) {
                        alert('Товар успешно добавлен в корзину!');
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
})

