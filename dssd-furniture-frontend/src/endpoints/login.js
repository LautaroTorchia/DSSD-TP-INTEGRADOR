import axios from 'axios';
import jwt from 'jsonwebtoken';
import { loginToBonita } from '@/endpoints/bonitalogin';
import { API_URL, JWT_SECRET } from '@/../config';

const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}auth/login/`, {
      email: username,
      password: password,
    });
    localStorage.setItem('token', response.data.tokens.access);
    localStorage.setItem('refreshToken', response.data.tokens.refresh);
    const bonitaLoginResponse = await loginToBonita('anthony.nichols', 'bpm',response.data.tokens.access);
    console.log(bonitaLoginResponse)
    return response.data.access;
  } catch (error) {
    throw error;
  }
};

const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refreshToken'); // Retrieve refresh token from localStorage
    if (!refreshToken) {
      throw new Error('Refresh token not found');
    }

    const response = await axios.post(`${API_URL}auth/token/refresh/`, {
      refresh: refreshToken,
    });
    
    const newAccessToken = response.data.access;
    localStorage.setItem('token', newAccessToken);
    return newAccessToken;
  } catch (error) {
    throw error;
  }
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('refreshToken'); // Remove the refresh token on logout
};

const decodeToken = (token) => {
  return jwt.verify(token, JWT_SECRET);
};

const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  return !!token; 
};


export { login, logout, decodeToken, refreshAccessToken, isAuthenticated };