import React, { useState } from 'react';
import styles from '../styles/collectionForm.module.css'; // Estilos específicos para el formulario

export default function CollectionForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    description: '',
    // Agrega más campos según sea necesario
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Crear Nueva Colección</h2>
      <form onSubmit={handleSubmit}>
        <div className={styles.formGroup}>
          <label htmlFor="name" className={styles.label}>Nombre:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={styles.input}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="category" className={styles.label}>Categoría:</label>
          <input
            type="text"
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            className={styles.input}
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="description" className={styles.label}>Descripción:</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className={styles.textarea}
            required
          />
        </div>
        {/* Agrega más campos según sea necesario */}
        <button
          type="submit"
          className={styles.submitButton}
        >
          Crear Colección
        </button>
      </form>
      {/* Additional content or instructions for the form */}
      <div className={styles.formInstructions}>
        <p>Por favor, complete el formulario para crear una nueva colección de muebles.</p>
        {/* You can add more instructions or information here */}
      </div>
    </div>
  );
}
