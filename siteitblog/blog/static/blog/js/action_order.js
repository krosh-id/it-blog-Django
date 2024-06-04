
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

function deleteOrder(button, csrftoken, orderId){
    return fetch(`/order/remove/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },  // Устанавливаем CSRF-токен в заголовке запроса
                body: JSON.stringify({orderId: orderId}),
                dataType: 'json'
                })
}


$(document).ready(function() {
    const buttons_remove = document.querySelectorAll('.items-named__order-button-remove');

    buttons_remove.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const orderCart = event.target.closest('.items-named__product-orders');
            const orderId = orderCart.id;
            const csrftoken = getCookie('csrftoken');

            deleteOrder(button, csrftoken, orderId).then(response => {
                if(response.ok){
                    orderCart.remove();
                }
                else{
                    alert('Произошла ошибка при удалении заказа');
                }
            })
            .catch(error => {
                    console.error('Ошибка:', error);
                })
        });
    });
})



