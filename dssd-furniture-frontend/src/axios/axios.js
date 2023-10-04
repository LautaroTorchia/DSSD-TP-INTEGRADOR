import axios from 'axios';
import { API_URL } from '@/../config'; // Replace with your API URL

const createApiClient = () => {
    return axios.create({
        baseURL: `${API_URL}`,
        headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`, // Use the provided token
            'Content-Type': 'application/json',
        },
    });
};

export default createApiClient;