import axios from 'axios';

const fetchProcesses = async () => {
  try {
    const endpoint = 'http://localhost:8000/api/bonita/list-processes/';

    // Read cookies from the browser's document.cookie
    console.log(document.cookie)
    var cookies=document.cookie
    console.log(cookies)

    const response = await axios.get(endpoint, {
      headers: {
        Cookie: cookies, // Set the cookies in the headers
      },
    });

    // Handle the response here
    console.log('Response:', response.data);

    return response.data;
  } catch (error) {
    // Handle errors here
    console.error('Error:', error);
    throw error;
  }
};

export default fetchProcesses;
