document.addEventListener('DOMContentLoaded', function() {
    var usernameInput = document.querySelector('input[name="username"]');
    var feedbackElement = document.querySelector('.username-feedback');

    var form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        var username = usernameInput.value;
        if (username.length >= 3) {
            checkUsernameAvailability(username);
        }
    });

    usernameInput.addEventListener('input', function() {
        feedbackElement.innerText = '';
        usernameInput.classList.remove('error');
    });

    function checkUsernameAvailability(username) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/check_username/?username=' + encodeURIComponent(username), true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.exists) {
                        feedbackElement.innerText = 'Este nome de usuário já está em uso.';
                        usernameInput.classList.add('error');
                    } else {
                        feedbackElement.innerText = '';
                        usernameInput.classList.remove('error');
                        form.submit();
                    }
                } else {
                    feedbackElement.innerText = 'Erro ao verificar o nome de usuário.';
                    usernameInput.classList.add('error');
                }
            }
        };
        xhr.send();
    }
});
