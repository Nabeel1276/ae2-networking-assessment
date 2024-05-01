// Importing the 'http' module
const http = require('http');

// Define the hostname and port on which the server will listen
const hostname = '127.0.0.1'; // Localhost
const port = 3000; // Port 3000

// Creating the server
const server = http.createServer((req, res) => {
  // Setting the status code and content type of the response
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  
  // Sending a response back to the client
  res.end('Hello, World!\n');
});

// Start the server and listen on the specified port and hostname
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
