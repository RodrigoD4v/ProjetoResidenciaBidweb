document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input');
    const errorMessages = {};

    form.addEventListener('submit', function(event) {
        var hasError = false;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('error');
                const errorDiv = document.createElement('div');
                errorDiv.classList.add('error-message');
                errorDiv.textContent = 'Este campo é obrigatório';
                input.parentElement.insertBefore(errorDiv, input.nextSibling);
                errorMessages[input.name] = errorDiv;
                hasError = true; 
            }
        });

        if (hasError) {
            event.preventDefault();
        }
    });

    inputs.forEach(input => {
        input.addEventListener('input', function() {
            const errorMessage = errorMessages[input.name];
            if (errorMessage) {
                errorMessage.remove();
                delete errorMessages[input.name];
            }
            input.classList.remove('error');
        });
    });
});
