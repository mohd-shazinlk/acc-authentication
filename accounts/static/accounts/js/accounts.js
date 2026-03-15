document.addEventListener('DOMContentLoaded', function() {
    // Tab switching logic
    window.openTab = function(evt, tabName, isLink) {
        if (isLink) {
            evt.preventDefault();
        }
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tab-content");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tab-link");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(tabName).style.display = "block";
        
        // Find the button that corresponds to this tab and activate it
        const activeButton = Array.from(tablinks).find(btn => btn.textContent.toLowerCase() === tabName);
        if(activeButton) {
            activeButton.className += " active";
        }
    }

    // Password validation logic
    const passwordInput = document.querySelector('#register input[name="password"]');
    const password2Input = document.querySelector('#register input[name="password2"]');
    const passwordMatchError = document.getElementById('password-match-error');

    const rules = {
        'min-chars': (val) => val.length >= 8,
        'capital-small': (val) => /[a-z]/.test(val) && /[A-Z]/.test(val),
        'number': (val) => /\d/.test(val),
        'symbol': (val) => /[\W_]/.test(val), // Matches any non-alphanumeric character
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