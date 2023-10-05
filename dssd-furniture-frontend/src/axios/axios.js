import axios from 'axios';
import { API_URL } from '@/../config';


const createApiClient = () => {
    return axios.create({
        baseURL: `${API_URL}`,
        headers: {
            Authorization: `Bearer ${sessionStorage.getItem('token')}`, 
            'Content-Type': 'application/json',
        },
    });
};

export default createApiClient;