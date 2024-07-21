document.addEventListener('DOMContentLoaded', () => {
    // Popup and Form Handling Functions
    const wrapper = document.querySelector('.wrapper');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const btnPopup = document.querySelector('.Login-popup');
    const iconClose = document.querySelector('.icon-close');

    if (registerLink) {
        registerLink.addEventListener('click', () => {
            wrapper.classList.add('active');
        });
    }

    if (loginLink) {
        loginLink.addEventListener('click', () => {
            wrapper.classList.remove('active');
        });
    }

    if (btnPopup) {
        btnPopup.addEventListener('click', () => {
            wrapper.classList.add('active-popup');
        });
    }

    if (iconClose) {
        iconClose.addEventListener('click', () => {
            wrapper.classList.remove('active-popup');
        });
    }

    window.closePopup = function() {
        const popup = document.getElementById('popup');
        if (popup) {
            popup.style.display = 'none';
            openLoginForm(); // Open the login form after closing the popup
        }
    };

    function openLoginForm() {
        document.getElementById('loginForm').style.display = 'block';
        document.getElementById('registerForm').style.display = 'none';
    }

    function openRegisterForm() {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('registerForm').style.display = 'block';
    }

    function closeLoginForm() {
        document.getElementById('loginForm').style.display = 'none';
    }

    // Display popup messages if present
    const popup = document.getElementById('popup');
    if (popup) {
        const messageType = popup.getAttribute('data-message-type');
        if (messageType) {
            const messageText = popup.getAttribute('data-message-text');
            document.querySelector('.popup-content p').innerText = messageText;
            popup.style.display = 'flex';
        }
    }

    // Handle password visibility toggle
    function togglePasswordVisibility(inputId, iconId) {
        const passwordInput = document.getElementById(inputId);
        const passwordIcon = document.getElementById(iconId);

        if (!passwordInput || !passwordIcon) {
            console.error('Password input or icon element not found.');
            return;
        }

        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            passwordIcon.classList.remove('lock-closed');
            passwordIcon.classList.add('lock-open');
        } else {
            passwordInput.type = 'password';
            passwordIcon.classList.remove('lock-open');
            passwordIcon.classList.add('lock-closed');
        }
    }

    const togglePasswordIcon = document.getElementById('togglePasswordIcon');
    if (togglePasswordIcon) {
        togglePasswordIcon.addEventListener('click', () => {
            togglePasswordVisibility('loginPassword', 'togglePasswordIcon');
        });
    }

    const toggleRegisterPasswordIcon = document.getElementById('toggleRegisterPasswordIcon');
    if (toggleRegisterPasswordIcon) {
        toggleRegisterPasswordIcon.addEventListener('click', () => {
            togglePasswordVisibility('registerPassword', 'toggleRegisterPasswordIcon');
        });
    }

    // Add event listener for the close button on the popup
    const closeBtn = document.querySelector('.close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', window.closePopup);
    }
});
