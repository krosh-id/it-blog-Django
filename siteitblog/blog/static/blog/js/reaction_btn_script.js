// Функция для получения значения cookie по имени
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
    // Обработчик события клика по кнопке лайка
    $('.button-icon-like').click(function(event) {
        event.preventDefault();

        let id = $(this).data('id');
        let modelType = $(this).data('type');
        let likesCountElement = $('#likes-count-' + modelType + '-' + id);
        let currentLikes = parseInt(likesCountElement.text().trim());
        // Получаем CSRF-токен из cookies
        let csrftoken = getCookie('csrftoken');


        // Отправляем AJAX-запрос для добавления лайка с CSRF-токеном в заголовке
        $.ajax({
            type: 'POST',
            url: `/${modelType}/like`,
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },  // Устанавливаем CSRF-токен в заголовке запроса
            data: JSON.stringify({
                modelId: id
            }),  // Преобразуем объект в JSON строку
            dataType: 'json', // Указываем, что ожидаем JSON-ответ
            success: function(response) {
                let newLikesCount = 0
                if (response['status'] === 'remove') {
                    newLikesCount = currentLikes - 1;
                }else{
                    newLikesCount = currentLikes + 1;
                }
                likesCountElement.text(newLikesCount);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});
