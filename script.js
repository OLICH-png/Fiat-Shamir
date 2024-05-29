$(document).ready(function() {
    // Функция для инициализации аутентификации
    function startAuth() {
        $.ajax({
            url: '/start_auth',
            type: 'POST',
            success: function(response) {
                if (response.status === 'continue') {
                    console.log('Starting authentication rounds');
                    performRound(response.v, response.x);
                } else {
                    alert(response.message);
                }
            }
        });
    }

    // Функция для выполнения аутентификационного раунда
    function performRound(v, x) {
        $.ajax({
            url: '/auth_round',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ e: Math.floor(Math.random() * 2) }), // Генерируем случайное значение e (0 или 1)
            success: function(response) {
                if (response.status === 'success') {
                    alert(response.message); // Аутентификация успешна
                } else if (response.status === 'failed') {
                    alert(response.message); // Аутентификация неуспешна
                } else if (response.status === 'continue') {
                    console.log('Round completed, continuing to next round');
                    performRound(response.v, response.x);  // Рекурсивный вызов для следующего раунда
                }
            }
        });
    }

    startAuth(); // Начинаем аутентификацию при загрузке страницы
});
