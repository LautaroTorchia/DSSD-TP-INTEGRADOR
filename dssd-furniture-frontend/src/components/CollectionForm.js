import { useState } from 'react';

export default function ColeccionForm({ onSubmit, collection }) {
  if (!collection) {
    collection = {
      nombre: '',
      descripcion: '',
    };
  }
  const [nombre, setNombre] = useState(collection.nombre);
  const [descripcion, setDescripcion] = useState(collection.descripcion);

  const handleSubmit = (e) => {
    e.preventDefault();

    const collectionData = {
      nombre,
      descripcion,
      terminada: false,
      instancia_bonita: null,
    };

    onSubmit(collectionData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="nombre">Nombre:</label>
        <input
          type="text"
          id="nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="descripcion">Descripción:</label>
        <textarea
          id="descripcion"
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
          required
        ></textarea>
      </div>
      <div>
        <button type="submit">Guardar</button>
      </div>
    </form>
  );
}
