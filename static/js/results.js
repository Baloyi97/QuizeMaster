document.addEventListener('DOMContentLoaded', () => {
    startTimer();

    document.getElementById('quizForm').addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Simulate a form submission and fetching the results
        const formData = new FormData(this);
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Assuming the response contains a field called 'resultMessage'
            document.getElementById('resultMessage').innerText = data.resultMessage;

            // Show the modal
            $('#resultsModal').modal('show');
        })
        .catch(error => console.error('Error:', error));
    });

 
    });

