import React, { useState } from 'react';
import styles from '../styles/collectionForm.module.css'; // Estilos específicos para el formulario
import login from '@/endpoints/login';
import fetchProcesses from '@/endpoints/fetchProcesses';

export default function CollectionForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    description: '',
    // Agrega más campos según sea necesario
  });
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleAuthentication = async (e) => {
    e.preventDefault();
    try {
      // Authenticate with Bonita and get cookies
      const cookies = await login('anthony.nichols', 'bpm');

      if (cookies) {
        setIsAuthenticated(true);
      } else {
        setIsAuthenticated(false);
        console.error('Authentication failed');
      }
      
    } catch (error) {
      console.error('Authentication error:', error);
      fetchProcesses()
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isAuthenticated) {
      // Proceed with form submission after successful authentication
      onSubmit(formData);
    } else {
      // Handle the case where authentication is required before submission
      console.error('Authentication is required before form submission');
    }
  };

  return (
    <div className={styles.container}>
      {isAuthenticated ? (
        <>
          <h2 className={styles.title}>Crear Nueva Colección</h2>
          <form onSubmit={handleSubmit}>
            {/* Form fields go here */}
            {/* ... */}
            <button
              type="submit"
              className={styles.submitButton}
            >
              Crear Colección
            </button>
          </form>
        </>
      ) : (
        <>
          <h2 className={styles.title}>Autenticación Requerida</h2>
          <form onSubmit={handleAuthentication}>
            <div className={styles.formGroup}>
              <label htmlFor="username" className={styles.label}>Usuario:</label>
              <input
                type="text"
                id="username"
                name="username"
                placeholder="Ingrese su usuario"
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="password" className={styles.label}>Contraseña:</label>
              <input
                type="password"
                id="password"
                name="password"
                placeholder="Ingrese su contraseña"
                required
              />
            </div>
            <button
              type="submit"
              className={styles.submitButton}
            >
              Iniciar Sesión
            </button>
          </form>
        </>
      )}
      {/* Additional content or instructions for the form */}
      <div className={styles.formInstructions}>
        <p>Por favor, complete el formulario para crear una nueva colección de muebles.</p>
        {/* You can add more instructions or information here */}
      </div>
    </div>
  );
}
