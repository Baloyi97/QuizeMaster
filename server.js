require('dotenv').config();

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
const port = 3000;
const gitToken = process.env.GIT_TOKEN;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Middleware to enable CORS
app.use(cors());

// Middleware to serve static files
app.use(express.static('static'));

// Define the /submit-quiz route
app.post('/quiz/<int:chapter>', (req, res) => {
  console.log(req.body);
  res.send('Quiz submitted successfully');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
