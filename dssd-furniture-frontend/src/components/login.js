// components/LoginForm.js
import { useState } from 'react';
import { login } from '@/endpoints/login'; 
import { useRouter } from 'next/router'; // Import useRouter

export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter(); // Initialize router

  const handleSubmit = async (e) => {
    e.preventDefault();

  
      
    try {
      await login(username, password);
      router.push("/");
    } catch (err) {
      setError('Invalid credentials. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <div>
        <button type="submit">Login</button>
      </div>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
