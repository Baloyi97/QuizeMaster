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
});

function startTimer() {
    let timeLeft = 40 * 60; // 40 minutes in seconds
    const timerElement = document.getElementById('timer');

    if (!timerElement) {
        console.error('Element with ID "timer" not found.');
        return;
    }

    let timer = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(timer);
            alert("Time's up!");
            document.getElementById('quizForm').submit(); // Submit the form when time is up
        } else {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            timerElement.innerHTML = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`; // Display the timer
            timeLeft--;
        }
    }, 1000);

    console.log('Timer started!');
}

function handleSubmit(event) {
    event.preventDefault(); // Prevent form submission to handle it via JS

    // Extract chapter from URL path
    const pathParts = window.location.pathname.split('/');
    const chapter = parseInt(pathParts[pathParts.length - 1]);

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

    console.log('Chapter Score:', chapterScore); // Debug log to check chapter score

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

    // Add the score and current date to the data
    data['chapterScore'] = chapterScore;
    data['date'] = new Date().toISOString();
	


    console.log('Form Data:', data); // Debug log to check the data being sent

    // Convert form data to JSON
    const jsonData = JSON.stringify(data);

    // Send the JSON data to the server
    fetch('/submit-quiz', {  // Ensure this URL matches your Flask route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        results.innerHTML += '<p>Quiz results submitted successfully!</p>';
    })
    .catch((error) => {
        console.error('Error:', error);
    });
	

}
