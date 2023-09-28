import axios from 'axios';

const login = async () => {
  try {
    const endpoint = 'http://localhost:8080/bonita/loginservice';
    const username = 'anthony.nichols';
    const password = 'bpm';

    const response = await axios.post(
      endpoint,
      `username=${username}&password=${password}`,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        withCredentials: true, // Enable sending cookies with the request
      }
    );

    // Handle the response here
    console.log('Response:', response.data);


    return response.data;
  } catch (error) {
    // Handle errors here
    console.error('Error:', error);
    throw error;
  }
};

export default login;

