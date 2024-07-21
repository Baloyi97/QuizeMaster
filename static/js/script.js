// Function to start the timer
function startTimer() {
    let timeLeft = 40 * 60; // 40 minutes in seconds
    let timer = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(timer);
            alert("Time's up!");
            document.getElementById('quizForm').submit(); // Submit the form when time is up
        } else {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            document.getElementById('timer').innerHTML = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`; // Display the timer
            timeLeft--;
        }
    }, 1000);
}

// Function to handle form submission and calculate results
function handleSubmit(event) {
    event.preventDefault(); // Prevent form submission to handle it via JS

    // Extract chapter from URL path
    const pathParts = window.location.pathname.split('/');
    const chapter = parseInt(pathParts[pathParts.length - 1]);

    // Print the chapter value to the console
    console.log("Retrieved chapter value from URL:", chapter);

    // Define correct answers object for each chapter
    const correctAnswers = {
        1: {0: 2, 1: 3, 2: 2, 3: 2, 4: 1},
        2: {0: 1, 1: 3, 2: 2, 3: 2, 4: 1},
        3: {0: 3, 1: 2, 2: 2, 3: 1, 4: 1},
        4: {0: 3, 1: 2, 2: 3, 3: 3, 4: 3},
        5: {0: 1, 1: 3, 2: 2, 3: 2, 4: 4, 5: 1, 6: 2, 7: 1, 8: 2, 9: 1}
    };

    if (isNaN(chapter) || !correctAnswers[chapter]) {
        console.error("Invalid chapter selected.");
        const results = document.getElementById('results');
        if (results) {
            results.innerHTML = '<p style="color: red;">Invalid chapter. Please go back to the dashboard and select a chapter.</p>';
        }
        return;
    }

    const form = document.getElementById('quizForm');
    const results = document.getElementById('results');
    results.innerHTML = '';

    let chapterScore = 0;
    let allAnswered = true;

    Object.keys(correctAnswers[chapter]).forEach(question => {
        const userAnswer = form.querySelector(`input[name="question${question}"]:checked`);
        const resultText = document.createElement('p');

        if (userAnswer) {
            if (parseInt(userAnswer.value) === correctAnswers[chapter][question]) {
                resultText.classList.add('correct-answer');
                resultText.textContent = `Question ${question}: Correct!`;
                chapterScore += 1; // Increment chapter score for correct answer
            } else {
                resultText.classList.add('incorrect-answer');
                resultText.textContent = `Question ${question}: Incorrect. The correct answer is "${correctAnswers[chapter][question]}".`;
            }
        } else {
            resultText.classList.add('incorrect-answer');
            resultText.textContent = `Question ${question}: No answer selected. The correct answer is "${correctAnswers[chapter][question]}".`;
            allAnswered = false;
        }

        results.appendChild(resultText);
    });

    if (!allAnswered) {
        alert('Please answer all questions.');
        return;
    }

    const scoreText = document.createElement('h3');
    scoreText.textContent = `Your Score: ${chapterScore} / ${Object.keys(correctAnswers[chapter]).length}`; // Display chapter score
    results.appendChild(scoreText);

    // Serialize the form data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Add the score to the data
    data['chapterScore'] = chapterScore; // Add chapter score to the data

    // Convert form data to JSON
    const jsonData = JSON.stringify(data);

    // Send the JSON data to the server
    fetch('/submit-quiz', {  // Make sure this URL matches your server route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Popup and Form Handling Functions
document.addEventListener('DOMContentLoaded', () => {
    // Start the timer
    startTimer();

    // Handle quiz submission
    const submitButton = document.getElementById('submitQuiz');
    if (submitButton) {
        submitButton.addEventListener('click', handleSubmit);
    } else {
        console.error('Element with ID "submitQuiz" not found.');
    }

    const quizForm = document.getElementById('quizForm');
    if (quizForm) {
        quizForm.addEventListener('submit', handleSubmit);
    } else {
        console.error('Element with ID "quizForm" not found.');
    }

    // Popup handling
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

    // Functions for form display
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

    // Event listeners for form display
    document.getElementById('loginLink').addEventListener('click', openLoginForm);
    document.getElementById('registerLink').addEventListener('click', openRegisterForm);
    document.getElementById('closePopup').addEventListener('click', closePopup);

    // Display the popup if a danger message exists
    window.onload = function() {
        const popup = document.getElementById('popup');
        if (popup && popup.querySelector('p').innerText.includes('incorrect')) {
            popup.style.display = 'flex';
        }
    };

    // Validate register form
    function validateRegisterForm() {
        const termsCheckbox = document.getElementById('terms');
        if (!termsCheckbox.checked) {
            alert('You must agree to the terms and conditions to register.');
            return false;
        }
        return true;
    }

    const termsLink = document.getElementById('termsLink');
    if (termsLink) {
        termsLink.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent the default link behavior
            window.location.href = this.href; // Navigate to the terms and conditions page
        });
    }

    // Toggle password visibility
    function togglePasswordVisibility(inputId, iconId) {
        const passwordInput = document.getElementById(inputId);
        const passwordIcon = document.getElementById(iconId);
        
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            passwordIcon.setAttribute("name", "eye");
        } else {
            passwordInput.type = "password";
            passwordIcon.setAttribute("name", "lock-closed");
        }
    }

    // Add event listeners to icons
    const togglePasswordIcon = document.getElementById('togglePasswordIcon');
    const toggleRegisterPasswordIcon = document.getElementById('toggleRegisterPasswordIcon');

    if (togglePasswordIcon) {
        togglePasswordIcon.addEventListener('click', () => {
            togglePasswordVisibility('loginPassword', 'togglePasswordIcon');
        });
    }

    if (toggleRegisterPasswordIcon) {
        toggleRegisterPasswordIcon.addEventListener('click', () => {
            togglePasswordVisibility('registerPassword', 'toggleRegisterPasswordIcon');
        });
    }
});
