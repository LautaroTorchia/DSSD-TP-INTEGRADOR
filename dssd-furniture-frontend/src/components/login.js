// components/LoginForm.js
import { useState } from 'react';
import { login } from '@/endpoints/login';
import { useRouter } from 'next/router'; // Importa useRouter

export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter(); // Inicializa el enrutador

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await login(username, password);
      router.push('/');
    } catch (err) {
      setError('Credenciales inválidas. Por favor, inténtalo de nuevo.');
    }
  };

  return (
    <div className="container mt-5 d-flex justify-content-center"> {/* Centra el contenido horizontalmente */}
      <form onSubmit={handleSubmit} className="w-50"> {/* Establece un ancho máximo */}
        <div className="mb-3"> {/* Agrega la clase 'mb-3' para el margen inferior */}
          <label htmlFor="username" className="form-label">Username:</label> {/* Agrega la clase 'form-label' */}
          <input
            type="text"
            id="username"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3"> {/* Agrega la clase 'mb-3' para el margen inferior */}
          <label htmlFor="password" className="form-label">Password:</label> {/* Agrega la clase 'form-label' */}
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <button type="submit" className="btn btn-primary">Login</button> {/* Agrega las clases 'btn' y 'btn-primary' */}
        </div>
        {error && <p className="error mt-3">{error}</p>} {/* Agrega la clase 'mt-3' para el margen superior */}
      </form>
    </div>
  );
}

