const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.Login-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
})

loginLink.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
})

btnPopup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
})

iconClose.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
})


function closePopup() {
    document.getElementById('popup').style.display = 'none';
    openLoginForm();
}

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

// Display the popup if a danger message exists
window.onload = function() {
    const popup = document.getElementById('popup');
    if (popup && popup.querySelector('p').innerText.includes('incorrect')) {
        popup.style.display = 'flex';
    }
};

function validateRegisterForm() {
    const termsCheckbox = document.getElementById('terms');
    if (!termsCheckbox.checked) {
        alert('You must agree to the terms and conditions to register.');
        return false;
    }
    return true;
}


document.addEventListener('DOMContentLoaded', (event) => {
    const termsLink = document.getElementById('termsLink');

    if (termsLink) {
        termsLink.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent the default link behavior
            window.location.href = this.href; // Navigate to the terms and conditions page
        });
    }
});

