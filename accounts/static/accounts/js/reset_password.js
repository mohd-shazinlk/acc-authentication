document.addEventListener('DOMContentLoaded', function() {
    // Password validation logic for reset password page
    const passwordInput = document.querySelector('input[name="new_password"]');
    const password2Input = document.querySelector('input[name="confirm_password"]');
    const passwordMatchError = document.getElementById('password-match-error');

    const rules = {
        'min-chars': (val) => val.length >= 8,
        'capital-small': (val) => /[a-z]/.test(val) && /[A-Z]/.test(val),
        'number': (val) => /\d/.test(val),
        'symbol': (val) => /[\W_]/.test(val),
    };

    if (passwordInput) {
        passwordInput.addEventListener('keyup', function() {
            const val = this.value;
            for (const ruleId in rules) {
                const ruleElement = document.getElementById(ruleId);
                if (rules[ruleId](val)) {
                    ruleElement.classList.add('valid');
                } else {
                    ruleElement.classList.remove('valid');
                }
            }
            validatePasswordMatch();
        });
    }

    if (password2Input) {
        password2Input.addEventListener('keyup', validatePasswordMatch);
    }

    function validatePasswordMatch() {
        if (passwordInput && password2Input && passwordMatchError) {
            if (passwordInput.value !== password2Input.value && password2Input.value !== "") {
                passwordMatchError.textContent = 'Password not match';
                passwordMatchError.style.color = 'var(--error-color)';
            } else if (passwordInput.value === password2Input.value && password2Input.value !== "") {
                passwordMatchError.textContent = 'Password matched';
                passwordMatchError.style.color = 'var(--success-color)';
            } else {
                passwordMatchError.textContent = '';
            }
        }
    }
}); 