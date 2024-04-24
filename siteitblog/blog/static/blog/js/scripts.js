document.addEventListener('DOMContentLoaded', function() {
    // Ваш код, который зависит от элементов DOM, должен идти здесь
    const textarea = document.querySelector('textarea');
    const counter = document.getElementById('counter-input');
    const maxlength = 500;

    textarea.addEventListener('input', onInput);

    function onInput(event) {
        event.target.value = event.target.value.substr(0, maxlength);
        const length = event.target.value.length;
        counter.textContent = length;

    }


    const imageInput = document.getElementById('real-input'); // Получаем элемент input
    // Обработчик события, который вызывается при выборе файла
    imageInput.addEventListener('change', function() {
        const files = this.files; // Получаем выбранные файлы
        if (files && files.length > 0) {
            // Предполагаем, что первый файл уже является изображением
            updateCounterImage(1); // Обновляем счетчик изображений
        } else {
            updateCounterImage(0); // Если файлов нет, обновляем счетчик на 0
        }
    });

    function updateCounterImage(count) {
        const counterImageElement = document.getElementById('counter-image');
        counterImageElement.textContent = count; // Обновляем текстовое содержимое элемента
    }
});

