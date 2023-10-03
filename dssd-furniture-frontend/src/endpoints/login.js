import { API_URL, JWT_SECRET } from '../../config';
import axios from 'axios';
import jwt from 'jsonwebtoken';

const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}auth/login/`, {
      "email": username,
      "password": password
    });
    const { access } = response.data;
    return access;
  } catch (error) {
    throw error;
  }
};

export default login

export const logout = () => {
  localStorage.removeItem('token');
};

export const decodeToken = (token) => {
  return jwt.verify(token, JWT_SECRET);
};