import axios from 'axios';

// Function to authenticate with the Bonita API and obtain cookies
async function authenticateWithBonita(username, password) {
  try {
    // Create a new Axios instance with a cookie jar
    const instance = axios.create({ withCredentials: true });

    // Send the POST request to the Bonita login endpoint
    const response = await instance.post('http://192.168.1.56:8080/bonita/loginservice', null, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      data: `username=${username}&password=${password}`,
    });

    // Check if the response contains cookies
    const cookies = response.headers['set-cookie'];
    
    if (cookies) {
      // Parse and extract the cookies you need
      const parsedCookies = cookies.map(cookie => {
        const parts = cookie.split(';')[0].split('=');
        return { name: parts[0], value: parts[1] };
      });

      return parsedCookies;
    }

    // Authentication failed
    throw new Error('Authentication failed');
  } catch (error) {
    // Handle any errors that occurred during the authentication process
    console.error('Authentication error:', error);
    throw error;
  }
}

export default authenticateWithBonita;
