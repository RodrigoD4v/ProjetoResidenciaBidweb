document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        var username = form.querySelector("input[name='username']").value;
        var password = form.querySelector("input[name='password']").value;

        clearError();

        if (username.trim() === "" || password.trim() === "") {
            event.preventDefault(); 
            showError("Por favor, preencha todos os campos.");
        }
    });

    function showError(message) {
        var errorMessage = document.createElement("p");
        errorMessage.textContent = message;
        errorMessage.classList.add("error-message");

        var passwordInput = form.querySelector("input[name='password']");
        passwordInput.parentNode.insertBefore(errorMessage, passwordInput.nextSibling);

        form.querySelector("input[name='username']").classList.add("error");
        form.querySelector("input[name='password']").classList.add("error");
    }

    function clearError() {
        var errorMessage = form.querySelector(".error-message");
        if (errorMessage !== null && !errorMessage.classList.contains("credential-error")) {
            errorMessage.parentNode.removeChild(errorMessage);

            form.querySelectorAll("input").forEach(function(input) {
                input.classList.remove("error");
            });
        }
    }

    form.querySelectorAll("input").forEach(function(input) {
        input.addEventListener("input", function() {
            input.classList.remove("error");

            var errorMessage = input.nextElementSibling;
            if (errorMessage && errorMessage.classList.contains("error-message")) {
                errorMessage.remove();
            }
        });
    });
});
