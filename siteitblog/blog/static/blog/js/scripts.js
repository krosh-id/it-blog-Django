// Получить элемент поля ввода
const input = document.getElementById('my-input');

// Добавить обработчик события "focus"
input.addEventListener('focus', () => {
  // Изменить цвет фона при фокусировке
  input.style.backgroundColor = '#ffff00';
});

// Добавить обработчик события "blur"
input.addEventListener('blur', () => {
  // Сбросить цвет фона при потере фокуса
  input.style.backgroundColor = 'white';
});


//кастомный загрузчик
const realInput = document.getElementById('real-input');
realInput.addEventListener('change', function() {
    const fileName = realInput.value.split('\\').pop();
    document.querySelector('.custom-file-upload').textContent = fileName || 'Загрузить файл';
});